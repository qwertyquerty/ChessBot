from command import *

class C_Badge(Command):
	name = "badge"
	helpstring = ["badge <emote>", "View a badge name!"]

	@classmethod
	async def run(self,ctx):
		if len(ctx.args) > 0:
			try:
				await ctx.ch.send([key for key, value in config.BADGES.items() if value == ctx.args[0]][0].replace("-"," ").title())
			except:
				await ctx.ch.send('Badge not found!')
		else:
			await ctx.ch.send('You must specify a badge as an emoji!')

command = C_Badge
