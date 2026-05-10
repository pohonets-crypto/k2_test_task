from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Product, Client, Order
from app.schemas import ClientRead, ClientCreate, ProductRead, ProductCreate, OrderRead, OrderCreate

app = FastAPI()

router = APIRouter()

app.include_router(router)


@app.post("/clients", response_model=ClientRead)
async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    new_client = Client(client_name=client.client_name)
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)

    stmt = select(Client).where(Client.id == new_client.id).options(selectinload(Client.orders))
    result = await db.execute(stmt)
    new_client = result.scalar_one()

    return new_client


@app.post("/products", response_model=ProductRead)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(product_name=product.product_name, price=product.price)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


@app.get("/products", response_model=List[ProductRead])
async def products_list(db: AsyncSession = Depends(get_db)):
    stmt = select(Product)
    result = await db.execute(stmt)

    products = result.scalars().all()

    return products


@app.post("/orders", response_model=OrderRead)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    client = await db.get(Client, order_data.client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    stmt = select(Product).where(Product.id.in_(order_data.product_id))
    result = await db.execute(stmt)
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="Order must contain at least 1 product")

    amount = sum([product.price for product in products])

    order = Order(
        client_id=client.id,
        amount=amount,
        products=products,
    )

    db.add(order)
    await db.commit()

    stmt = select(Order).where(Order.id == order.id).options(selectinload(Order.products))
    result = await db.execute(stmt)
    order = result.scalar_one()

    return order


@app.get("/order", response_model=List[OrderRead])
async def get_order_by_client_id(client_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Order).where(Order.client_id == client_id).options(selectinload(Order.products))
    result = await db.execute(stmt)

    orders = result.scalars().all()

    return orders
