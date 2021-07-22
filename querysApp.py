from flask_sqlalchemy import SQLAlchemy
from models.product import Product

db = SQLAlchemy()

class QuerysApp():

    def craete_Product(self):
        db.session.add(self)
        db.session.commit()

    def get_products_all():
        return Product.query.all()