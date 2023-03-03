from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from form import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

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
    name = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(20), nullable=False, default='Anything')
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(40), nullable=False, default='All Day')
    price = db.Column(db.Integer, nullable=False, default=0)
    address = db.Column(db.String(40), nullable=False)
    area = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='anything.png')
    map_image = db.Column(db.String(20), nullable=False, default='map.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Event('{self.name}', '{self.category}', '{self.date}', '{self.price}', '{self.address}'," \
               f" '{self.area}', '{self.description}', '{self.image}')"


class EventForm(FlaskForm):
    name = StringField('Namn', validators=[DataRequired(), Length(min=2, max=40)])
    category = StringField('Category')
    date = StringField('Date', validators=[DataRequired(), Length(min=2, max=24)])
    time = StringField('Time', validators=[DataRequired(), Length(min=2, max=40)])
    price = StringField('Price', validators=[DataRequired(), Length(max=16)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=40)])
    area = StringField('Area', validators=[DataRequired(), Length(min=2, max=24)])
    description = TextAreaField('Describe the Event', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submit')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    about = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    created_events = db.relationship('Event', backref='author', lazy=True)
    saved_events = db.relationship('Event', backref='saved', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.lastname}', '{self.description}', '{self.image}')"


"""events = [
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
]"""


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    events = Event.query.all()
    return render_template('index.html', title="Home", events=events)


@app.route("/detail", methods=['GET'])
def detail():
    event = int(request.args["event"])
    return render_template('event-detail-page.html', title="Detail - {{ event.name }}", event=event)


@app.route("/searchresult")
def result():
    return render_template('searchresult.html', title="Search Result")


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


@app.route("/event/add", methods=['GET', 'POST'])
def add_event():
    event = None
    form = EventForm()
    if form.validate_on_submit():
        if event is None:
            event = Event(
                name=form.name.data,
                category=form.category.data,
                date=form.date.data,
                time=form.time.data,
                price=form.price.data,
                address=form.address.data,
                area=form.area.data,
                description=form.description.data
            )
            db.session.add(event)
            db.session.commit()

            form.name.data = '',
            form.category.data = '',
            form.date.data = '',
            form.time.data = '',
            form.price.data = '',
            form.address.data = '',
            form.area.data = '',
            form.description.data = '',
            form.image.data = ''

            flash("Your Event was added Successfully!")

            return redirect(url_for('index'))
    return render_template('postevent.html', title="Add Event", form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
