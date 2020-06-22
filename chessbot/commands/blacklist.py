from chessbot.command import *

class CommandBlacklist(Command):
    name = "blacklist"
    help_string = "Blacklist a user"
    parameters = [ParamUser()]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        db.User.from_mem(ctx.args[0]).blacklist()
        await ctx.ch.send("They have been cast into the pit of DOOM!")


class CommandUnblacklist(Command):
    name = "unblacklist"
    help_string = "Unblacklist a user"
    parameters = [ParamUser()]
    level = LEVEL_ADMIN

    @classmethod
    async def run(self,ctx):
        db.User.from_mem(ctx.args[0]).unblacklist()
        await ctx.ch.send("They have been resurrected from the pit of DOOM!")



class CommandReset(Command):
    name = "reset"
    help_string = "Reset a user's profile"
    parameters = [ParamUser()]
    level = LEVEL_ADMIN
    
    @classmethod
    async def run(self,ctx):
        [g.delete() for g in db.User.from_mem(ctx.args[0]).get_games()]
        rating_sync()
        await ctx.ch.send("User has been reset!")
