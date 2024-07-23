from app.extensions import db
from datetime import datetime

class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100), nullable=False)  # Assuming name is required
    contact = db.Column(db.String(20), nullable=True)  # Assuming contact is optional

    # relationships
    user = db.relationship("User", back_populates="donations")

    def __init__(self, user_id, amount, name, donation_date=None, message=None, contact=None):
        self.user_id = user_id
        self.amount = amount
        self.name = name
        self.donation_date = donation_date or datetime.utcnow()
        self.message = message
        self.contact = contact

    def get_donation_summary(self):
        return f'Donation Amount: ${self.amount:.2f}, Date: {self.donation_date}, Message: {self.message or "No message"}'
