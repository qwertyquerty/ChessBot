from flask import abort, Blueprint, redirect, request, render_template, Response

from chessbot.config import *
from chessbot import db
from chessbot.command import Command
from chessbot.commands import *

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

	if len(game.board.move_stack) > 0:
		board_svg = chess.svg.board(game.board, lastmove=game.board.peek())
	else:
		board_svg = chess.svg.board(game.board)
	
	return Response(board_svg, content_type="image/svg+xml")


@blueprint_home.route("/leaderboard")
def page_leaderboard():
	return render_template("leaderboard.html")


@blueprint_home.route("/commands")
def page_commands():
	available_commands = [command for command in Command.__subclasses__() if command.level == LEVEL_EVERYONE]
	sorted_commands = sorted(available_commands, key = lambda x: x.help_index)

	return render_template("commands.html", commands=sorted_commands, prefix=PREFIX)

@blueprint_home.route("/user/<int:id>")
def page_user(id):

	user = db.User.from_user_id(id)

	if not user:
		abort(404)

	return render_template("user.html", user=user)


@blueprint_home.route("/invite")
def page_invite():
	return redirect(BOT_INVITE_LINK)


@blueprint_home.route("/github")
def page_github():
	return redirect(GITHUB_LINK)