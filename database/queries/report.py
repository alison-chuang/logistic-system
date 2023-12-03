from database.models import engine
from sqlalchemy import text

def count_order_by_status():
    with engine.connect() as conn:
        sql_query = text("""
            SELECT tracking_status, COUNT(*) as order_count
            FROM tracking_status
            JOIN (
                SELECT order_sno, MAX(id) as max_tracking_id
                FROM tracking_status
                GROUP BY order_sno
            ) as latest_status
            ON tracking_status.order_sno = latest_status.order_sno
            AND tracking_status.id = latest_status.max_tracking_id
            GROUP BY tracking_status
        """)

        return conn.execute(sql_query).fetchall()
