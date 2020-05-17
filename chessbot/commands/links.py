from chessbot.command import *

class CommandVote(Command):
    name = "vote"
    helpstring = ["vote", "Vote for the bot (please) for prizes"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(VOTEURL)


class CommandServer(Command):
    name = "server"
    helpstring = ["server", "Join the official bot server!"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(DISCORD_LINK)


class CommandInvite(Command):
    name = "invite"
    aliases = ["inv"]
    helpstring = ["invite", "Invite the bot to your server!"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("https://discordapp.com/oauth2/authorize?client_id=366770566331629579&scope=bot&permissions=8")


class CommandDonate(Command):
    name = "donate"
    aliases = ["patreon"]
    helpstring = ["donate", "Give me money. Please."]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("https://www.patreon.com/qwertyquerty")