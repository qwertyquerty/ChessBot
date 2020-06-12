from chessbot.config import *
from chessbot.website import app

app.run("localhost", port=WEBHOOK_PORT, debug=True)