from .device import DeviceSchemaOut
from .person_base import PersonBaseSchema


class PersonSchemaOut(PersonBaseSchema):
    devices_responsibility: list[DeviceSchemaOut]
