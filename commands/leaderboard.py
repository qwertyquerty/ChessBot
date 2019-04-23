from command import *

class C_Leaderboard(Command):
	name = "leaderboard"
	aliases = ["lb"]
	helpstring = ["leaderboard", "View the global elo leaderboard!"]

	@classmethod
	async def run(self,ctx):
		em = discord.Embed()
		em.colour = discord.Colour(4623620)
		em.type = "rich"

		if len(ctx.args)>0 and ctx.args[0] == "servers":
			lead = db.leaderboardguilds(8,"games")
			title = "Server Games"
			unit = "games"
		else:
			lead = db.leaderboard(8,"elo")
			title = "elo"
			unit = "elo"

		em.title = title.title()
		for i,ii in zip(lead,range(len(lead))):
			em.add_field(name=str(ii+1),value=i["name"]+": "+str(i[unit]),inline=False)

		await ctx.ch.send(embed=em)

command = C_Leaderboard
