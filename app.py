from flask import Flask

app = Flask(__name__)

@app.route('/') #basic route
def index():
    return "Hello"


@app.route('/Saja') #basic route
def Saja():
    return "Hello Saja"


if __name__ == '__main__':
    app.run(debug=True)
