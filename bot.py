import discord
import traceback
import db
from config import *
from util import *
from commands import *

command_list = [about.command, badge.command, bio.command, board.command, coinflip.command, debug.command, donate.command, draw.command, exit.command, fen.command, game.command, games.command, help.command, invite.command, leaderboard.command, listserver.command, move.command, newgame.command, ping.command, ping.command, prefix.command, profile.command, resign.command, restart.command, server.command, setstatus.command, stats.command, suggestion.command, takeback.command, vote.command, blacklist.command, unblacklist.command, pocket.command,reset.command]

bot = discord.AutoShardedClient()
stats = Stats(bot)

@bot.event
async def on_ready():
	stats.startgames = db.games.count()
	stats.startguilds = len(bot.guilds)
	stats.startusers = len(bot.users)
	if MOTD == "":
		await bot.change_presence(activity=discord.Game(name=str(db.games.find().count())+" games!"),status=discord.Status.online)
	else:
		await bot.change_presence(activity=discord.Game(name=MOTD),status=discord.Status.online)

@bot.event
async def on_guild_join(guild):
	db.Guild.new(guild.id,guild.name)
	await send_dbl_stats(bot)

@bot.event
async def on_guild_remove(guild):
	await send_dbl_stats(bot)

@bot.event
async def on_guild_update(before, after):
	guild = db.Guild.from_id(after.id)
	if after.name != guild.name: guild.set("name", after.name)


@bot.event
async def on_message(message):
	ctx = Ctx()
	ctx.bot = bot
	ctx.stats = stats
	ctx.stats.messages += 1
	ctx.msg = message
	ctx.message = ctx.msg
	ctx.mem = ctx.msg.author
	ctx.content = ctx.msg.content
	ctx.ch = ctx.msg.channel
	ctx.channel = ctx.ch
	try:
		ctx.guild = ctx.msg.guild
		ctx.mentions = ctx.msg.mentions
		ctx.dbguild = db.Guild.from_guild(ctx.guild)

		if ctx.guild.name != ctx.dbguild.name: ctx.dbguild.set("name", ctx.guild.name)

		ctx.prefix = ctx.dbguild.prefix

		if ctx.mem.id != BOT_ID and not ctx.mem.bot and ctx.content.startswith(ctx.prefix):
			ctx.user = db.User.from_mem(ctx.mem)

			if ctx.user.name != str(ctx.mem): ctx.user.set("name", str(ctx.mem))
			if ctx.user.flags & USER_FLAG_BLACKLISTED: return

			ctx.game = db.Game.from_user_id(ctx.mem.id)
			ctx.args = ' '.join(ctx.msg.content.strip(ctx.prefix).split()).split()

			if len(ctx.args) == 0: return

			ctx.command = ctx.args.pop(0).lower()

			for cmd in command_list:
				if ctx.command == cmd.name or ctx.command in cmd.aliases:
					await ctx.ch.trigger_typing()
					await cmd.call(ctx)

					ctx.stats.commandcalls += 1

					if ctx.guild != None: await log_command(ctx)
					if ctx.dbguild != None: ctx.dbguild.inc("calls", 1)

					break



	except Exception as E:
		if type(E) == discord.errors.Forbidden:
			await ctx.mem.send("I don't have permissions to talk in that channel! I need: ```Read Messages, Send Messages, Embed Links, Upload files, Add reactions``` If you do not have permission to change these, talk to the server owner.")
		elif type(E) == UnboundLocalError:
			await ctx.mem.send("I don't do DMs nerd")
		else:
			await log_error(ctx.bot,ctx.msg,traceback.format_exc())




bot.run(BOTTOKEN)
