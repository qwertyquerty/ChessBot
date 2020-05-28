from chessbot.command import *

class C_Setstatus(Command):
    name = "setactivity"
    help_string = "Set the bot's activity for all shards"
    level = LEVEL_OWNER

    @classmethod
    async def run(self,ctx):
        config.MOTD = ctx.content.replace("{prefix}setactivity".format(prefix=ctx.prefix),"").strip(" ")
        await ctx.bot.change_presence(activity=discord.Game(name=config.MOTD),status=discord.Status.online)
        await ctx.ch.send('Activity set!')