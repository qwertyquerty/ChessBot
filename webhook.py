from flask import Flask, request, jsonify
import db
from config import *
app = Flask(__name__)

@app.route('/api/votes', methods=['POST'])
def on_vote():
    print(request.headers)
    if request.headers.get('Authorization') == WEBHOOKTOKEN:
        data = request.json

        try:
            user = int(data['user'])
        except Exception as E:
            return jsonify({'success': False})

        try:
            user = db.User.from_id(user)
            user.inc("votes", 1)
        except Exception as E:
            pass

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    print(request.headers)
    try:
        d = {
            "games": db.games.find({"valid": True}).count()
        }
        return jsonify(d)
    except:
        return jsonify({'success': False})

app.run(host="0.0.0.0", port=3000,debug=True)
