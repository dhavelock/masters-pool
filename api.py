import flask
from flask import request, jsonify
from leaderboard import update_pool

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/', methods=['GET'])
def update():
    return jsonify(update_pool())

app.run()