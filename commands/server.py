from command import *

class C_Server(Command):
    name = "server"
    helpstring = ["server", "Join the official bot server!"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(DISCORD_LINK)

command = C_Server
