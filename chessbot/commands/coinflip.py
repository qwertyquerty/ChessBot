from chessbot.command import *

class CommandCoinflip(Command):
	name = "coinflip"
	helpstring = ["coinflip", "Flip a coin!"]
	aliases = ["cf"]

	@classmethod
	async def run(self,ctx):
		await ctx.ch.send(random.choice(["Heads", "Tails"]))