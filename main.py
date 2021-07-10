
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.product import Product
from shema.schemaApp import ProductSchema


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)        # Devuele instancia de base de datos
# Lee toda la clase y procede a crear la tabla
db.create_all()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/inventory_bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/add-product', methods=['POST'])
def createProduct():
    name = request.json['name']
    description = request.json['description']
    reference = request.json['reference']
    cant = request.json['cant']
    fech_update = request.json['fech_update']

    new_product = Product(name, description, reference, cant, fech_update)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


if __name__ == '__main__':
    os.system('cls')
    app.run(debug=True)