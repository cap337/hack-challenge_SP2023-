from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class merch(db.Model):
    __tablename__ = "merch"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    general_type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    pick_up_time = db.Column(db.String, nullable=False)
    pick_up_place = db.Column(db.String, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        self.price = kwargs.get("price")
        self.name = kwargs.get("name")
        self.general_type = kwargs.get("general_type")
        self.description = kwargs.get("description")
        self.pick_up_time = kwargs.get("pick_up_time")
        self.pick_up_place = kwargs.get("pick_up_place")
        self.seller_id = kwargs.get("seller_id")

    def serialize(self):
        x = {
            "id": self.id,
            "sid": self.seller_id,
            "name": self.name,
            "generalType": self.general_type,
            "description": self.description,
            "price": self.price,
            "pickupTime": self.pick_up_time,
            "pickupPlace": self.pick_up_place,
        }
        return x


class user(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

    def serialize(self):
        return {"id": self.id, "username": self.username, "pw":self.password}


class order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_notes = db.Column(db.String, nullable=False)
    item_amount = db.Column(db.Integer, nullable=False)
    picked_up = db.Column(db.Boolean, nullable=False)
    payment_received = db.Column(db.Boolean, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    merch_id = db.Column(db.Integer, db.ForeignKey("merch.id"), nullable=False)

    def __init__(self, **kwargs):
        self.buyer_notes = kwargs.get("buyer_notes")
        self.item_amount = kwargs.get("item_amount")
        self.picked_up = kwargs.get("picked_up")
        self.payment_received = kwargs.get("payment_received")
        self.buyer_id = kwargs.get("buyer_id")
        self.merch_id = kwargs.get("merch_id")

    def serialize(self):
        return {
            "id": self.id,
            "mid": self.merch_id,
            "bid": self.buyer_id,
            "notes": self.buyer_notes,
            "num": self.item_amount,
            "pickedUp": self.picked_up,
            "paid": self.payment_received,
            
        }
