from chessbot.command import *

class CommandBlacklist(Command):
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



class CommandUnblacklist(Command):
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



class CommandReset(Command):
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
