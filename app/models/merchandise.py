from app.extensions import db

class Merchandise(db.Model):
    __tablename__ = "merchandises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(30), nullable=False)

    # relationships
    order_items = db.relationship("OrderItem", back_populates="merchandise")
    

    def __init__(self, name, description, price, stock, image, category):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.category = category

    def get_item_summary(self):
        return f'Item: {self.name}, Price: ${self.price:.2f}'
