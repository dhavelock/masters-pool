import flask
from flask import request, jsonify
from leaderboard import update_pool

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/leaderboard', methods=['GET'])
def update():
    response = {
        'leaderboard': update_pool()
    }
    return jsonify(update_pool())

if __name__ == '__main__':
    app.run()