from app.extensions import db

class Ticket(db.Model):
    __tablename__ = "tickets"
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Assuming 'events' is the table name
    price = db.Column(db.Float, nullable=False)
    section = db.Column(db.String(50), nullable=False)
    row = db.Column(db.String(50), nullable=False)
    seat = db.Column(db.String(50), nullable=False)
    

    def __init__(self, event_id, price, section, row, seat):
        self.event_id = event_id
        self.price = price
        self.section = section
        self.row = row
        self.seat = seat

    def __repr__(self):
        return f'<Ticket id={self.id}, event_id={self.event_id}, section="{self.section}", row="{self.row}", seat="{self.seat}", price={self.price}>'
