from enum import Enum
from typing import Any, Callable, Type

from crud_db_v1.sa_crud import CRUDSA
from exceptions.http_exceptions import (
    HttpExceptionsHandler,
    HTTPObjectNotExist,
    HTTPUniqueException,
)
from exceptions.sa_handler_manager import ItemNotUnique
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from loguru import logger
from schemas.base import BaseSchema


class RouterGenerator(APIRouter):
    def __init__(
        self,
        db_crud: CRUDSA,
        schema_basic_out: Type[BaseSchema],
        schema_basic_in: Type[BaseSchema] | None = None,
        schema_in: Type[BaseSchema] | None = None,
        schema_out: Type[BaseSchema] | None = None,
        schema_create: Type[BaseSchema] | None = None,
        schema_update: Type[BaseSchema] | None = None,
        prefix: str = '',
        tags: list[str | Enum] = [''],
        route_get_all: bool = False,
        route_get_by_id: bool = False,
        route_create: bool = False,
        route_update: bool = False,
        route_delete: bool = False,
        deps_route_get_all: list[Depends] = [],
        deps_route_get_by_id: list[Depends] = [],
        deps_route_create: list[Depends] = [],
        deps_route_update: list[Depends] = [],
        deps_route_delete: list[Depends] = [],
        *args, **kwargs
    ) -> None:
        self.db_model = db_crud.get_model()
        self.db_crud = db_crud
        self.schema_basic_in = schema_basic_in
        self.schema_basic_out = schema_basic_out
        self.schema_in = schema_in
        self.schema_out = schema_out
        self.schema_create = schema_create
        self.schema_update = schema_update

        super().__init__(prefix=prefix, tags=tags, )
        # self._pk = inspect(self.db_model).mapper.primary_key
        if route_get_all:
            self._add_api_route(
                '',
                endpoint=self._get_all(),
                methods=["GET"],
                response_model=list[self.schema_basic_out] | None,
                summary="Get all",
                dependencies=deps_route_get_all)

        if route_get_by_id:
            self._add_api_route(
                '/{item_id}/',
                endpoint=self._get_by_id(),
                methods=["GET"],
                response_model=self.schema_basic_out,
                summary="Get by id",
                dependencies=deps_route_get_by_id)

        if route_create:
            self._add_api_route(
                '',
                endpoint=self._create(),
                methods=["POST"],
                response_model=self.schema_basic_out,
                summary="Create",
                dependencies=deps_route_create)

        if route_update:
            self._add_api_route(
                '',
                endpoint=self._update(),
                methods=["PATCH"],
                response_model=self.schema_in,
                summary="Update",
                dependencies=deps_route_update)

        if route_delete:
            self._add_api_route(
                '/{item_id}/',
                endpoint=self._delete(),
                methods=["DELETE"],
                response_model=self.schema_in,
                summary="Delete item",
                dependencies=deps_route_delete)

    def _add_api_route(
        self,
        path,
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

    def _get_by_id(self) -> Callable:
        async def endpoint(item_id: int):
            include_fields = self.schema_basic_out.model_fields
            with HttpExceptionsHandler():
                result = await self.db_crud.get_by_id(item_id,
                                                      include=include_fields)
            return result
        return endpoint

    def _create(self) -> Callable:
        async def endpoint(
                data: self.schema_create = Body()
        ) -> self.schema_basic_out:
            try:
                logger.debug('Create endpoint. Data', data.dict())
                response: int = await self.db_crud.create(data=data.dict())
                return response
            except ItemNotUnique:
                raise HTTPUniqueException
        return endpoint

    def _update(self) -> Callable:
        async def endpoint(id: int, data: self.schema_update = Body()):
            data = jsonable_encoder(data)
            result = await self.db_crud.update(id, data)
            if not result:
                raise HTTPObjectNotExist
            return result
        return endpoint

    def _delete(self) -> Callable:
        async def endpoint(item_id: int) -> int | None:
            with HttpExceptionsHandler():
                result = await self.db_crud.delete(item_id)
            return result
        return endpoint
