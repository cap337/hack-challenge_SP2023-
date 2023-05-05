from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class merch(db.Model):


    __tablename__ = "merch"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable  = False)
    pick_up_time  = db.Column(db.String, nullable  = False)
    pick_up_place  = db.Column(db.String, nullable  = False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, **kwargs): 
        self.price = kwargs.get("price")
        self.description = kwargs.get("description")
        self.pick_up_time = kwargs.get("pick_up_time")
        self.pick_up_place = kwargs.get("pick_up_place")
        self.seller_id = kwargs.get("seller_id")

    def serialize(self):
        x = {
            "id": self.id,
            "price":self.price,
            "description":self.description,
            "pick_up_time":self.pick_up_time,
            "pick_up_place":self.pick_up_place,
            "seller_id":self.seller_id
        }
        return x 

    


    




class user(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False)
    hashed_password = db.Column(db.String, nullable = False)


    def __init__(self, **kwargs):
        self.username =kwargs.get("username")


    def serialize(self):
        return {"username":self.username}




class order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    buyer_notes = db.Column(db.String, nullable = False)
    item_amount = db.Column(db.Integer, nullable = False)
    picked_up = db.Column(db.Boolean, nullable = False)
    payment_received =  db.Column(db.Boolean, nullable = False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id") ,nullable  = False)
    
    


    def __init__(self, **kwargs): 
        self.buyer_notes = kwargs.get("buyer_notes")
        self.item_amount = kwargs.get("item_amount")
        self.picked_up = kwargs.get("picked_up")
        self.payment_received  = kwargs.get("payment_received")


