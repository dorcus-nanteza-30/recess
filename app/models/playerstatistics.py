from app.extensions import db

class PlayerStatistic(db.Model):
    __tablename__ = "playerstatistics"
    
    id = db.Column(db.Integer, primary_key=True)
    squad_id = db.Column(db.Integer, db.ForeignKey("squads.id"), nullable=False)
    matches_played = db.Column(db.Integer, nullable=False)
    tries_scored = db.Column(db.Integer, nullable=False)
    conversions = db.Column(db.Integer, nullable=False)
    penalties = db.Column(db.Integer, nullable=False)
    yellow_cards = db.Column(db.Integer, nullable=False)
    red_cards = db.Column(db.Integer, nullable=False)
    minutes_played = db.Column(db.Integer, nullable=False)
    
    
    def __init__(self, squad_id, matches_played, tries_scored=0, conversions=0, penalties=0, yellow_cards=0, red_cards=0, minutes_played=0):
        self.squad_id = squad_id
        self.matches_played = matches_played
        self.tries_scored = tries_scored
        self.conversions = conversions
        self.penalties = penalties
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.minutes_played = minutes_played

    def __repr__(self):
        return (f'<PlayerStatistic id={self.id}, squad_id={self.squad_id}, '
                f'matches_played={self.matches_played}, tries_scored={self.tries_scored}, '
                f'conversions={self.conversions}, penalties={self.penalties}, '
                f'yellow_cards={self.yellow_cards}, red_cards={self.red_cards}, '
                f'minutes_played={self.minutes_played}>')
