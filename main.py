from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# from main import app, db
# app.app_context().push()
# db.create_all()
# db.drop_all()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False, default='Anything')
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    adress = db.Column(db.String(40), nullable=False)
    area = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='anything.png')
    map_image = db.Column(db.String(20), nullable=False, default='map.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.name}', '{self.category}', '{self.date}', '{self.price}', '{self.adress}'," \
               f" '{self.area}', '{self.description}', '{self.image}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    created_events = db.relationship('Event', backref='author', lazy=True)
    saved_events = db.relationship('Event', backref='saved', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.lastname}', '{self.description}', '{self.image}')"


events = [
    {"name": "Morsans Loppis", "category": "Second Hand", "date": "01.04.2023", "tid": "10-16", "price": "Free",
     "adress": "Storgatan 50", "area": "Gamla Stan",
     "image": "/static/images/second-hand.png",
     "description": "Kom till min Loppis i Gamla Stan! Här finnes allt mellan himmel och jord till fantastiska priser"},
    {"name": "Sagostund", "category": "Family", "date": "10.04.2023", "tid": "14-15", "price": "Free",
     "adress": "Bygatan 10", "area": "Biblioteket",
     "image": "/static/images/family.png",
     "description": "Bibi läser Pippi Långstrump för de minsta. Ålder: 0-1"},
    {"name": "Stor Bandet Spelar", "category": "Concert", "date": "27.03.23", "tid": "22-01", "price": "100",
     "adress": "Avenyn 5", "area": "Stora nattklubben",
     "image": "/static/images/music.png",
     "description": "Stora Bandet spelar allt från covers till egen musik inom pop, rock, jazz, och dansbandsmusik. "
                    "Välkommen till en svängig kväll!"},
    {"name": "Hemma laget möter Borta laget", "category": "Sport", "date": "03.04.2023", "tid": "16-20", "price": "50",
     "adress": "Sportgatan 25", "area": "City Arena",
     "image": "/static/images/sport.png",
     "description": "Final match! Var med att kora årets mästare i året pirrigast final."}

]
event = [{"name": "Stor Bandet Spelar", "category": "Concert", "date": "27.03.23", "tid": "22-01", "price": "100",
         "adress": "Avenyn 5", "area": "Stora nattklubben",
         "image": "/static/images/music.png",
         "description": "Stora Bandet spelar allt från covers till egen musik inom pop, rock, jazz, och "
                        "dansbandsmusik. Välkommen till en svängig kväll!"}
]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # img_file = url_for('static', filename='images/whatsup-vertical.png')
    # , img_file=img_file
    return render_template('index.html', title="Home", events=events)


@app.route("/detail")
def detail():
    #event = int(request.args["event"])
    #title = events[event]["name"]

    return render_template('event-detail-page.html', title="Detail", event=event)


@app.route("/searchresult")
def result():
    return render_template('searchresult.html', title="Search Result", events=events)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('register.html', title="Sign in", form=form)

# Log in form route. From register
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)


@app.route("/postevent")
def postevent():
    return render_template('postevent.html', title="Post Event")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
