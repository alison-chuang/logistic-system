from sqlalchemy import select

from database.models import engine, Location, Order
from database.queries.location import get_location_ids
from data_util import generate_tracking_statuses

statuses = [
    "Created", 
    "Package Received", 
    "In Transit", 
    "Out for Delivery", 
    "Delivery Attempted", 
    "Delivered", 
    "Returned to Sender", 
    "Exception",
]

def get_order_snos():
    with engine.connect() as conn:
        res = conn.execute(select(Order.sno)).fetchall()
    return [ sno[0] for sno in res ]

if __name__ == '__main__':
    order_snos = get_order_snos()
    location_ids = get_location_ids()
    for order_sno in order_snos:
        generate_tracking_statuses(order_sno, location_ids)
