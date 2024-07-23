from app.extensions import db

class Squad(db.Model):
    __tablename__ = "squads"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    jersey_number = db.Column(db.String(30), unique=True, nullable=False)
    biography = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Numeric(5, 2))
    height = db.Column(db.Numeric(5, 2))
    date_of_birth = db.Column(db.Date)

    # Relationships
    
    player_statistics = db.relationship('PlayerStatistic', backref='squard', lazy=True)
   
    def __init__(self,first_name,last_name,position, jersey_number, biography, image, weight=None, height=None, date_of_birth=None):
        
        
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.jersey_number = jersey_number
        self.biography = biography
        self.image = image
        self.weight = weight
        self.height = height
        self.date_of_birth = date_of_birth

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
