from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # img_file = url_for('static', filename='images/whatsup-vertical.png')
    # , img_file=img_file
    return render_template('index.html', title="Home")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
