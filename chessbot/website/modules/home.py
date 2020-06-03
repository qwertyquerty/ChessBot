from flask import abort, Blueprint, redirect, request, render_template, Response

from chessbot.config import *
from chessbot import db

import chess
import chess.svg

blueprint_home = Blueprint('home', __name__)

@blueprint_home.route("/")
def page_index():
	return render_template("home.html")

@blueprint_home.route("/game_image/<string:game_id>")
def page_game_image(game_id):
	try:
		game = db.Game.from_id(game_id)
	except:
		return abort(400)

	if not game:
		return abort(404)
	
	return Response(chess.svg.board(game.board, lastmove=game.board.peek(), style=BOARD_CSS), content_type="image/svg+xml")

@blueprint_home.route("/leaderboard")
def page_leaderboard():
	return render_template("leaderboard.html")

@blueprint_home.route("/invite")
def page_invite():
	return redirect(BOT_INVITE_LINK)

@blueprint_home.route("/github")
def page_github():
	return redirect(GITHUB_LINK)