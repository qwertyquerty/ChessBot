from flask import Flask, abort, request

from chessbot.config import *
from chessbot import db

app = Flask(__name__)

@app.route("/api/vote", methods = ['POST'])
def page_api_vote():

	if request.headers["Authorization"] != WEBHOOK_TOKEN:
		return abort(401)

	user = db.User.from_user_id(request.json["user"])

	if not user:
		return abort(400)
	
	user.inc("votes", 1)
	return abort(200)

app.run("localhost", port=WEBHOOK_PORT)