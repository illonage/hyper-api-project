from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "<h1> Deployed to Heroku</h1>"

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json)
    return '', 200

if __name__ == '__main__':
    app.run()
