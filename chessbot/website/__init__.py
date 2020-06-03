from flask import Flask, abort, request, send_from_directory

from chessbot.config import *
from chessbot import config
from chessbot import db

app = Flask(__name__)

app.url_map.strict_slashes = False


@app.context_processor
def context_processor():
	return dict(cfg=config, db=db)


@app.route('/static/<path:path>')
def static_content(path):
    return send_from_directory('./static', path)


from chessbot.website.modules.api import blueprint_api
from chessbot.website.modules.home import blueprint_home

app.register_blueprint(blueprint_api)
app.register_blueprint(blueprint_home)