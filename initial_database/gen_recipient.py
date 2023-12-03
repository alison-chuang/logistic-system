from sqlalchemy import insert

from database.models import engine, Recipient
from data import recipients

def generate_recipients():
    with engine.connect() as conn:
        conn.execute(insert(Recipient), recipients)
        conn.commit()

if __name__ == "__main__":
    generate_recipients()
