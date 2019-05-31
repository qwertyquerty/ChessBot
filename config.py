import re
from tok import *

BOTURL = "https://discordbots.org/bot/366770566331629579"
MOTD = ""

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
VARIANT_SUICIDE = 1
VARIANT_CRAZYHOUSE = 2
VARIANT_ATOMIC = 3
VARIANT_KOTH = 4
VARIANT_ANTICHESS = 5
VARIANT_RACINGKINGS = 6
VARIANT_HORDE = 7
VARIANT_NAMES = ["Chess", "Suicide", "Crazyhouse", "Atomic", "King of the Hill", "Antichess", "Racing Kings", "Horde"]

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

#
USER_FLAG_BLACKLISTED = 1
USER_FLAG_TOURNAMENT_1ST = 2
USER_FLAG_TOURNAMENT_2ND = 4
USER_FLAG_PATRON = 8
USER_FLAG_MASTER = 16

ELO_K = 75

STARTING_ELO = 1200

ACCEPT_MARK = "\U00002705"
DENY_MARK = "\U0000274e"

COLOR = 4623620
EMBED_COLOR = 4623620


ID_REGEX = re.compile("[0-9]+")
USERNAME_REGEX = re.compile(".+#[0-9][0-9][0-9][0-9]")

DBLURL = "https://discordbots.org/api/bots/366770566331629579/stats"
DISCURL = "https://discordapp.com/api"
VOTEURL = "https://discordbots.org/bot/366770566331629579/vote"

DBLHEADERS = {"Authorization" : DBLTOKEN}
DISCHEADERS = {"Authorization" : "Bot "+BOTTOKEN}

BOT_ID = 366770566331629579

PREFIX = "|"

CHESSBOTSERVER = 430504476458221570

ERRORCHANNEL = 433431162107723787
VOTECHANNEL = 430858422582378517
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
    "intermediate":
    "\U0001f5e1",
    "novice": "\U0001f4a1",
    "addicted": "\U0001f48a",
    "master": "\U0001f3c6",
    "patron": "\U0001f4b3",
    "chess-bot-master": "\U0001f3f3",
    "blacklisted": "\U0001f6ab"
}

PAGELENGTH = 8

WINMESSAGES = [
"{winner} TORE THE HEAD OFF OF--err, won in a chess match against {loser}",
"{winner} just absolutely demolished {loser}"
]


DISCORD_LINK = "https://discord.gg/uV5y7RY"

BOARD_CSS = """
text {
    fill: #f1ad00;
    font-size:20px;
    font-weight: bold;
}
"""

ELO_ROLES = {
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

HELP = [
    {
        "newgame [mention]": "Start a new game against someone!\nSupported varients: atomic, koth, antichess, crazyhouse, horde, and racingkings.",
        "board": "View the board!",
        "move [LAN]": "Make a move using Long Notation, aka a2a3 to move the piece at a2 to a3. Promoting: a7a8q",
        "go [SAN]": "Make a move using Standard Notation, more complicated. If you don't know this, use {prefix}move",
        "draw": "Request a draw!",
        "takeback": "Request a takeback!",
        "resign": "Resign the current game you are in!",
        "exit": "Exit a game as if it were not ranked. ONLY USE THIS IF YOUR OPPONENT IS CHEATING OR WAITING YOU OUT. ABUSE WILL LEAD TO A BLACKLIST!",
    },
    {
        "about": "All about me!",
        "vote": "Vote for the bot and earn rewards!",
        "leaderboard": "View the global elo leaderboard!",
        "ping": "View the latency of the bot!",
        "fen (mention)": "Get the FEN of a game!",
        "pgn": "This command has been removed. use {prefix}game instead.",
        "hasbeat [mention 1] [mention 2]": "Check if one user has beat another!",
        "coinflip": "Flip a coin!",
    },
    {
        "profile (mention)": "View your, or someone else's profile!",
        "games (mention)": "View a list of your games!",
        "game (mention/game id)": "View your current game, or a previous one!",
        "bio [bio]": "Set your personal profile bio!",
        "badge [emote]": "View a badge name!",
    },
    {
        "server": "Join the official ChessBot server!",
        "invite": "Invite the bot to your server too!",
        "listserver": "List your server as a public Chess server!",
        "prefix [prefix]": "Change the bot prefix for your server!",
        "help": "You're reading it... buddy...",
        "suggestion [suggestion]": "Offer up a suggestion to the oh great qwerty.",
        "donate": "I need the money to keep ChessBot up, so please. Pay up.",
    }
]
