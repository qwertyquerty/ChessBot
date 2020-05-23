from chessbot.command import *

class CommandGames(Command):
    name = "games"
    helpstring = ["games [mention]", "View a list of games a user has played."]


    @classmethod
    async def run(self, ctx):
        page = 0
        a = -1 # Not found
        if len(ctx.args) > 0:
            if (len(ctx.mentions) == 0):
                a = int(ctx.args[0])
            else:
                a = int(ctx.mentions[0].id)
				
        if a != -1 and len(str(a)) > 16 and len(str(a)) < 20:
            u = db.User.from_user_id(int(a))
            if len(ctx.args) >= 2:
                try:
                    page = int(ctx.args[1])-1
                except:
                    pass
        else:
            u = ctx.user
            if len(ctx.args) >= 1:
                try:
                    page = int(ctx.args[0])-1
                except:
                    pass

        if not u:
            await ctx.ch.send("User not found!")
            return
        gs = u.get_games()
        if len(gs) == 0:
            await ctx.ch.send("No games found!")
            return

        pages = int(math.ceil(len(gs)/PAGELENGTH))
        page = min(max(page,0), pages-1)

        em = discord.Embed()
        em.title = "{}'s games ({}/{})".format(u.name,page+1,pages)
        em.colour = discord.Colour(config.COLOR)
        em.type = "rich"

        gs = gs[page*PAGELENGTH:(page+1)*PAGELENGTH]
        for g in gs:
            em.add_field(name="{}".format(g._id), value="{} vs {} ({}) â€” {} Moves".format(db.User.from_user_id(g.white).name, db.User.from_user_id(g.black).name, OUTCOME_NAMES[g.outcome], math.ceil(len(db.Game.from_id(g._id).moves) / 2)), inline=False)

        await ctx.ch.send(embed=em)



class CommandGame(Command):
    name = "game"
    helpstring = ["game [mention/game id]", "View information about a game."]


    @classmethod
    async def run(self,ctx):
        if ctx.mentions:
            g = db.Game.from_user_id_recent(ctx.mentions[0].id)
            if not g:
                await ctx.ch.send(ctx.mentions[0].mention+" hasn't played any games!")
                return
        else:
            if len(ctx.args) > 0:
                try:
                    g = db.Game.from_id(ctx.args[0])
                    if not g:
                        await ctx.ch.send("Game not found!")
                        return
                except:
                    await ctx.ch.send("Game not found!")
                    return
            else:
                g = db.Game.from_user_id_recent(ctx.mem.id)
                if not g:
                    await ctx.ch.send("You haven't played any games!")
                    return

        await ctx.ch.send(embed=embed_from_game(g))



class CommandFen(Command):
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