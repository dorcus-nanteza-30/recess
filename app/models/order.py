from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status_of_order = db.Column(db.String(30), nullable=False)
    address_of_delivery = db.Column(db.String(255), nullable=False)

    # relationships
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")

    def __init__(self, user_id, status_of_order, address_of_delivery, order_date=None):
        self.user_id = user_id
        self.status_of_order = status_of_order
        self.address_of_delivery = address_of_delivery
        self.order_date = order_date or datetime.utcnow()

    def get_order_summary(self):
        return f'Order Date: {self.order_date}, Status: {self.status_of_order}, Delivery Address: {self.address_of_delivery}'
