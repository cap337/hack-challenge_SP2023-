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


@app.route("/users/")
def get_all_users():
    users = u.query.all()
    user_list = []
    for user in users:
        user_list.append(user.serialize())
    return success_response({"users": user_list})


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

@app.route("/users/", methods=["GET"])
def verify_user():
    data = json.loads(request.data)
    username = data.get("username")
    password = data.get("password")
    
    if len(u.query.filter_by(username=username,password=password).all()) != 0:
        user = u.query.filter_by(username=username,password=password).all()
        return success_response(user.serialize())
    else:
        return failure_response("user already exist")

@app.route("/users/", methods=["GET"])
def get_user_by_id():
    data = json.loads(request.data)
    id = data.get("id")
    
    if len(u.query.filter_by(id=id)) != 0:
        user = u.query.filter_by(id=id).all()
        return success_response(user.serialize())
    else:
        return failure_response("user already exist")

@app.route("/merch/")
def get_all_merch():
    merches = m.query.all()
    merch_list = []
    for merch in merches:
        merch_list.append(merch.serialize())

    return success_response({"merch": merch_list})


@app.route("/merch/<int:sid>", methods=["POST"])
def add_merch(sid):
    data = json.loads(request.data)
    price = data.get("price")
    description = data.get("description")
    pick_up_time = data.get("pick_up_time")
    pick_up_place = data.get("pick_up_place")
    seller_id = sid

    new_merch = m(
        price=price,
        description=description,
        pick_up_time=pick_up_time,
        pick_up_place=pick_up_place,
        seller_id=seller_id,
    )

    db.session.add(new_merch)
    db.session.commit()

    return success_response(new_merch.serialize())

@app.route("/orders/")
def get_all_orders():
    orders = o.query.all()
    order_list = []
    for order in orders:
        order_list.append(order.serialize())
    return success_response({"orders": order_list})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
