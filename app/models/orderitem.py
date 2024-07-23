from app.extensions import db

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    merchandise_id = db.Column(db.Integer, db.ForeignKey("merchandises.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_of_item = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    # relationships
    order = db.relationship("Order", back_populates="order_items")
    merchandise = db.relationship("Merchandise", back_populates="order_items")

    def __init__(self, order_id, merchandise_id, quantity, price_of_item):
        self.order_id = order_id
        self.merchandise_id = merchandise_id
        self.quantity = quantity
        self.price_of_item = price_of_item
        self.total_amount = quantity * price_of_item

    def get_total_price(self):
        return f'Total Price: ${self.total_amount:.2f}'
