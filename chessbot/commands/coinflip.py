from chessbot.command import *

class CommandCoinflip(Command):
	name = "coinflip"
	help_string = "Flip a coin"
	help_index = 310
	aliases = ["cf"]

	@classmethod
	async def run(self,ctx):
		await ctx.ch.send(random.choice(["Heads", "Tails"]))