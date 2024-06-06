import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from model.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
idcomp = Annotated[int, mapped_column(ForeignKey('company.id', ondelete="CASCADE"), nullable=False)]


class TypeOfOrganization(enum.Enum):
    IP = 'ИП'
    OAO = 'ОАО'
    OOO = 'ООО'
    ZAO = 'ЗАО'


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


class Company(Base):
    __tablename__ = "company"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[TypeOfOrganization]
    address: Mapped[str]
    email: Mapped[str]


class InfoAboutSale(Base):
    __tablename__ = "infoAboutSale"

    id: Mapped[intpk]
    idProduct: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    idSale: Mapped[int] = mapped_column(ForeignKey("sale.id", ondelete="CASCADE"))
    amount: Mapped[int]
    cost: Mapped[int] = mapped_column(nullable=True)


class Sale(Base):
    __tablename__ = "sale"

    id: Mapped[intpk]
    idCompany: Mapped[int] = mapped_column(ForeignKey('company.id', ondelete="CASCADE"))
    idWorker: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    idStore: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    date: Mapped[str]