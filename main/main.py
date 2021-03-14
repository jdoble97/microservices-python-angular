from flask import Flask, json, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
CORS(app)
db = SQLAlchemy(app)

@dataclass 
class Product(db.Model):
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
    print('dato all:')
    products = Product.query.all()
    # products_Json = jsonify(products) da error por lo que haré lo siguiente para devolver un json al cliente
    mapped_products = map(convertJson, products)
    # Primero se convierte a una lista y después a un json de arrays
    return json.dumps(list(mapped_products))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
