from command import *

class C_Restart(Command):
    name = "restart"
    helpstring = ["restart [item]", "Restarts the bot, or another process"]
    level = LEVEL_OWNER

    @classmethod
    async def run(self,ctx):

        await ctx.ch.send("Attempting to restart... Saving...")

        await ctx.ch.send("Saved...")
        if len(ctx.args) > 0:
            os.system("pm2 restart "+ctx.args[0])
        else:
            os.system("pm2 restart chess")
            await ctx.bot.change_presence(status=discord.Status.dnd)

command = C_Restart
