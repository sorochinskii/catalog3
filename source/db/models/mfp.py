from typing import TYPE_CHECKING, Any

# from source.apps.cartridges.models import Cartridge
from db.models.devices import Device, NetworkDeviceMixin, PolymorphicMixin
from db.models.rooms import Room
from db.models.utils import split_and_concatenate
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .printers import Printer


class MFPNetwork(Device, NetworkDeviceMixin):

    # id: Mapped[int] = mapped_column(ForeignKey('device.id'), primary_key=True)

    @ declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        return {
            'polymorphic_identity': 'mfp_network'
        }


class MFP(Printer):

    @ declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        return {
            'polymorphic_identity': 'mfp'
        }
