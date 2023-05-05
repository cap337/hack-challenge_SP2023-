from db import db
from flask import Flask
import json
from flask import request
from db import merch as m
from db import user as u
from db import order as o

app = Flask(__name__)
db_filename = "merch.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=400):
    return json.dumps({"error": message}), code


@app.route("/")
def hello():
    return success_response({"hello": "world"})


"""
user routes
"""


@app.route("/users/", methods=["GET"])
def get_user():
    try:
        data = json.loads(request.data)
    except:
        # get all users
        users = u.query.all()
        user_list = []
        for user in users:
            user_list.append(user.serialize())
        return success_response({"users": user_list})

    username = data.get("username")
    password = data.get("password")
    id = data.get("id")

    # verify user
    if username is not None and password is not None:
        user = u.query.filter_by(username=username, password=password).first()
        if user is None:
            return failure_response("verification failed")
        return success_response(user.serialize())

    # get user by id
    if id is not None:
        user = u.query.filter_by(id=id).first()
        if user is None:
            return failure_response("user not found")
        return success_response(user.serialize())

    return failure_response("bad user GETrequest")


@app.route("/users/", methods=["POST"])
def create_user():
    data = json.loads(request.data)
    username = data.get("username")
    password = data.get("password")
    if len(u.query.filter_by(username=username).all()) != 0:
        return failure_response("user already exist")
    else:
        new_user = u(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
    return success_response(new_user.serialize())


"""
merch routes
"""


@app.route("/merch/", methods=["GET"])
def get_all_merch():
    try:
        data = json.loads(request.data)
    except:
        merches = m.query.all()
        merch_list = []
        for merch in merches:
            merch_list.append(merch.serialize())
        return success_response({"merch": merch_list})

    merch_id = data.get("merch_id")
    seller_id = data.get("seller_id")

    # get one merch by merch_id
    if merch_id is not None:
        merch = m.query.filter_by(id=merch_id).first()
        if merch is None:
            return failure_response("merch not found")
        return success_response(merch.serialize())

    if seller_id is not None:
        merch = m.query.filter_by(seller_id=seller_id).all()
        if merch is None:
            return failure_response("no merch is sold by the seller")
        merch_list = []
        for me in merch:
            merch_list.append(me.serialize())
        return success_response({"merch": merch_list})

    return failure_response("bad merch GETrequest")


@app.route("/merch/", methods=["POST"])
def create_merch():
    data = json.loads(request.data)

    price = data.get("price")
    name = data.get("name")
    general_type = data.get("general_type")
    description = data.get("description")
    pick_up_time = data.get("pick_up_time")
    pick_up_place = data.get("pick_up_place")
    seller_id = data.get("seller_id")

    new_merch = m(
        price=price,
        name=name,
        general_type=general_type,
        description=description,
        pick_up_time=pick_up_time,
        pick_up_place=pick_up_place,
        seller_id=seller_id,
    )

    db.session.add(new_merch)
    db.session.commit()

    return success_response(new_merch.serialize())


"""
order routes
"""


@app.route("/orders/")
def get_all_orders():
    orders = o.query.all()
    order_list = []
    for order in orders:
        order_list.append(order.serialize())
    return success_response({"orders": order_list})


@app.route("/orders/", methods=["POST"])
def create_order():
    data = json.loads(request.data)
    merch_id = data.get("merch_id")
    buyer_id = data.get("buyer_id")
    buyer_notes = data.get("buyer_notes")
    item_amount = data.get("item_amount")
    if (
        merch_id is None
        or buyer_id is None
        or buyer_notes is None
        or item_amount is None
    ):
        return failure_response("malformed json body")

    new_order = o(
        merch_id=merch_id,
        buyer_id=buyer_id,
        buyer_notes=buyer_notes,
        item_amount=item_amount,
        payment_received=False,
        picked_up=False,
    )
    db.session.add(new_order)
    db.session.commit()
    return success_response(new_order.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
