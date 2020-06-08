from chessbot.command import Command
from chessbot.commands import *
from chessbot.config import *
from chessbot import db
from chessbot.util import *

import discord
import traceback

command_list = Command.__subclasses__()

prefix_cache = {}


bot = discord.AutoShardedClient(max_messages=MAX_MESSAGE_CACHE)
stats = Stats(bot)

@bot.event
async def on_ready():
	stats.startgames = db.games.count_documents({})
	stats.startguilds = len(bot.guilds)
	stats.startusers = len(bot.users)
	
	if MOTD == "":
		await bot.change_presence(activity=discord.Game(name=str(db.games.count_documents({}))+" games!"),status=discord.Status.online)
	else:
		await bot.change_presence(activity=discord.Game(name=MOTD),status=discord.Status.online)
	
	await send_dbl_stats(bot)

@bot.event
async def on_guild_join(guild):
	db.Guild.new(guild.id,guild.name)
	await send_dbl_stats(bot)

@bot.event
async def on_guild_remove(guild):
	await send_dbl_stats(bot)

@bot.event
async def on_guild_update(before, after):
	guild = db.Guild.from_guild_id(after.id)
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

		ctx.dbguild = None

		if ctx.guild.id in prefix_cache:
			ctx.prefix = prefix_cache[ctx.guild.id]
		else:
			ctx.dbguild = db.Guild.from_guild(ctx.guild)
			ctx.prefix = ctx.dbguild.prefix
			prefix_cache[ctx.guild.id] = ctx.dbguild.prefix

		if ctx.mem.id != ctx.bot.user.id and not ctx.mem.bot and ctx.content.startswith(ctx.prefix):

			if ctx.dbguild == None:
				ctx.dbguild = db.Guild.from_guild(ctx.guild)

			if ctx.guild.name != ctx.dbguild.name: ctx.dbguild.set("name", ctx.guild.name)

			ctx.user = db.User.from_mem(ctx.mem)

			if ctx.user.name != str(ctx.mem): ctx.user.set("name", str(ctx.mem))

			ctx.game = db.Game.from_user_id(ctx.mem.id)
			ctx.raw_args = ' '.join(ctx.msg.content[len(ctx.prefix):].split()).split()
			ctx.args = []

			if len(ctx.raw_args) == 0: return

			ctx.command = ctx.raw_args.pop(0).lower()

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
			await log_error(ctx.bot, ctx.msg, traceback.format_exc())
