import math
from config import *
import db
import random
import chess
import discord
import time
import chess.pgn
import chess.svg
import cairosvg
from io import BytesIO

class Ctx():
    def __init__(self):
        pass

class Stats():
    def __init__(self,bot):
        self.messages = 0
        self.commandcalls = 0
        self.startgames = db.games.count()
        self.startguilds = len(bot.guilds)
        self.startusers = len(bot.users)
        self.starttime = int(time.time())


async def send_dbl_stats(bot):
    try:
        payload = {"shard_count": len(bot.shards), "server_count": len(bot.guilds)}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(DBLURL, data=payload, headers=DBLHEADERS)
    except:
        pass

def makeboard(board):
    if len(board.move_stack)>0:
        bytes = cairosvg.svg2png(bytestring=chess.svg.board(board=board, lastmove=board.peek(), style=BOARD_CSS))
    else:
        bytes = cairosvg.svg2png(bytestring=chess.svg.board(board=board, style=BOARD_CSS))
    bytesio = BytesIO(bytes)
    dfile = discord.File(bytesio, filename="board.png")
    return dfile

def ment(id):
    return "<@!{}>".format(id)

def codeblock(s, language=None):
    if language != None:
        return "```{}\n{}```".format(language,s)
    return "```{}```".format(s)

def elo_probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def elo_rating(ra, rb, K, draw=False):

    pb = elo_probability(ra, rb)

    pa = elo_probability(rb, ra)
    if not draw:
        ra = int(round(ra + K * (1 - pa),0))
        rb = int(round(rb + K * (0 - pb),0))
    else:
        ra = int(round(ra + K * (0.5 - pa),0))
        rb = int(round(rb + K * (0.5 - pb),0))
    return (ra,rb)


def elo_sync():
    users = {}
    games = db.date_ordered_games()
    for game in games:
        if game["ranked"] and game["valid"] and game["outcome"] != OUTCOME_EXIT and game["outcome"] != OUTCOME_UNFINISHED:
            if not game["1"] in users:
                users[game["1"]] = STARTING_ELO
            if not game["2"] in users:
                users[game["2"]] = STARTING_ELO
            if game["outcome"] == OUTCOME_DRAW:
                e = elo_rating(users[game["1"]], users[game["2"]], ELO_K, draw=True)
                users[game["1"]] = e[0]
                users[game["2"]] = e[1]
            elif game["outcome"] == OUTCOME_RESIGN or game["outcome"] == OUTCOME_CHECKMATE:
                e = elo_rating(users[game["winner"]], users[game["loser"]], ELO_K)
                users[game["winner"]] = e[0]
                users[game["loser"]] = e[1]
    db.users.update_many({}, {"$set": {"elo": STARTING_ELO}})
    for id,elo in users.items():
        db.users.update({"id": id}, {"$set": {"elo": elo}})

def get_base_board(g):
    if g.variant == VARIANT_SUICIDE: board = chess.variant.SuicideBoard(fen=g.basefen)
    elif g.variant == VARIANT_CRAZYHOUSE: board = chess.variant.CrazyhouseBoard(fen=g.basefen)
    elif g.variant == VARIANT_KOTH: board = chess.variant.KingOfTheHillBoard(fen=g.basefen)
    elif g.variant == VARIANT_ATOMIC: board = chess.variant.AtomicBoard(fen=g.basefen)
    elif g.variant == VARIANT_ANTICHESS: board = chess.variant.GiveawayBoard(fen=g.basefen)
    elif g.variant == VARIANT_RACINGKINGS: board = chess.variant.RacingKingsBoard(fen=g.basefen)
    elif g.variant == VARIANT_HORDE: board = chess.variant.HordeBoard(fen=g.basefen)
    elif g.variant == VARIANT_960 or g.variant == VARIANT_STANDARD or g.variant == VARIANT_CUSTOMFEN: board = chess.Board(fen=g.basefen)
    return board

def pgn_from_game(g):
    board = get_base_board(g)
    pb = chess.pgn.Game().without_tag_roster()
    pb.setup(board)
    pb.headers["Site"] = BOTURL
    pn = pb
    for i in g.moves:
        pn = pn.add_variation(chess.Move.from_uci(i))
    return pb


async def log_command(ctx):
    data = "```USER NAME: {}\nUSER ID: {}\nGUILD NAME: {}\nGUILD ID: {}\nCHANNEL NAME: {}\nCHANNEL ID: {}\nMESSAGE ID: {}\nCOMMAND: {}\nARGS: {}```"
    data = data.format(ctx.mem, ctx.mem.id, ctx.guild, ctx.guild.id, ctx.ch, ctx.ch.id, ctx.msg.id, ctx.command, ctx.args)
    await ctx.bot.get_channel(LOGCHANNEL).send(data)

async def log_error(bot, msg, error):
    data = "```USER NAME: {}\nUSER ID: {}\nGUILD NAME: {}\nGUILD ID: {}\nCHANNEL NAME: {}\nCHANNEL ID: {}\nMESSAGE: {}\nMESSAGE ID: {}\nTRACEBACK:\n\n{}```"
    data = data.format(msg.author, msg.author.id, msg.guild, msg.guild.id, msg.channel, msg.channel.id, msg.content, msg.id,error)
    await bot.get_channel(ERRORCHANNEL).send(data)


async def reward_game(winner,loser,outcome, game, channel, bot):
    winner = db.User.from_id(winner)
    loser = db.User.from_id(loser)
    guild = channel.guild
    if game.ranked:
        if outcome == OUTCOME_RESIGN or outcome == OUTCOME_CHECKMATE:
            new_elo = elo_rating(winner.elo, loser.elo, ELO_K)
            winner.set("elo", new_elo[0])
            loser.set("elo", new_elo[1])

    if outcome == OUTCOME_CHECKMATE:
        if game.ranked:
            await channel.send(random.choice(WINMESSAGES).format(winner=ment(winner.id), loser=ment(loser.id))+"! Checkmate! ({}/{})".format(new_elo[0]-winner.elo,new_elo[1]-loser.elo))
        else:
            await channel.send(random.choice(WINMESSAGES).format(winner=ment(winner.id), loser=ment(loser.id))+"! Checkmate!")
        game.end(winner.id, loser.id, OUTCOME_CHECKMATE)

    if outcome == OUTCOME_RESIGN:
        if len(game.moves) > 2:
            if game.ranked:
                await channel.send("You have resigned! <@!"+str(winner.id)+"> wins! ({}/{})".format(new_elo[0]-winner.elo,new_elo[1]-loser.elo))
            else:
                await channel.send("You have resigned! <@!"+str(winner.id)+"> wins!")
            game.end(winner.id, loser.id, OUTCOME_RESIGN)
        else:
            await channel.send("You have resigned! <@!"+str(winner.id)+"> wins!")
            game.delete()

    if outcome == OUTCOME_DRAW:
        if len(game.moves) > 2:
            if game.ranked:
                new_elo = elo_rating(winner.elo, loser.elo, ELO_K, draw=True)
                winner.set("elo", new_elo[0])
                loser.set("elo", new_elo[1])
                await channel.send("The game is a draw! Game over! ({}/{})".format(new_elo[0]-winner.elo,new_elo[1]-loser.elo))

            else:
                await channel.send("The game is a draw! Game over!")
            game.end(None, None, OUTCOME_DRAW)
        else:
            await channel.send("The game is a draw! Game over!")
            game.delete()

    if outcome == OUTCOME_EXIT:
        await channel.send('You have exited the game!')
        if len(game.moves) > 2:
            game.end(None, None, OUTCOME_EXIT)
        else:
            game.delete()

    g = db.Game.from_id(game._id)
    if g:
        await bot.get_channel(GAMESCHANNEL).send(embed=embed_from_game(g))


def embed_from_game(game):
    em = discord.Embed()
    em.title="Game "+str(game._id)
    em.colour = discord.Colour(COLOR)
    em.type = "rich"
    em.description = "```"+str(pgn_from_game(game))+"```"
    em.add_field(name="White",value=db.User.from_id(game.white).name,inline=True)
    em.add_field(name="Black",value=db.User.from_id(game.black).name,inline=True)
    em.add_field(name="Outcome",value=OUTCOME_NAMES[game.outcome],inline=True)
    if game.outcome in [OUTCOME_CHECKMATE, OUTCOME_RESIGN]:
        em.add_field(name="Winner",value=db.User.from_id(game.winner).name,inline=True)
    else:
        em.add_field(name="Winner",value=str(None),inline=True)
    em.add_field(name="Timestamp",value=str(game.timestamp.strftime('%m-%d-%Y %H:%M:%S')),inline=True)
    em.add_field(name="Ranked",value=str(game.ranked),inline=True)
    if game.variant != VARIANT_STANDARD:
        em.add_field(name="Variant",value=VARIANT_NAMES[game.variant],inline=True)
    return em

async def update_elo_roles(ctx):
    guild = ctx.bot.get_guild(CHESSBOTSERVER)
    rmroles = [guild.get_role(r) for r in ELO_ROLES.values()]
    for member in guild.members:
        user = db.User.from_mem(member)
        elo = int((user.elo)/100)*100
        rs = [r for r in rmroles if r in member.roles]
        await member.remove_roles(*rs)
        time.sleep(0.2)
        if elo in ELO_ROLES:
            await member.add_roles(guild.get_role(ELO_ROLES[elo]))

def rig(**kwargs):
    return "Game Rigged"
