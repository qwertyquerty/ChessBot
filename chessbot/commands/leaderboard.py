from chessbot.command import *

class CommandLeaderboard(Command):
	name = "leaderboard"
	aliases = ["lb", "top"]
	help_string = "View the global rating leaderboard!"
	parameters = [ParamString("scope", required=False)]
	help_index = 160

	@classmethod
	async def run(self,ctx):
		em = discord.Embed()
		em.colour = discord.Colour(4623620)
		em.type = "rich"

		if ctx.args[0] in ["server", "local"]:
			lead = db.local_leaderboard(8, ctx.guild)
			em.title = "Local Server Leaderboard"
		else:
			lead = db.leaderboard(8)
			em.title = "Global Leaderboard"

		for i,ii in zip(lead,range(len(lead))):
			em.add_field(name=str(ii + 1), value=i["name"]+": "+str(int(round(i["rating"], 0))), inline=False)

		await ctx.ch.send(embed=em)