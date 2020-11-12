import flask
from flask import request, jsonify
from leaderboard import update_pool
from flask_cors import CORS
from datetime import datetime
import pytz

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/v1/leaderboard', methods=['GET'])
def update():
    response = {
        'leaderboard': update_pool(),
        'last_updated': get_timestamp()
    }
    return jsonify(response)

def get_timestamp():
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    eastern = pytz.timezone('US/Eastern')
    return eastern.localize(datetime.now()).strftime(fmt)

if __name__ == '__main__':
    app.run()