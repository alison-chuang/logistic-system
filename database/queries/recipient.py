from sqlalchemy import select

from database.models import engine, Recipient

def get_recipient_ids():
    with engine.connect() as conn:
        recipients = select(Recipient.id)
        res = conn.execute(recipients).fetchall()
    return [ id[0] for id in res ]
