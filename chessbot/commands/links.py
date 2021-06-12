from chessbot.command import *

class CommandVote(Command):
    name = "vote"
    help_string = "Vote for the bot (please) for prizes"
    help_index = 340

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("{}\n\n{}".format(BOTVOTEURL, SERVERVOTEURL))


class CommandServer(Command):
    name = "server"
    aliases = ["support", "guild"]
    help_string = "Join the official bot server"
    help_index = 360

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(DISCORD_LINK)


class CommandInvite(Command):
    name = "invite"
    aliases = ["inv", "join"]
    help_string = "Invite the bot to your server"
    help_index = 380

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(BOT_INVITE_LINK)


class CommandDonate(Command):
    name = "donate"
    aliases = ["patreon", "money"]
    help_string = "Give me money. Please."
    help_index = 400

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send("Patreon: <https://www.patreon.com/qwertyquerty>\n\nPayPal: <http://paypal.me/qwertyquerty>\n\nCrypto:\n\n`BTC: bc1qkqy5tqdahdn70tnm42gs6qmq0hg7x5xvr87f94`\n\n`ETH: 0x75FE644Df34A95b3C5E03767AeAEe80d7B1B6ce7`")