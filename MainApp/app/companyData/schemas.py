import datetime
from datetime import date
from typing import Optional

from pydantic import BaseModel
from app.companyData.models import TypeOfOrganization, Unit, TypeOfStore, StatusOfReturn


class Product(BaseModel):
    id: int
    data_licvid: int
    name: str
    type: int
    unit: Unit
    idCompany: int


class ProductUpdate(BaseModel):
    id: int
    data_licvid: int
    name: str
    type: str
    unit: Unit
    idCompany: Optional[int]


class ProductCreate(BaseModel):
    data_licvid: int
    name: str
    type: str
    unit: Unit
    idCompany: Optional[int]


class GroupOfProducts(BaseModel):
    id: int
    name: str
    idCompany: int


class GroupUpdate(BaseModel):
    id: int
    name: str
    idCompany: Optional[int]


class GroupCreate(BaseModel):
    name: str
    idCompany: Optional[int]


class Store(BaseModel):
    id: int
    name: str
    idCompany: int
    type: TypeOfStore


class StoreCreate(BaseModel):
    name: str
    type: TypeOfStore
    idCompany: Optional[int]

class StoreUpdate(BaseModel):
    id: int
    name: str
    type: TypeOfStore
    idCompany: Optional[int]

class Company(BaseModel):
    name: str
    type: TypeOfOrganization
    address: str
    email: str


class Sale(BaseModel):
    id: int
    idCompany: int
    idWorker: int
    created_at: datetime.datetime
    idStore: int
    date: str


class SaleCreate(BaseModel):
    idCompany: Optional[int]
    idWorker: Optional[int]
    created_at: Optional[datetime.datetime]
    idStore: int
    date: str


class Buy(BaseModel):
    id: int
    idCompany: int
    idWorker: int
    created_at: str
    idStore: int
    date: str


class BuyCreate(BaseModel):
    idCompany: Optional[int]
    idWorker: Optional[int]
    created_at: Optional[str]
    idStore: int
    date: str


class Return(BaseModel):
    id: int
    idCompany: int
    idWorker: int
    created_at: str
    idStore: int
    idProduct: int
    date: str
    idSale: int
    amount: int
    cost: int
    status: StatusOfReturn


class ReturnCreate(BaseModel):
    idCompany: Optional[int]
    idWorker: Optional[int]
    created_at: Optional[str]
    idStore: int
    idProduct: int
    date: Optional[str]
    idSale: int
    amount: int
    cost: int


# class Inventory(BaseModel):
#     id: int
#     idCompany: int
#     idWorker: int
#     created_at: str
#     idStore: int
#     date: str
#
#
# class InventoryCreate(BaseModel):
#     idCompany: Optional[int]
#     idWorker: Optional[int]
#     created_at: Optional[str]
#     idStore: int
#     date: str


class Displacement(BaseModel):
    id: int
    idCompany: int
    idWorker: int
    created_at: str
    idStore: int
    date: str
    idProduct: int
    idStoreToMove: int
    amount: int


class DisplacementCreate(BaseModel):
    idCompany: Optional[int]
    idWorker: Optional[int]
    created_at: Optional[str]
    idStore: int
    date: str
    idProduct: int
    idStoreToMove: int
    amount: int
