from command import *

class C_Game(Command):
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

command = C_Game
