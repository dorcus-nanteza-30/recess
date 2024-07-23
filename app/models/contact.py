from app.extensions import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  

    # Relationship to User
    user = db.relationship("User", back_populates="contacts")

    def __init__(self, name, email, message,user_id,date=None):
        self.name = name
        self.email = email
        self.message = message
        self.user_id = user_id
        self.date = date or datetime.utcnow()

    def get_contact_summary(self):
        return f'Name: {self.name}, Email: {self.email}, Message: {self.message}'
