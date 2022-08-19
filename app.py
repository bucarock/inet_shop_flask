from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    opisanie = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    items = Item.query.order_by(Item.price).all()
    return render_template('catalog.html', data=items)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        opisanie = request.form['opisanie']
        item = Item(title=title, price=price, opisanie=opisanie)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/catalog')
        except:
            return "Произошла ошибка. попробуйте снова."
    else:
        return render_template('create.html')

@app.route('/oplata/<int:id>')
def oplata(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)