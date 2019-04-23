from command import *

class C_Invite(Command):
    name = "invite"
    aliases = ["inv"]
    helpstring = ["invite", "Invite the bot to your server!"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("https://discordapp.com/oauth2/authorize?client_id=366770566331629579&scope=bot&permissions=8")

command = C_Invite
