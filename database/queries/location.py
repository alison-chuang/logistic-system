from sqlalchemy import insert, select

from database.models import engine, Location
from data import locations

def generate_locations():
    with engine.connect() as conn:
        conn.execute(insert(Location), locations)
        conn.commit()

def get_location_ids():
    with engine.connect() as conn:
        res = conn.execute(select(Location.id)).fetchall()
    return [ id[0] for id in res ]
