import os.path

import wtforms
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from form import RegistrationForm, LoginForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo



app = Flask(__name__)
#app.config['INSTANCE_PATH'] = '/tmp'
app.config['SECRET_KEY'] = '123456'
file_abs_path = os.path.abspath(os.path.dirname(__file__))
# if instance folder exists, use it
if os.path.exists(os.path.join(file_abs_path, 'instance')):
    file_abs_path = os.path.join(file_abs_path, 'instance')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(file_abs_path, 'site.db')}"
db = SQLAlchemy(app)

# from main import app, db
# app.app_context().push()
# db.create_all()
# db.drop_all()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(20), nullable=False, default='Anything')
    date = db.Column(db.Date, nullable=False)
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
    date = DateField('Date', validators=[DataRequired()])
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
    sex = db.Column(db.String(10), nullable=False, default='Female')
    created_events = db.relationship('Event', backref='author', lazy=True)
    saved_events = db.relationship('Event', backref='saved', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}')"

# Create 5 dummy events (of each category: Second Hand, Family, Sport, Music, Anything else)
# if database doesn't contain any for each category of events


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
"""if events is None:
    events = [{
        "name": "This is how it can look",
        "category": "Anything",
        "date": "01.04.2023",
        "time": "10-12",
        "price": "Free",
        "address": "The Street",
        "area": "The Area",
        "description": "This is were you describe your event in detail"}]"""


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    events = Event.query.all()

    return render_template('index.html', title="Home", events=events)


@app.route("/detail", methods=['GET'])
def detail():
    event_id = request.args.get("event")
    event = Event.query.filter_by(id=event_id).first()

    return render_template('event-detail-page.html', title=event.name, event=event)


@app.route("/calendar")
def result():
    events = Event.query.all()

    return render_template('result.html', title="Calendar", events=events)


@app.route("/register", methods=['GET', 'POST'])
def register():
    user = None
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                username=form.username.data,
                password=form.password.data,
                about=form.about.data
            )
            db.session.add(user)
            db.session.commit()

            form.firstname.data = '',
            form.lastname.data = '',
            form.username.data = '',
            form.password.data = '',
            form.about.data = '',
            form.sex.data = ''

            flash("Your Profile was added Successfully!")

        return redirect(url_for('index'))
    return render_template('register.html', title="Sign Up", form=form)


# Log in form route. From register
@app.route("/login")
def login():
    user = None
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            # Flash login fail message
            flash("Login Failed")

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
            form.description.data = ''

            flash("Your Event was added Successfully!")

            return redirect(url_for('index'))
    return render_template('postevent.html', title="Add Event", form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)


