from chessbot.command import *

class CommandHelp(Command):
	name = "help"
	aliases = ["commands"]
	help_string = "You're reading it, buddy..."
	parameters = [ParamInt("page", required=False)]
	help_index = 440

	@classmethod
	async def run(self,ctx):

		available_commands = [command for command in Command.__subclasses__() if command.level == LEVEL_EVERYONE]

		sorted_commands = sorted(available_commands, key = lambda x: x.help_index)

		pages = math.ceil(len(sorted_commands) / PAGELENGTH)

		if ctx.args[0]:
			page = max(1, min(ctx.args[0], pages))
		else:
			page = 1

		em = discord.Embed()
		em.title= "Help Page {}/{}".format(page, pages)
		em.colour = discord.Colour(EMBED_COLOR)
		em.type = "rich"

		for command in sorted_commands[(page - 1) * PAGELENGTH : (page - 1) * PAGELENGTH + PAGELENGTH]:
			if ctx.user.level >= command.level:
				em.add_field(name = "{}{}".format(ctx.prefix, command.usage_string()), value = command.help_string, inline=False)

		em.set_footer(text="{}{}".format(ctx.prefix, self.usage_string()))

		await ctx.ch.send(embed=em)


class CommandAbout(Command):
	name = "about"
	help_string = "All about me"
	help_index = 420

	@classmethod
	async def run(self,ctx):
		em = discord.Embed()
		em.title="About Chess"
		em.set_thumbnail(url=ctx.bot.user.avatar_url)
		em.colour = discord.Colour(4623620)
		em.type = "rich"

		em.description = "A bot for playing a Chess game in your server with ease. Challenge your friends to fight to the death."
		em.add_field(name="Creator",value="qwerty#6768",inline=True)
		em.add_field(name="Help Command",value="`{}help`".format(ctx.prefix),inline=True)
		em.add_field(name="Games",value=str(db.games.count()),inline=True)
		em.add_field(name="Players",value=str(db.users.count()),inline=True)
		em.add_field(name="Support Server",value="https://discord.gg/uV5y7RY",inline=True)
		em.add_field(name="Version",value="3.0.0",inline=True)
		em.set_footer(text="Special thanks: Rapptz, niklasf, channelcat, MongoDB Inc, DBL, Aurora, And you, yes you.")
		em.url = "https://discordbots.org/bot/366770566331629579"
		await ctx.ch.send(embed=em)


class CommandVariants(Command):
    name = "variants"
    aliases = ["variants", "gamemodes"]
    help_string = "Get a list of the variants the bot allows"
    help_index = 410

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("__**List of Variants:**__\n{}".format("\n".join(VARIANT_NAMES)))