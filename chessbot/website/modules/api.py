from flask import abort, Blueprint, request

from chessbot.config import *
from chessbot import db

blueprint_api = Blueprint('api', __name__)

@blueprint_api.route("/api/vote", methods = ['POST'])
def page_api_vote():

	if request.headers["Authorization"] != WEBHOOK_TOKEN:
		return abort(401)
	
	print(request.json)

	user = db.User.from_user_id(request.json["user"])

	print(user)

	if not user:
		return abort(400)
	
	user.inc("votes", 1)
	return abort(200)
