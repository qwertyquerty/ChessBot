from chessbot.command import *

class CommandLeaderboard(Command):
	name = "leaderboard"
	aliases = ["lb"]
	helpstring = ["leaderboard", "View the global elo leaderboard!"]

	@classmethod
	async def run(self,ctx):
		em = discord.Embed()
		em.colour = discord.Colour(4623620)
		em.type = "rich"

		lead = db.leaderboard(8,"elo")

		em.title = "Global Leaderboard"
		for i,ii in zip(lead,range(len(lead))):
			em.add_field(name=str(ii + 1), value=i["name"]+": "+str(int(round(i["elo"], 0))), inline=False)

		await ctx.ch.send(embed=em)