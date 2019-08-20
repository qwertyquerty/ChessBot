from command import *

class C_Fen(Command):
	name = "fen"
	helpstring = ["fen [mention]", "Get the FEN of a game!"]


	@classmethod
	async def run(self,ctx):
		if ctx.mentions:
			try:
				g = db.Game.from_user_id_recent(ctx.mentions[0].id)
				await ctx.ch.send('```'+str(g.fen)+'```')
			except:
				await ctx.ch.send(ctx.mentions[0].mention+" hasn't played any games! Make one with {prefix}newgame [mention]".format(prefix=ctx.prefix))

		else:
			try:
				g = db.Game.from_user_id_recent(ctx.mem.id)
				await ctx.ch.send('```'+str(g.fen)+'```')
			except:
				await ctx.ch.send("You haven't played any games! Make one with {prefix}newgame [mention]".format(prefix=ctx.prefix))

command = C_Fen