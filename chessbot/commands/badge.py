from chessbot.command import *

class CommandBadge(Command):
	name = "badge"
	helpstring = ["badge <emoji>", "View a badge name!"]
	parameters = [ParamString("emoji")]

	@classmethod
	async def run(self,ctx):
		try:
			await ctx.ch.send([key for key, value in config.BADGES.items() if value == ctx.args[0]][0].replace("-"," ").title())
		except:
			await ctx.ch.send('Badge not found!')
