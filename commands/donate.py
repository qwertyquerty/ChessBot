from command import *

class C_Donate(Command):
    name = "donate"
    aliases = ["patreon"]
    helpstring = ["donate", "Give me money. Please."]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("https://www.patreon.com/qwertyquerty")

command = C_Donate
