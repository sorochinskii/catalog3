from typing import TYPE_CHECKING, Any

from db.models.cartridges import Model
from db.models.devices import Device, PolymorphicMixin
from db.models.utils import split_and_concatenate
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.cartridges import Cartridge


class Printer(Device):

    cartridge_model_id: Mapped[int | None] = mapped_column(
        ForeignKey('model.id'))
    cartridge_model: Mapped['Model'] = relationship(
        back_populates='printer', foreign_keys=[cartridge_model_id], lazy='joined')

    current_cartridge_id: Mapped[int | None] = mapped_column(
        ForeignKey('cartridge.id'))
    # current_cartridge: Mapped['Cartridge'] = relationship(
    #     back_populates='current_printer', foreign_keys=[current_cartridge_id])

    @ declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        return {
            'polymorphic_abstract': True
        }
