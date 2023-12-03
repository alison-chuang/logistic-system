import json
import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from database.models import redis_conn
from database.queries.get_tracking_status import get_tracking_status
from database.queries.location import get_location_ids
from database.queries.order import generate_orders
from data_util import generate_tracking_statuses

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/')
def check():
    return 'OK'


@app.route('/fake', methods=['GET'])
def fake():
    """
    generate sno & tracking_status data. /fake?num={ }
    """
    num = int(request.args.get('num', 10))
    num = 100 if num > 100 else num
    locations = get_location_ids()
    res = []
    for _ in range(num):
        order_sno = generate_orders(1)
        tracking_statuses = generate_tracking_statuses(order_sno, locations)
        res.append({"sno": order_sno, "details": tracking_statuses, "tracking_status": tracking_statuses[-1]})
    return jsonify({"data": res}), 200


@app.route('/query', methods=['GET'])
def query_tracking_status():
    """
    Query shipping status by sno. /query?sno={ }
    """
    order_sno = request.args.get('sno')
    if order_sno is None:
        return jsonify({
            "status": "error", 
            "data": None, 
            "error": "Order sno is required"
        }), 400

    result = redis_conn.get(order_sno)
    if result:
        return json.loads(result)
    return get_tracking_status(order_sno)


if __name__ == '__main__':
    app.run(debug=os.getenv("IS_DEBUG_MODE"), port=os.getenv("PORT"))
