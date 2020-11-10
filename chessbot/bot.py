from chessbot.command import Command
from chessbot.commands import *
from chessbot.config import *
from chessbot import db
from chessbot.util import *

import elasticapm

import discord
import traceback

class ChessBot(discord.AutoShardedClient):
	def __init__(self, pid=None, **kwargs):
		super().__init__(**kwargs)
		
		self.pid = pid
		self.prefix_cache = {}
		self.command_list = Command.__subclasses__()

		self.log_channel = None
		self.error_channel = None

		if APM_SERVICE:
			self.apm = elasticapm.Client({'SERVICE_NAME': APM_SERVICE})

	async def on_ready(self):
		self.log_channel = await self.fetch_channel(LOGCHANNEL)
		self.error_channel = await self.fetch_channel(ERRORCHANNEL)

		await update_activity(self)

		await send_dbl_stats(self)

	async def on_guild_join(self, guild):
		db.Guild.new(guild.id,guild.name)
		await send_dbl_stats(self)

	async def on_guild_remove(self, guild):
		await send_dbl_stats(self)

	async def on_guild_update(self, before, after):
		guild = db.Guild.from_guild_id(after.id)
		if after.name != guild.name: guild.set("name", after.name)

	async def on_message(self, message):
		ctx = Ctx()
		ctx.bot = self
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

			if ctx.guild.id in self.prefix_cache:
				ctx.prefix = self.prefix_cache[ctx.guild.id]
			else:
				ctx.dbguild = db.Guild.from_guild(ctx.guild)
				ctx.prefix = ctx.dbguild.prefix
				self.prefix_cache[ctx.guild.id] = ctx.dbguild.prefix

			if not ctx.mem.bot and ctx.content.startswith(ctx.prefix):

				ctx.raw_args = ' '.join(ctx.msg.content[len(ctx.prefix):].split()).split()
				ctx.args = []

				if len(ctx.raw_args) == 0: return

				ctx.command = ctx.raw_args.pop(0).lower()

				for cmd in self.command_list:
					if ctx.command == cmd.name or ctx.command in cmd.aliases:

						### Make the bot type while it works out the command
						await ctx.ch.trigger_typing()

						### Update user name and guild name if needed when a viable command is found
						ctx.user = db.User.from_mem(ctx.mem)
						if ctx.user.name != str(ctx.mem): ctx.user.set("name", str(ctx.mem))

						if ctx.dbguild == None:
							ctx.dbguild = db.Guild.from_guild(ctx.guild)

						if ctx.guild.name != ctx.dbguild.name: ctx.dbguild.set("name", ctx.guild.name)

						### Fetch the game because it's usually needed (probably bad practice here whatever tho)
						ctx.game = db.Game.from_user_id(ctx.mem.id)

						if self.apm:
							self.apm.begin_transaction("command")
							elasticapm.set_transaction_name("command.{}".format(cmd.name), override=False)

						### Actually call the command
						await cmd.call(ctx)

						if ctx.guild != None:
							await log_command(ctx)
							if self.apm: self.apm.end_transaction("command", "success")

						break

		except Exception as E:
			if type(E) == discord.errors.Forbidden:
				await ctx.mem.send("I don't have permissions to talk in that channel! I need: ```Read Messages, Send Messages, Embed Links, Upload files, Add reactions``` If you do not have permission to change these, talk to the server owner.")
			elif type(E) == UnboundLocalError:
				await ctx.mem.send("I don't do DMs nerd")
			else:
				if self.apm:
					self.apm.capture_exception()
				await log_error(ctx.bot, ctx.msg, traceback.format_exc())
