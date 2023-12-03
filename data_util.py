import random 

from sqlalchemy import insert

from database.models import engine, TrackingStatus
from database.queries.order import generate_orders
from database.queries.location import get_location_ids
from data import sender_statuses, receiver_statuses, EXCEPTION, DELIVERD, RETURNED, IN_TRANSIT

def get_random_number(start=1, end=3):
    return random.randint(start, end)

def exception_happended(threshold=0.05):
    return random.uniform(0, 1) < threshold

def returned_happended(threshold=0.05):
    return random.uniform(0, 1) < threshold

def is_on_the_way(threshold=0.5):
    return random.uniform(0, 1) < threshold

def generate_tracking_statuses(order_sno, location_ids):
    tracking_statuses = []
    in_transit_num = get_random_number()
    sender_loc, receiver_loc, *in_transit_locs = random.sample(location_ids, 2 + in_transit_num)
    for ss in sender_statuses:
        tracking_statuses.append({
            "order_sno": order_sno,
            "tracking_status": ss,
            "location_id": sender_loc
        })

    for t_loc in in_transit_locs:
        if is_exception := exception_happended():
            tracking_statuses.append({
                "order_sno": order_sno,
                "tracking_status": EXCEPTION,
                "location_id": t_loc
            })
            break
        tracking_statuses.append({
            "order_sno": order_sno,
            "tracking_status": IN_TRANSIT,
            "location_id": t_loc
        })
        
    if not is_on_the_way():
        if not is_exception:
            for rs in receiver_statuses:
                if is_exception := exception_happended():
                    tracking_statuses.append({
                        "order_sno": order_sno,
                        "tracking_status": EXCEPTION,
                        "location_id": receiver_loc
                    })
                    break
                tracking_statuses.append({
                    "order_sno": order_sno,
                    "tracking_status": rs,
                    "location_id": receiver_loc
                })
        if not is_exception:
            if returned_happended():
                if is_exception := exception_happended():
                    tracking_statuses.append({
                        "order_sno": order_sno,
                        "tracking_status": EXCEPTION,
                        "location_id": sender_loc
                    })
                else:
                    tracking_statuses.append({
                        "order_sno": order_sno,
                        "tracking_status": RETURNED,
                        "location_id": sender_loc
                    })
            else:
                if is_exception := exception_happended():
                    tracking_statuses.append({
                        "order_sno": order_sno,
                        "tracking_status": EXCEPTION,
                        "location_id": receiver_loc
                    })
                else:
                    tracking_statuses.append({
                        "order_sno": order_sno,
                        "tracking_status": DELIVERD,
                        "location_id": receiver_loc
                    })
    with engine.connect() as conn:
        conn.execute(insert(TrackingStatus), tracking_statuses)
        conn.commit()
    return tracking_statuses

if __name__ == "__main__":
    order_sno = generate_orders(1)
    locations = get_location_ids()
    generate_tracking_statuses(order_sno, locations)
