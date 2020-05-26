from chessbot.command import *

class CommandHelp(Command):
	name = "help"
	helpstring = ["help", "You're reading it, buddy..."]
	parameters = [ParamInt("page", required=False)]

	@classmethod
	async def run(self,ctx):
		if ctx.args[0]:
			page = int(ctx.args[0])-1
			page = max(0, min(page, len(HELP)-1))
		else:
			page = 0

		em = discord.Embed()
		em.title= "Help Page {}/{}".format(page+1,len(HELP))
		em.colour = discord.Colour(COLOR)
		em.type = "rich"

		for cmd,desc in HELP[page].items():
			em.add_field(name="{prefix}{cmd}".format(prefix=ctx.prefix,cmd=cmd),value=desc.format(prefix=ctx.prefix), inline=False)
		em.set_footer(text="{prefix}help (page)".format(prefix=ctx.prefix))

		await ctx.ch.send(embed=em)


class CommandAbout(Command):
	name = "about"
	helpstring = ["about", "All about me!"]

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
		em.add_field(name="Servers",value=str(len(ctx.bot.guilds)),inline=True)
		em.add_field(name="Users",value=str(sum([len(i.members) for i in ctx.bot.guilds])),inline=True)
		em.add_field(name="Support Server",value="https://discord.gg/uV5y7RY",inline=True)
		em.add_field(name="Version",value="2.5.9",inline=True)
		em.set_footer(text="Special thanks: Rapptz, niklasf, channelcat, MongoDB Inc, DBL, Aurora, And you, yes you.")
		em.url = "https://discordbots.org/bot/366770566331629579"
		await ctx.ch.send(embed=em)