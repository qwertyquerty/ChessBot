from chessbot.command import *

class CommandLeaderboard(Command):
	name = "leaderboard"
	aliases = ["lb", "top"]
	help_string = "View the global rating leaderboard!"
	help_index = 160
	parameters = [ParamInt("page", required=False), ParamChoice("sort", required=False, options=["lowest", "highest"])]

	@classmethod
	async def run(self,ctx):
		page = ctx.args[0] - 1 if ctx.args[0] else 0
		sort = ctx.args[1] if ctx.args[1] else "highest"

		# Might be able to limit amount and only load 8 at a time, but this is easier.
		if sort == "lowest":
			lead = db.leaderboard(80, 1)
		else:
			lead = db.leaderboard(80)

		pages = int(math.ceil(len(lead) / PAGELENGTH))
		page = min(max(page, 0), pages-1)
		
		em = discord.Embed()
		em.title = "Global Leaderboard ({}/{})".format(page+1,pages)
		em.colour = discord.Colour(4623620)
		em.type = "rich"

		lead = lead[page * PAGELENGTH : (page + 1) * PAGELENGTH]

		for i,ii in zip(lead,range(len(lead))):
			em.add_field(name=str(PAGELENGTH*page+(ii + 1)), value=i["name"]+": "+str(int(round(i["rating"], 0))), inline=False)

		await ctx.ch.send(embed=em)