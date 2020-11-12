import flask
from flask import request, jsonify
from leaderboard import update_pool
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/v1/": {"origins": "http://localhost:4200/"}})

@app.route('/api/v1/leaderboard', methods=['GET'])
def update():
    response = {
        'leaderboard': update_pool()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()