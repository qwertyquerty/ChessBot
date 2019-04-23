from command import *

class C_Setstatus(Command):
    name = "setstatus"
    helpstring = ["setstatus", "Set the bot's game."]
    level = LEVEL_OWNER

    @classmethod
    async def run(self,ctx):
        config.MOTD = ctx.content.replace("{prefix}setstatus".format(prefix=ctx.prefix),"").strip(" ")
        await ctx.bot.change_presence(activity=discord.Game(name=MOTD),status=discord.Status.online)
        await ctx.ch.send('Status set!')

command = C_Setstatus
