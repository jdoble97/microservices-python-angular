from flask import Flask, json, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
import requests
from producer import publish


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
CORS(app)
db = SQLAlchemy(app)

@dataclass 
class Product(db.Model):
    id:int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def toJson(self):
        return {'id': self.id, 'title': self.title, 'image': self.image}

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


def convertJson(x: Product):
    return x.toJson()


@app.route('/api/products')
def index():
    """
    products = Product.query.all()
    mapped_products = map(convertJson, products)
    Primero se convierte a una lista y después a un json de arrays
    return json.dumps(list(mapped_products))"""
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like',methods=['POST'])
def like(id):
    #docker.for.win.localhost is deprecated
    req = requests.get('http://host.docker.internal:8000/api/user')
    jsonTo=req.json()
    print('id json',jsonTo)
    try:
        productUser = ProductUser(user_id=jsonTo['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id )
    except:
        abort(400,'Ya diste like a este producto')
    # req = requests.get('http://docker.for.win.localhost:8000/api/user')
    return jsonify({
        'message': 'Diste like'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
