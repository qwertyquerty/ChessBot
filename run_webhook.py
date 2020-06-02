from chessbot.config import *
from chessbot.webhook import app

app.run("localhost", port=WEBHOOK_PORT)