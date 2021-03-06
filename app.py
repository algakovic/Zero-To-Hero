# Import modules
from flask import Flask, jsonify, request

# CORS is to allow us to access this API from a different server
from flask_cors import CORS

app = Flask(__name__)
# apply the cors config to allow access
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World from Zero to Hero'


@app.route("/predict", methods=["POST"])
def predict_top_hero():
    user_rating = request.get_json()
    print(f'You rated: is {user_rating}')
    result = new_hero_new_user_prediction(user_rating, heroes, algobaseitems)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)s