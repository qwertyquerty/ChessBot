from command import *

class C_Reset(Command):
    name = "reset"
    helpstring = ["reset", "Reset a user!"]
    level = LEVEL_ADMIN
    
    @classmethod
    async def run(self,ctx):
        if len(ctx.mentions):
            
            [g.delete () for g in db.User.from_mem(ctx.mentions[0]).get_games()]
            elo_sync()
            await ctx.ch.send("User has been reset!")
        else:
            await ctx.ch.send("Mention a user nerd.")

command = C_Reset


