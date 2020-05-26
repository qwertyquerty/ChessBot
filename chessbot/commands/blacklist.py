from chessbot.command import *

class CommandBlacklist(Command):
    name = "blacklist"
    helpstring = ["blacklist", "Blacklist a user!"]
    parameters = [ParamUser()]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        db.User.from_mem(ctx.mentions[0]).blacklist()
        await ctx.ch.send("They have been cast into the pit of DOOM!")


class CommandUnblacklist(Command):
    name = "unblacklist"
    helpstring = ["unblacklist", "Unblacklist a user!"]
    parameters = [ParamUser()]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        db.User.from_mem(ctx.mentions[0]).unblacklist()
        await ctx.ch.send("They have been resurrected from the pit of DOOM!")



class CommandReset(Command):
    name = "reset"
    helpstring = ["reset", "Reset a user!"]
    parameters = [ParamUser()]
    level = LEVEL_ADMIN
    
    @classmethod
    async def run(self,ctx):
        [g.delete() for g in db.User.from_mem(ctx.mentions[0]).get_games()]
        elo_sync()
        await ctx.ch.send("User has been reset!")
