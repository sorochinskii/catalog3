from httpx import AsyncClient
from polyfactory.factories.pydantic_factory import ModelFactory

from source.schemas.vendors import VendorSchema, VendorSchemaOut
from source.schemas.vendors_base import VendorBaseSchema, VendorBaseSchemaOut


class VendorCreateFactory(ModelFactory[VendorBaseSchema]):
    __model__ = VendorSchema


class VendorOutFactory(ModelFactory[VendorBaseSchemaOut]):
    __model__ = VendorBaseSchemaOut


async def test_delete_vendor(test_client: AsyncClient):
    vendor_create = VendorCreateFactory.build()
    data = vendor_create.model_dump()
    vendor = await test_client.post(
        '/v1/vendors', json=data)
    item_id = vendor.json().get('id')
    response = await test_client.delete(f'/v1/vendors/{item_id}/')
    response_id = response.json()
    assert response_id == item_id


async def test_create_vendor(test_client: AsyncClient):
    vendor_create = VendorCreateFactory.build()
    data = vendor_create.model_dump()
    response = await test_client.post('/v1/vendors', json=data)
    assert response.json().get('name') == data.get('name')
