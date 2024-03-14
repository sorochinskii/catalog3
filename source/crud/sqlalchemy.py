from dataclasses import dataclass
from typing import Any, Callable, TypedDict

from crud.base import CRUD
from sqlalchemy import Session, select
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.orm import MappedClassProtocol, load_only, raiseload

from source.db.db import async_session_maker
from source.db.models.base import Base


class CRUDSA(CRUD):

    def __init__(
            self,
            model: Base,
            session: Session,
            *args: Any,
            **kwargs: Any
    ):
        self.model = model
        self.async_session_maker = async_session_maker

    @dataclass
    class SelectOptions:
        raiseload: list[Callable]
        load_only: Callable

    def get_select_options(self,
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
