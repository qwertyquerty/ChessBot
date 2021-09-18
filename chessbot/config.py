import chess.svg
from os import getenv

WEBHOOK_PORT = int(getenv('WEBHOOK_PORT', '7003'))

BOT_INVITE_LINK = getenv('BOT_INVITE_LINK', '')
GITHUB_LINK = getenv('GITHUB_LINK', "https://github.com/qwertyquerty/ChessBot")

BOTURL = getenv('BOTURL', "https://discordbots.org/bot/366770566331629579")
MOTD = getenv('MOTD', '')

COLOR_WHITE = True
COLOR_BLACK = False
COLOR_NAMES = ["Black", "White"]

OUTCOME_UNFINISHED = 0
OUTCOME_CHECKMATE = 1
OUTCOME_RESIGN = 2
OUTCOME_DRAW = 3
OUTCOME_EXIT = 4
OUTCOME_NAMES = ["Unfinished", "Checkmate", "Resign", "Draw", "Exit"]

VARIANT_STANDARD = 0
VARIANT_CRAZYHOUSE = 2
VARIANT_ATOMIC = 3
VARIANT_KOTH = 4
VARIANT_ANTICHESS = 5
VARIANT_RACINGKINGS = 6
VARIANT_HORDE = 7
VARIANT_960 = 8
VARIANT_NAMES = ["Chess", "Suicide", "Crazyhouse", "Atomic", "King of the Hill", "Antichess", "Racing Kings", "Horde", "Chess960"]

RATED = True
CASUAL = False
RATED_NAMES = ["Casual", "Rated"]

#LEVELS
LEVEL_EVERYONE = 0
LEVEL_MOD = 1
LEVEL_ADMIN = 2
LEVEL_OWNER = 3

#FLAGS
FLAG_NONE = 0
FLAG_MUST_BE_IN_GAME = 1
FLAG_MUST_BE_SERVER_OWNER = 2
FLAG_MUST_HAVE_PERM_MANAGE_SERVER = 4
FLAG_MUST_NOT_BE_BLACKLISTED = 8

#
USER_FLAG_BLACKLISTED = 1
USER_FLAG_TOURNAMENT_1ST = 2
USER_FLAG_TOURNAMENT_2ND = 4
USER_FLAG_PATRON = 8
USER_FLAG_MASTER = 16

GLICKO_MU = 1200.0
GLICKO_PHI = 250.0
GLICKO_SIGMA = 0.06
GLICKO_TAU = 0.75

GLICKO_PROVISIONAL_MIN_PHI = 150

ACCEPT_MARK = "\U00002705"
DENY_MARK = "\U0000274e"

EMBED_COLOR = 4623620

MAX_MESSAGE_CACHE = 5000

DBLURL = "https://top.gg/api/bots/366770566331629579/stats"

BOTVOTEURL = "https://top.gg/bot/366770566331629579/vote"
SERVERVOTEURL = "https://top.gg/servers/430504476458221570/vote"

PREFIX = getenv('PREFIX', "|")

CHESSBOTSERVER = 430504476458221570

ERRORCHANNEL = 433431162107723787
LOGCHANNEL = 436342882551595008
GAMESCHANNEL = 503633867673042953
SUGGESTIONCHANNEL = 441095220038467585

BADGES = {
    "blunder": "\U00002753",
    "proficient": "\U00002757",
    "brilliant": "\U0000203c",
    "tournament-first-place": "\U0001f947",
    "tournament-second-place": "\U0001f948",
    "developer": "\U00002699",
    "admin": "\U0001f440",
    "voter": "\U0001f4dd",
    "expert": "\U00002694",
    "intermediate": "\U0001f5e1",
    "novice": "\U0001f4a1",
    "addicted": "\U0001f48a",
    "master": "\U0001f3c6",
    "patron": "\U0001f4b3",
    "blacklisted": "\U0001f6ab",
    "supporter": "\u2764"
}

PAGELENGTH = 8

WINMESSAGES = [
"{winner} TORE THE HEAD OFF OF--err, won in a chess match against {loser}",
"{winner} just absolutely demolished {loser}",
"{winner} completely outwitted {loser}",
"{winner} has asserted dominance over {loser}",
"{winner} is obviously better at Chess than {loser}"
]

DISCORD_LINK = "https://discord.gg/uV5y7RY"

chess.svg.DEFAULT_COLORS["coord"] = "#f1ad00"
chess.svg.DEFAULT_COLORS["margin"] = "rgba(0,0,0,0)"

RATING_ROLES = {
    1200: 559561778607161376,
    1300: 559561460787838976,
    1400: 559561680632152064,
    1500: 559561732595384350,
    1600: 559561811440173073,
    1700: 559561870013366273,
    1800: 559561905937711124,
    1900: 559561940586987551,
    2000: 559562032920264705,
}

SHARDS_PER_PROCESS = 12
PROCESSES = 4

APM_SERVICE = None

from chessbot.tok import * # Overwrite defaults


DBLHEADERS = {"Authorization" : DBLTOKEN}
