from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    reference = db.Column(db.Integer)
    cant = db.Column(db.Integer)
    fech_update = db.Column(db.Integer)


    def __init__(self, name, description, reference, cant, fech_update):
        self.name = name
        self.description = description
        self.reference = reference
        self.cant = cant
        self.fech_update = fech_update