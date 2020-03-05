from zero_to_hero import *



# Flask for basic API routing, jsonify to 'translate' the data you send, request to 'translate' the data received!

from flask import Flask, jsonify, request

# CORS is to allow us to access this API from a different server
from flask_cors import CORS

# time lib only for me to use sleep method to simulate delay waiting for model to run - you can get rid of it
import time

app = Flask(__name__)
# apply the cors config to allow access
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route("/predict", methods=["POST"])
def predict_top_hero():
    user_rating = request.get_json()
    print(f'You rated: is {user_rating}')
    result = new_hero_new_user_prediction(user_rating, heroes, algobaseitems)
#     print(f'Your results are: {result}')
    # database.add_this_person(user_ratings)
    # result model.predict(whatever_you_need_for_that)
    # get rid of this when using the actual model!
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)