import random
from sqlalchemy import insert

from database.models import engine, Order
from database.queries.recipient import get_recipient_ids

def generate_orders(num=10):
    orders = []
    recipient_ids = get_recipient_ids()
    for _ in range(num):
        orders.append({
            "recipient_id": random.choice(recipient_ids)
        })
    with engine.connect() as conn:
        res = conn.execute(insert(Order), orders)
        conn.commit()

    if num == 1:
        return res.inserted_primary_key[0]
