from command import *

class C_Games(Command):
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
            u = db.User.from_id(int(a))
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
            em.add_field(name="{}".format(g._id), value="{} vs {} ({}) — {} Moves".format(db.User.from_id(g.white).name, db.User.from_id(g.black).name, OUTCOME_NAMES[g.outcome], math.ceil(len(db.Game.from_id(g._id).moves) / 2)), inline=False)

        await ctx.ch.send(embed=em)

command = C_Games
