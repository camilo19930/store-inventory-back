
import os
from flask_cors import CORS
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.product import Product
from shema.schemaApp import ProductSchema
from querysApp import QuerysApp
import psycopg2


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# db = SQLAlchemy(app)        # Devuele instancia de base de datos
global conn
conn = psycopg2.connect( dbname="bd_inventory", user="postgres", password="root", host="localhost", port="5432" )
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/bd_inventory"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)        # Devuele instancia de base de datos
db.create_all()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/add-product', methods=['POST'])
def createProduct():
    name = request.json['name']
    description = request.json['description']
    reference = request.json['reference']
    cant = request.json['cant']
    fech_update = request.json['fech_update']

    new_product = Product(None, name, description, reference, cant, fech_update)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/list-product', methods=['GET'])
def listProduct():
    all_products = QuerysApp.get_products_all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>', methods=['PUT'])
def product_update(id):
    name = request.json['name']
    description = request.json['description']
    reference = request.json['reference']
    cant = request.json['cant']
    fech_update = request.json['fech_update']

    update_product = Product(None, name, description, reference, cant, fech_update)
    cursor = conn.cursor()
    query = ''' UPDATE product SET id=%s, name=%s, description=%s, reference=%s, cant=%s, fech_update=%s WHERE id=%s'''
    cursor.execute(query, (id, name, description, reference, cant, fech_update, id))
    conn.commit()
    return product_schema.jsonify(update_product)

@app.route('/delete-product/<id>', methods=['DELETE'])
def delete_product(id):
    print(f'El id es: {id}')
    cursor = conn.cursor()
    query = '''DELETE FROM public.product WHERE id=%s'''
    cursor.execute(query, (id))
    # ((product_schema), each['id'])
    conn.commit()
    conn.close()
    return {'message': f'Producto con id {id} fue eliminado con exito'}



if __name__ == '__main__':
    os.system('cls')
    app.run(debug=True)