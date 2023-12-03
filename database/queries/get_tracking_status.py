import traceback
import json

from sqlalchemy import text
from database.models import engine, redis_conn

def get_tracking_status(order_sno):
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT
                    ts.id AS tracking_status_id,
                    ts.created_at AS tracking_status_create_at,
                    ts.tracking_status AS tracking_status_tracking_status,
                    ts.location_id AS tracking_status_location_id,
                    location.title AS location_title,
                    location.address AS location_address,
                    recipient.*
                FROM
                    tracking_status ts
                JOIN location ON ts.location_id = location.id
                JOIN `order` ON ts.order_sno = order.sno
                JOIN recipient ON order.recipient_id = recipient.id
                WHERE ts.order_sno = :order_sno;
            """)

            results = conn.execute(query, {"order_sno": order_sno}).fetchall()
            print(results)

            if results:
                details = [
                    {
                        "id": result.tracking_status_id,
                        "date": result.tracking_status_create_at.strftime("%Y-%m-%d"),
                        "status": result.tracking_status_tracking_status,
                        "location_id": result.tracking_status_location_id,
                        "location_title": result.location_title
                    }
                    for result in results
                ]

                response_data = {
                    "sno": order_sno,
                    "tracking_status": results[-1].tracking_status_tracking_status,
                    "estimated_delivery": results[-1].tracking_status_create_at.strftime("%Y-%m-%d"),
                    "details": details,
                    "recipient": {
                        "id": results[-1].id,
                        "name": results[-1].name,
                        "address": results[-1].address,
                        "phone": results[-1].phone
                    },
                    "current_location": {
                        "location_id": results[-1].tracking_status_location_id,
                        "title": results[-1].location_title,
                        "address": results[-1].location_address
                    }
                }

                # set cache
                redis_conn.setex(response_data["sno"], 14400, json.dumps(response_data))

                return {"status": "success", "data": response_data, "error": None}, 200
            return {"status": "error", "data": None, "error": { "code": 404, "message": "Tracking number not found"}}, 404

    except Exception as e:
        print(traceback.format_exc())
        return {"status": "error", "data": None, "error": { "code": 500, "message": str(e)}}, 500
