from models import Customer, Order, Ticket, get_engine_and_session, Base
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
engine, Session = get_engine_and_session()
Base.metadata.create_all(bind=engine)

session = Session()

customers = []
orders = []
tickets = []

# Create 50 customers
for _ in range(50):
    c = Customer(
        name=fake.name(),
        email=fake.email(),
        phone="".join([str(random.randint(0,9)) for _ in range(10)])
    )
    customers.append(c)
session.add_all(customers)
session.flush()  # assign IDs

# Create 100 orders randomly assigned to customers
for _ in range(100):
    cust = random.choice(customers)
    o = Order(
        customer_id=cust.id,
        product_name=fake.word().capitalize() + " " + fake.word().capitalize(),
        order_status=random.choice(["Processing", "Shipped", "Delivered", "Cancelled"]),
        expected_delivery=fake.date_between(start_date="today", end_date="+30d"),
        last_updated=fake.date_time_this_month()
    )
    orders.append(o)
session.add_all(orders)
session.flush()

# Create tickets randomly for some orders
for o in random.sample(orders, 50):  # 50 tickets
    t = Ticket(
        customer_id=o.customer_id,
        order_id=o.id,
        issue=random.choice([
            "Delay in delivery", 
            "Wrong item received", 
            "Product damaged", 
            "Missing accessories"
        ]),
        status=random.choice(["Open", "Pending", "Resolved"]),
        created_at=fake.date_time_this_month(),
        updated_at=fake.date_time_this_month()
    )
    tickets.append(t)
session.add_all(tickets)

session.commit()
print("✅ Database seeded with 50 customers, 100 orders, 50 tickets (10-digit phones)!")
