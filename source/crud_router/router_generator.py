from collections.abc import Coroutine
from enum import Enum
from typing import Any, Callable, Type
from xml.etree.ElementInclude import include

from crud_db_v1.sqlalchemy import CRUDSA
from db.models.base import BaseCommon
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Depends
from schemas.base import BaseSchema
from sqlalchemy import Sequence, inspect


class RouterGenerator(APIRouter):
    def __init__(
        self,
        db_crud: CRUDSA,
        # db_model: Type[BaseCommon] | None = None,
        schema_basic_in: Type[BaseSchema] | None = None,
        schema_basic_out: Type[BaseSchema] | None = None,
        schema_in: Type[BaseSchema] | None = None,
        schema_out: Type[BaseSchema] | None = None,
        schema_create: Type[BaseSchema] | None = None,
        prefix: str = '',
        tags: list[str | Enum] = [''],
        route_get_all: bool = False,
        route_get_by_id: bool = False,
        deps_route_get_all: list[Depends] = [],
        deps_route_get_by_id: list[Depends] = [],
        *args, **kwargs
    ) -> None:
        self.db_model = db_crud.get_model()
        self.db_crud = db_crud
        self.schema_basic_in = schema_basic_in
        self.schema_basic_out = schema_basic_out
        self.schema_in = schema_in
        self.schema_out = schema_out
        self.schema_create = schema_create
        self.deps_route_get_all = deps_route_get_all
        self.deps_route_get_by_id = deps_route_get_by_id
        self.route_get_all = route_get_all
        self.route_get_by_id = route_get_by_id

        super().__init__(prefix=prefix, tags=tags, )
        self._pk: int = inspect(self.db_model).mapper.primary_key
        if route_get_all:
            self._add_api_route(
                '',
                endpoint=self._get_all(),
                methods=["GET"],
                response_model=list[self.schema_basic_out] | None,
                summary="Get all",
                dependencies=self.deps_route_get_all)

        if route_get_by_id:
            self._add_api_route(
                '',
                endpoint=self._get_by_id(),
                methods=["GET"],
                response_model=self.schema_basic_out,
                summary="Get by id",
                dependencies=self.deps_route_get_by_id)

    def _add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        dependencies: list[Depends] = [],
        error_responses: list[HTTPException] | None = None,
        **kwargs: Any,
    ) -> None:

        super().add_api_route(
            path, endpoint, dependencies=dependencies,
            ** kwargs
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable:
        async def endpoint():
            if self.schema_basic_out:
                include_fields = self.schema_basic_out.model_fields
            else:
                raise Exception('No response model.')
            return await self.db_crud.get_all(include=include_fields)
        return endpoint

    def _get_by_id(self, *args: Any, **kwargs: Any) -> Callable:
        async def endpoint(id: int):
            if self.schema_basic_out:
                include_fields = self.schema_basic_out.model_fields
            else:
                raise Exception('No response model.')
            return await self.db_crud.get_by_id(id, include=include_fields)
        return endpoint
