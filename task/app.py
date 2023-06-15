from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    link = db.Column(db.String(100))

    def __init__(self, title, link):
        self.title = title
        self.link = link


@app.route('/')
def index():
    portfolios = Portfolio.query.all()
    return render_template('index.html', portfolios=portfolios)


@app.route('/drop', methods=['GET', 'POST'])
def drop_db():
    if request.method == 'POST':
        db.drop_all()
        db.session.commit()
        dbInit()

    portfolios = Portfolio.query.all()
    return render_template('index.html', portfolios=portfolios)

@app.route('/add', methods=['GET', 'POST'])
def add_portfolio():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        portfolio = Portfolio(title=title, link=link)
        db.session.add(portfolio)
        db.session.commit()
    return render_template('add.html')


def dbInit():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('portfolio'):
            db.create_all()
            print('Таблица "portfolio" создана')
        else:
            print('Таблица "portfolio" уже существует')


if __name__ == '__main__':
    dbInit()
    app.run(debug=True)
