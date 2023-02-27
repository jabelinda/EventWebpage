from flask import Flask, render_template, url_for

app = Flask(__name__)

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


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # img_file = url_for('static', filename='images/whatsup-vertical.png')
    # , img_file=img_file
    return render_template('index.html', title="Home", events=events)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
