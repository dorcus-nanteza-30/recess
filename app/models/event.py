from app.extensions import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    # Relationship
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    
    def __init__(self, name, description, date, location):
        self.name = name
        self.description = description
        self.date = date
        self.location = location
        

    def get_event_summary(self):
        return f'Event: {self.name}, Date: {self.date}, Location: {self.location} '
