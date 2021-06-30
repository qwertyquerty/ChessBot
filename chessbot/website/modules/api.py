from flask import abort, Blueprint, request, Response

from chessbot.config import *
from chessbot import db

blueprint_api = Blueprint('api', __name__)

@blueprint_api.route("/api/vote", methods = ['GET', 'POST'])
def page_api_vote():

	if request.headers["Authorization"] != WEBHOOK_TOKEN:
		return abort(401)
	
	print(request.args)
	uid = int(request.json()["user"])

	user = db.User.from_user_id(uid)

	if not user:
		return abort(400)
	
	user.inc("votes", 1)
	return Response(status=200)
