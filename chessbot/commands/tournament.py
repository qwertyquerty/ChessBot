from chessbot.command import *

class CommandTournament(Command):
	name = "tournament"
	aliases = ["tnmt"]
	helpstring = ["tournament", "Usually has something to do with Chess tournaments"]

	@classmethod
	async def run(self,ctx):

			if len(ctx.args) > 0 and ctx.args[0] == "signup":
				
				chessbotguild = ctx.bot.get_guild(CHESSBOTSERVER)

				if ctx.mem not in chessbotguild:
					await ctx.mem.send("In order to sign up for the tournament, you must be in the ChessBot Community server, as that is where the games will take place. After joining, try signing up again.\n\nHere's a link for ya: {}".format(DISCORD_LINK))
					return
				
				await ctx.bot.get_channel(714596355238133810).send("{} ({})".format(str(ctx.mem), ctx.mem.id))

				await ctx.mem.send("Thank you for signing up for the tournament. You will be notified about your first game sometime around 5/30/2020. You must stay in the ChessBot Community server if you wish to compete in the tournament. A bracket will be released in a few days.")

				await ctx.ch.send("You have successfully signed up for the tournament!")


class CommandMegaAd(Command):
	name = "megaad"
	aliases = []
	helpstring = ["megaad", "For qwerty"]
	level = LEVEL_OWNER

	@classmethod
	async def run(self,ctx):

		await ctx.ch.send("I'm doin it:")

		announcement = ctx.content[len(ctx.prefix+ctx.command):]

		await ctx.ch.send(announcement.replace("[prefix]", ctx.prefix))

		notifs = 0

		for guild in ctx.bot.guilds:
			try:
				dbguild = db.Guild.from_guild_id(guid.id)

				if dbguild.subscribed:
					for channel in guild.channels:
						if "chess" in channel.name.lower():
							try:
								await channel.send(announcement.replace("[prefix]", dbguild.prefix))
								notifs += 1
								break
							except:
								pass

			except Exception as E:
				await ctx.ch.send("ERROR: {}".format(E))
		
		await ctx.ch.send("I successfully sent {} notifications".format(notifs))


class CommandUnsubscribe(Command):
	name = "unsubscribe"
	helpstring = ["unsubscribe", "Unsubscribe your guild from notifications!"]
	flags = FLAG_MUST_BE_SERVER_OWNER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", False)
		
		await ctx.ch.send("You have unsubscribed your guild from ChessBot notifications! You can resubscribe with {}subcribe".format(ctx.prefix))

class CommandSubscribe(Command):
	name = "subscribe"
	helpstring = ["subscribe", "Subscribe your guild to notifications!"]
	flags = FLAG_MUST_BE_SERVER_OWNER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", True)
		
		await ctx.ch.send("You have subscribed your guild from ChessBot notifications!")