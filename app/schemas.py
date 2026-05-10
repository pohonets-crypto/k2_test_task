from typing import List

from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    client_name: str = Field(..., max_length=100)


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    orders: List["OrderRead"]

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    product_name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    client_id: int = Field(..., gt=0)
    product_id: List[int] = Field(..., min_items=1)


class OrderRead(BaseModel):
    id: int
    client_id: int
    products: List[ProductRead]
    amount: float

    class Config:
        from_attributes = True
