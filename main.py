
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.product import Product
from shema.schemaApp import ProductSchema
from querysApp import QuerysApp
import psycopg2


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

@app.route('/list-product', methods=['GET'])
def listProduct():
    all_products = QuerysApp.get_products_all()
    # obtiene los datos de la base de datos
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/list-product/<id>', methods=['GET'])
def get_persona(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# @app.route('/add-product-posgresql', methods=['GET'])
# def createProduct2():
#     conn = psycopg2.connect(
#     dbname="bd_inventory",
#     user="postgres",
#     password="root",
#     host="localhost",
#     port="5432"
#     )
#     cursor = conn.cursor()
#     query = ''' SELECT *FROM product'''
#     cursor.execute(query)
#     row = cursor.fetchall()
#     print('**********************')
#     print(row)  
#     conn.commit()
#     conn.close()

@app.route('/add-product-posgresql', methods=['POST'])
def createProduct2():
    name = request.json['name']
    description = request.json['description']
    reference = request.json['reference']
    cant = request.json['cant']
    fech_update = request.json['fech_update']
    conn = psycopg2.connect( dbname="bd_inventory", user="postgres", password="root", host="localhost", port="5432" )
    try:
        cursor = conn.cursor()
        query = ''' INSERT INTO product( id, name, description, reference, cant, fech_update) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (10, name, description, reference, cant, fech_update))
        print('Datos insertados')
        conn.commit()
        conn.close()
        return 'OK'
    except:
        print("ERRRRO")
        return 'MAL'





if __name__ == '__main__':
    os.system('cls')
    app.run(debug=True)