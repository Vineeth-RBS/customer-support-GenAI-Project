from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env so we can get DATABASE_URI

Base = declarative_base()

# ---- Define our database tables ---- #

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(15))

    orders = relationship("Order", back_populates="customer")
    tickets = relationship("Ticket", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_name = Column(String(100))
    order_status = Column(String(50))
    expected_delivery = Column(Date)
    last_updated = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")
    tickets = relationship("Ticket", back_populates="order")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    issue = Column(String(255))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="tickets")
    order = relationship("Order", back_populates="tickets")


# ---- Helper to create engine and session ---- #

def get_engine_and_session():
    db_uri = os.getenv("DATABASE_URI")
    engine = create_engine(db_uri, echo=True, future=True)
    Session = sessionmaker(bind=engine, autoflush=False, future=True)
    return engine, Session
