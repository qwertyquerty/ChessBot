from chessbot.command import *

class CommandTournament(Command):
	name = "tournament"
	aliases = ["tnmt"]
	help_string = "Start a tournament game"
	parameters = [ParamUser("p1"), ParamUser("p2"), ParamInt("game")]
	level = LEVEL_OWNER

	@classmethod
	async def run(self,ctx):
		cbguild = ctx.bot.get_guild(CHESSBOTSERVER)

		p1mem = ctx.guild.get_member(ctx.args[0].id)
		p2mem = ctx.guild.get_member(ctx.args[1].id)

		if not p1mem:
			await ctx.ch.send("p1 left the server")
		if not p2mem:
			await ctx.ch.send("p2 left the server")
		
		if (not p1mem) or (not p2mem):
			return

		overwrites = {
			cbguild.default_role: discord.PermissionOverwrite(send_messages=False),
			p1mem: discord.PermissionOverwrite(send_messages=True),
			p2mem: discord.PermissionOverwrite(send_messages=True)
		}

		category = cbguild.get_channel(715245810425659403)

		channel = await cbguild.create_text_channel("game-{}".format(ctx.args[2]), category = category, overwrites = overwrites)

		await channel.send("**{p1} VS {p2}**\n\nYou have 3 days to complete your game! Use the `{prefix}coinflip` command to decide who will play white. Then use the `{prefix}newgame <mention>` command to start the game! Whoever does the `{prefix}newgame` command will be white! If the game results in a *draw*, **replay the game until there is a clear win.**\n\n***All games will be checked for cheating.***\n\n**Observers:** No recommending moves through reactions or other channels!! Doing so will lead to a ban.\n**Players:** You may not use outside assistance in any way. Doing so will lead to a loss and a blacklist.\n\nWhen you complete your game: run the command `{prefix}game`, ping qwerty and then **stop talking in the channel.**".format(p1=p1mem.mention, p2=p2mem.mention, prefix=ctx.prefix))

		await ctx.ch.send("Game **{}** started in: {}".format(ctx.args[2], channel.mention))

class CommandArchive(Command):
	name = "archive"
	help_string = "Archive a tournament game"
	level = LEVEL_OWNER

	@classmethod
	async def run(self,ctx):
		cbguild = ctx.bot.get_guild(CHESSBOTSERVER)

		archived_cat = cbguild.get_channel(715616342283255818)

		await ctx.ch.edit(category = archived_cat, overwrites = {}, sync_permissions = True)

		await ctx.ch.send("Archived.")