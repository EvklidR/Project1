import datetime

from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, validates
import enum
from typing import Annotated

from model.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
idcomp = Annotated[int, mapped_column(ForeignKey('company.id', ondelete="CASCADE"), nullable=False)]


class TypeOfOrganization(enum.Enum):
    IP = 'ИП'
    OAO = 'ОАО'
    OOO = 'ООО'
    ZAO = 'ЗАО'


class StatusOfReturn(enum.Enum):
    in_request = "Подана заявка"
    request_rejected = "Заявка отклонена"
    request_approved = "Заявка одобрена"
    done = "Товар возвращен"


class TypeOfStore(enum.Enum):
    Opt = "Оптовый склад"
    Rosn = "Розничный магазин"


class Unit(enum.Enum):
    metr = 'м'
    col = 'шт'
    litr = 'л'
    kilo = 'кг'


class GroupOfProducts(Base):
    __tablename__ = "groupOfProducts"

    id: Mapped[intpk]
    name: Mapped[str]
    idCompany: Mapped[idcomp]


class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    data_licvid: Mapped[int]
    name: Mapped[str]
    type: Mapped[int] = mapped_column(ForeignKey('groupOfProducts.id', ondelete="CASCADE"))
    unit: Mapped[Unit]
    idCompany: Mapped[idcomp]


class ProductOnStore(Base):
    __tablename__ = "productonstore"

    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    idStore: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True)
    amount: Mapped[int] = mapped_column(default=0)


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[TypeOfStore]
    idCompany: Mapped[idcomp]


class Company(Base):
    __tablename__ = "company"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[TypeOfOrganization]
    address: Mapped[str]
    email: Mapped[str]


class Operation:
    id: Mapped[intpk]
    idCompany: Mapped[int] = mapped_column(ForeignKey('company.id', ondelete="CASCADE"))
    idWorker: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    idStore: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    date: Mapped[str]


class InfoAboutSale(Base):
    __tablename__ = "infoAboutSale"

    id: Mapped[intpk]
    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    idSale: Mapped[int] = mapped_column(ForeignKey("sale.id", ondelete="CASCADE"))
    amount: Mapped[int]
    cost: Mapped[int] = mapped_column(nullable=True)


class InfoAboutBuy(Base):
    __tablename__ = "infoAboutBuy"

    id: Mapped[intpk]
    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    idBuy: Mapped[int] = mapped_column(ForeignKey("buy.id", ondelete="CASCADE"))
    amount: Mapped[int]
    cost: Mapped[int] = mapped_column(nullable=True)


class Sale(Operation, Base):
    __tablename__ = "sale"



class Buy(Operation, Base):
    __tablename__ = "buy"



class Return(Operation, Base):
    __tablename__ = "return"

    idSale: Mapped[int] = mapped_column(ForeignKey("sale.id", ondelete="CASCADE"))
    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    amount: Mapped[int]
    cost: Mapped[int]
    status: Mapped[StatusOfReturn] = mapped_column(default=StatusOfReturn.in_request)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Displacement(Operation, Base):
    __tablename__ = "displacement"

    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    idStoreToMove: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    amount: Mapped[int]

#
# class Inventory(Operation, Base):
#     __tablename__ = "inventory"
#
#
# class InfoAboutInventory(Base):
#     __tablename__ = "infoAboutInventory"
#
#     id: Mapped[intpk]
#     idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
#     idInventory: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
#     expectedAmount: Mapped[int]
#     amountAtFact: Mapped[int]
