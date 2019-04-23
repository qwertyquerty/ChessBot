from command import *

class C_Unblacklist(Command):
    name = "unblacklist"
    helpstring = ["unblacklist", "Unblacklist a user!"]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        if len(ctx.mentions) > 0:
            db.User.from_mem(ctx.mentions[0]).unblacklist()
            await ctx.ch.send("They have been resurrected from the pit of DOOM!")
        else:
            await ctx.ch.send("Mention a user nerd.")

command = C_Unblacklist
