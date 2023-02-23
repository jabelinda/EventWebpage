from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return "<h1>Hello Everyone!</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)