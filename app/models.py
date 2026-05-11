from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

OrderProducts = Table(
    "order_products",
    Base.metadata,
    Column(
        "order_id",
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(100), nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        secondary=OrderProducts,
        back_populates="products",
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clients.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float)

    client: Mapped[Client] = relationship(
        Client,
        back_populates="orders",
    )

    products: Mapped[list[Product]] = relationship(
        Product,
        secondary=OrderProducts,
        back_populates="orders",
    )
