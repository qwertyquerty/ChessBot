from chessbot import config
from chessbot.config import *
from chessbot import db

import aiohttp
import math
import random
import chess
import discord
import time
import chess.pgn
import chess.svg
import cairosvg
import traceback
from io import BytesIO

from .glicko2 import Glicko2

glicko_env = Glicko2(GLICKO_MU, GLICKO_PHI, GLICKO_SIGMA, GLICKO_TAU)

class Ctx():
    def __init__(self):
        pass

async def send_dbl_stats(bot):
    if bot.pid == 0:
        try:
            payload = {"shard_count": SHARDS_PER_PROCESS * PROCESSES, "server_count": len(bot.guilds) * PROCESSES}
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post(DBLURL, data=payload, headers=DBLHEADERS)
        except:
            await log_lone_error(bot, "DBL STATS API", traceback.format_exc())

def makeboard(board):
    if len(board.move_stack)>0:
        bytes = cairosvg.svg2png(bytestring=chess.svg.board(board=board, lastmove=board.peek()))
    else:
        bytes = cairosvg.svg2png(bytestring=chess.svg.board(board=board))
    bytesio = BytesIO(bytes)
    dfile = discord.File(bytesio, filename="board.png")
    return dfile

def ment(id):
    return "<@!{}>".format(id)

def codeblock(s, language=None):
    if language != None:
        return "```{}\n{}```".format(language,s)
    return "```{}```".format(s)

def rating_sync():
    users = {}
    games = db.date_ordered_games()

    for game in games:
        if game["ranked"] and game["valid"] and game["outcome"] != OUTCOME_EXIT and game["outcome"] != OUTCOME_UNFINISHED:
            if not game["1"] in users:
                users[game["1"]] = glicko_env.create_rating()

            if not game["2"] in users:
                users[game["2"]] = glicko_env.create_rating()

            if game["outcome"] == OUTCOME_DRAW:
                new_rating = glicko_env.rate_1vs1(users[game["1"]], users[game["2"]], drawn=True)
                users[game["1"]] = new_rating[0]
                users[game["2"]] = new_rating[1]

            elif game["outcome"] == OUTCOME_RESIGN or game["outcome"] == OUTCOME_CHECKMATE:
                new_rating = glicko_env.rate_1vs1(users[game["winner"]], users[game["loser"]])
                users[game["winner"]] = new_rating[0]
                users[game["loser"]] = new_rating[1]

    default_rating = glicko_env.create_rating()
    db.users.update_many({}, {"$set": {"rating": default_rating.mu, "rating_deviation": default_rating.phi, "rating_volatility": default_rating.sigma}})

    for id, rating in users.items():
        db.users.update({"id": id}, {"$set": {"rating": rating.mu, "rating_deviation": rating.phi, "rating_volatility": rating.sigma}})

def get_base_board(g):
    if g.variant == VARIANT_CRAZYHOUSE: board = chess.variant.CrazyhouseBoard(fen=g.basefen)
    elif g.variant == VARIANT_KOTH: board = chess.variant.KingOfTheHillBoard(fen=g.basefen)
    elif g.variant == VARIANT_ATOMIC: board = chess.variant.AtomicBoard(fen=g.basefen)
    elif g.variant == VARIANT_ANTICHESS: board = chess.variant.AntichessBoard(fen=g.basefen)
    elif g.variant == VARIANT_RACINGKINGS: board = chess.variant.RacingKingsBoard(fen=g.basefen)
    elif g.variant == VARIANT_HORDE: board = chess.variant.HordeBoard(fen=g.basefen)
    elif g.variant == VARIANT_960 or g.variant == VARIANT_STANDARD: board = chess.Board(fen=g.basefen)

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
    await ctx.bot.log_channel.send(data)

async def log_error(bot, msg, error):
    data = "```USER NAME: {}\nUSER ID: {}\nGUILD NAME: {}\nGUILD ID: {}\nCHANNEL NAME: {}\nCHANNEL ID: {}\nMESSAGE: {}\nMESSAGE ID: {}\nTRACEBACK:\n\n{}```"
    data = data.format(msg.author, msg.author.id, msg.guild, msg.guild.id, msg.channel, msg.channel.id, msg.content, msg.id,error)
    await bot.error_channel.send(data)

async def log_lone_error(bot, event, error):
    data = "```ERROR IN: {}\nTRACEBACK:\n\n{}```"
    data = data.format(event, error)
    await bot.error_channel.send(data)


async def reward_game(winner,loser,outcome, game, channel, bot):
    winner = db.User.from_user_id(winner)
    loser = db.User.from_user_id(loser)
    guild = channel.guild
    if game.ranked:
        if (outcome == OUTCOME_RESIGN and len(game.moves) > 2) or outcome == OUTCOME_CHECKMATE:
            new_rating = glicko_env.rate_1vs1(winner.glicko, loser.glicko)
            winner.update_glicko(new_rating[0])
            loser.update_glicko(new_rating[1])

    if outcome == OUTCOME_CHECKMATE:
        if game.ranked:
            await channel.send(random.choice(WINMESSAGES).format(winner=ment(winner.id), loser=ment(loser.id))+"! Checkmate! ({}/{})".format(int(round(new_rating[0].mu-winner.rating, 0)),int(round(new_rating[1].mu-loser.rating, 0))))
        else:
            await channel.send(random.choice(WINMESSAGES).format(winner=ment(winner.id), loser=ment(loser.id))+"! Checkmate!")
        
        game.end(winner.id, loser.id, OUTCOME_CHECKMATE)

    if outcome == OUTCOME_RESIGN:
        if len(game.moves) > 2:
            if game.ranked:
                await channel.send("You have resigned! <@!"+str(winner.id)+"> wins! ({}/{})".format(int(round(new_rating[0].mu-winner.rating, 0)),int(round(new_rating[1].mu-loser.rating, 0))))
            else:
                await channel.send("You have resigned! <@!"+str(winner.id)+"> wins!")
            game.end(winner.id, loser.id, OUTCOME_RESIGN)
        else:
            await channel.send("You have resigned! <@!"+str(winner.id)+"> wins!")
            game.delete()

    if outcome == OUTCOME_DRAW:
        if len(game.moves) > 2:
            if game.ranked:
                new_rating = glicko_env.rate_1vs1(winner.glicko, loser.glicko, drawn=True)
                winner.update_glicko(new_rating[0])
                loser.update_glicko(new_rating[1])

                await channel.send("The game is a draw! Game over! ({}/{})".format(int(round(new_rating[0].mu-winner.rating, 0)),int(round(new_rating[1].mu-loser.rating, 0))))

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

    g = db.Game.from_id(game.id)
    if g:
        ch = await bot.fetch_channel(GAMESCHANNEL)
        await ch.send(embed=embed_from_game(g))

    await update_activity(bot)

def embed_from_game(game):
    em = discord.Embed()
    em.title="Game "+str(game.id)
    em.colour = discord.Colour(EMBED_COLOR)
    em.type = "rich"
    em.description = "```"+str(pgn_from_game(game))+"```"
    em.add_field(name="White",value=db.User.from_user_id(game.white).name,inline=True)
    em.add_field(name="Black",value=db.User.from_user_id(game.black).name,inline=True)
    em.add_field(name="Outcome",value=OUTCOME_NAMES[game.outcome],inline=True)

    if game.outcome in [OUTCOME_CHECKMATE, OUTCOME_RESIGN]:
        em.add_field(name="Winner",value=db.User.from_user_id(game.winner).name,inline=True)
    else:
        em.add_field(name="Winner",value=str(None),inline=True)

    em.add_field(name="Timestamp",value=str(game.timestamp.strftime('%m-%d-%Y %H:%M:%S')),inline=True)
    em.add_field(name="Ranked",value=str(game.ranked),inline=True)

    if game.variant != VARIANT_STANDARD:
        em.add_field(name="Variant",value=VARIANT_NAMES[game.variant],inline=True)
        
    return em

async def update_rating_roles(ctx):
    guild = ctx.bot.get_guild(CHESSBOTSERVER)
    rmroles = [guild.get_role(r) for r in RATING_ROLES.values()]
    for member in guild.members:
        user = db.User.from_mem(member)
        rating = int((user.rating)/100)*100
        rs = [r for r in rmroles if r in member.roles]
        if len(rs) > 0:
            await member.remove_roles(*rs)
        if user.game_count() > 0:
            if rating in RATING_ROLES:
                await member.add_roles(guild.get_role(RATING_ROLES[rating]))


async def update_activity(bot):
    await bot.change_presence(activity=discord.Game(name="{} / {} games!".format(
        db.games.find({"outcome": OUTCOME_UNFINISHED}).count(),
        db.games.count_documents({})
    )), status=discord.Status.online)