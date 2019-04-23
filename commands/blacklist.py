from command import *

class C_Blacklist(Command):
    name = "blacklist"
    helpstring = ["blacklist", "Blacklist a user!"]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        if len(ctx.mentions) > 0:
            db.User.from_mem(ctx.mentions[0]).blacklist()
            await ctx.ch.send("They have been cast into the pit of DOOM!")
        else:
            await ctx.ch.send("Mention a user nerd.")
            
command = C_Blacklist
