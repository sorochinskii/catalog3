import datetime
from typing import TYPE_CHECKING

# from source.apps.cartridges.models import Cartridge
from db.models.devices import Device, NetworkDeviceMixin, PolymorphicMixin
from db.models.rooms import Room
from db.models.utils import split_and_concatenate
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.rooms import Room


class MFPNetwork(Device, PolymorphicMixin, NetworkDeviceMixin):

    id: Mapped[int] = mapped_column(ForeignKey('device.id'), primary_key=True)
