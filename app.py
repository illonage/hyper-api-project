from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def respond():
    return 'hello you'

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json);
    return Response(status=200)