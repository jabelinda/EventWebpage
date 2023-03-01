from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # img_file = url_for('static', filename='images/whatsup-vertical.png')
    # , img_file=img_file
    return render_template('index.html', title="Home")


@app.route("/register")
def register():
    return render_template('register.html', title="Sign in")


@app.route("/postevent")
def postevent():
    return render_template('postevent.html', title="Post Event")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7001, debug=True)
