from dataclasses import dataclass
from json import dumps, loads
from typing import Any, Callable, Sequence, Type

from db.db import async_session_maker
from db.models.base import BaseCommon
from exceptions.sa_handler_manager import ErrorHandler
from loguru import logger
from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.orm import load_only, raiseload


class CRUDSA:

    def __init__(
            self,
            model: Type[BaseCommon],
            # session: Session,
            *args: Any,
            **kwargs: Any
    ):
        self.model = model
        self.async_session_maker = async_session_maker

    @dataclass
    class SelectOptions:
        raiseload: list[Any]
        load_only: Any

    async def get_all(self,
                      include: list[Any] = [],
                      exclude: list[Any] = []) -> Sequence[Any]:
        options = self._get_select_options(include, exclude)
        stmt = select(self.model
                      ).options(*options.raiseload, options.load_only)
        async with self.async_session_maker() as session:
            raw = await session.scalars(stmt)
        result = raw.all()
        return result

    async def get_by_id(self,
                        id: int,
                        include: list[Any] = [],
                        exclude: list[Any] = []) -> Any:
        options = self._get_select_options(include, exclude)
        stmt = select(self.model
                      ).options(*options.raiseload, options.load_only
                                ).filter_by(id=id)
        async with self.async_session_maker() as session:
            with ErrorHandler() as error_handler:
                result = await session.execute(stmt)
                item = result.one()[0]
        return item

    async def get_with_filters(self,
                               include: list[Any] = [],
                               exclude: list[Any] = [],
                               **filters) -> Any:
        # filters = kwargs.get('filters')
        options = self._get_select_options(include, exclude)
        stmt = select(self.model
                      ).options(*options.raiseload, options.load_only
                                ).filter_by(**filters)
        async with self.async_session_maker() as session:
            with ErrorHandler() as error_handler:
                result = await session.execute(stmt)
                item = result.one()[0]
        return item

    async def create(self,
                     data: dict,
                     include: list[Any] = [],
                     exclude: list[Any] = []) -> Any:
        stmt = insert(self.model).returning(self.model)
        async with self.async_session_maker() as session:
            with ErrorHandler():
                result = await session.scalar(stmt, [data])
                await session.commit()
        logger.debug(f"SA crud create statement: {stmt}, data: {data}")
        return result

    async def update(self, id: int, data: dict,
                     include: list[Any] = [],
                     exclude: list[Any] = []) -> int | None:
        stmt = update(self.model).\
            where(self.model.id == id).\
            values(data).\
            returning(self.model.id)
        async with self.async_session_maker() as session:
            item_id = await session.scalar(stmt)
            await session.commit()
        return item_id

    async def delete(self, item_id: int) -> int | None:
        stmt = delete(self.model).\
            where(self.model.id == item_id).\
            returning(self.model.id)
        with ErrorHandler():
            await self.check_exist_by_id(item_id)
        async with self.async_session_maker() as session:
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def check_exist_by_id(self, id):
        query = text(
            f'SELECT * FROM {self.model.__tablename__} WHERE id=:id')
        async with async_session_maker() as session:
            result = await session.execute(query, {'id': id})
        return result.one()

    def _get_select_options(self,
                            include: list[Any] = [],
                            exclude: list[Any] = [],
                            raise_all_relations: bool = True
                            ) -> SelectOptions:
        '''
            If field defined in both exclude and include lists,
                excluding priority
            higher than including. (i.e. excluding more powerful.)
            If any relation included to include list
                and raise_all_relations == True, then all relations raised.
            If include list empty, its equal that all fields included to it.
            If at least one field/relation defined in include list,
                other fields/relations excluded.
            If at least one field/relation defined in exclude list,
                other fields/relations included.
        '''
        all_fields = self.model.as_list()
        pks = self.model.get_pks()
        fks = self.model.get_fks()
        relationships = self.model.get_relationships()
        select_options = self.SelectOptions(raiseload=[], load_only=[])
        if include:
            clean_include = [field for field in include
                             if field not in exclude]
            include = clean_include
        elif not include:
            include = [field for field in all_fields
                       if field not in exclude]
        include_list = [field for field in all_fields if (
            field in include
            and field not in exclude
            and field not in pks
            and field not in fks)]
        include_fields = []
        for field in include_list:
            attr = getattr(self.model, field, None)
            if attr:
                include_fields.append(attr)
        select_options.load_only = load_only(*include_fields)
        if not raise_all_relations:
            for relation in relationships:
                if ((attr := getattr(self.model, relation, False))
                        and (relation in exclude and relation not in include)):
                    select_options.raiseload.append(raiseload(attr))
        else:
            select_options.raiseload.append(raiseload('*'))
        return select_options

    def get_model(self) -> Type[BaseCommon]:
        return self.model
