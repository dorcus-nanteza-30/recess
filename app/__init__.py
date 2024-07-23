from flask import Flask
from app.extensions import db, migrate,bcrypt,jwt


def create_app():

     app =  Flask(__name__)
     app.config.from_object('config.config')


     db.init_app(app)
     migrate.init_app(app, db)
     bcrypt.init_app(app)
     jwt.init_app(app)

    #importing models
     from app.models import user
     from app.models import ticket
     from app.models import squad
     from app.models import playerstatistics
     from app.models import orderitem
     from app.models import order
     from app.models import merchandise
     #from app.models import membership
     from app.models import event
     from app.models import donation
     from app.models import contact

     

     #registering blueprints
     from app.controllers.user_controller import user_bp
     app.register_blueprint(user_bp)
     from app.controllers.squad_controller import squad_bp
     app.register_blueprint(squad_bp)
     from app.controllers.playerstatistics_controller import playerstatistics_bp
     app.register_blueprint(playerstatistics_bp)
     from app.controllers.contact_controller import contact_bp
     app.register_blueprint(contact_bp)
     from app.controllers.donation_controller import donation_bp
     app.register_blueprint(donation_bp)
     from app.controllers.merchandise_controller import merchandise_bp
     app.register_blueprint(merchandise_bp)
     from app.controllers.orderitem_controller import orderitem_bp
     app.register_blueprint(orderitem_bp)
     from app.controllers.order_controller import order_bp
     app.register_blueprint(order_bp)
     from app.controllers.event_controller import event_bp
     app.register_blueprint(event_bp)
     from app.controllers.ticket_controller import ticket_bp
     app.register_blueprint(ticket_bp)


    
     

     @app.route("/") 
     def home():
         return "Website Api"


     return app 

 
