from command import *

class C_Coinflip(Command):
	name = "coinflip"
	helpstring = ["coinflip", "Flip a coin!"]
	aliases = ["cf"]

	@classmethod
	async def run(self,ctx):
		await ctx.ch.send(random.choice(["Heads","Tails"]))

command = C_Coinflip
