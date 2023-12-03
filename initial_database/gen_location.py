from sqlalchemy import insert

from database.models import engine, Location
from data import locations

def generate_locations():
    with engine.connect() as conn:
        conn.execute(insert(Location), locations)
        conn.commit()

if __name__ == "__main__":
    generate_locations()
