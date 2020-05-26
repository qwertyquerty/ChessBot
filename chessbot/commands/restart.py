from chessbot.command import *

class CommandRestart(Command):
    name = "restart"
    helpstring = ["restart", "Restarts the bot, or another process"]
    level = LEVEL_OWNER

    @classmethod
    async def run(self,ctx):

        await ctx.ch.send("Attempting to restart... Saving...")

        await ctx.ch.send("Saved...")
        
        os.system("pm2 restart chess")
        await ctx.bot.change_presence(status=discord.Status.dnd)