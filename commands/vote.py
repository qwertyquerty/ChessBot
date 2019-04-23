from command import *

class C_Vote(Command):
    name = "vote"
    helpstring = ["vote", "Vote for the bot (please) for prizes"]

    @classmethod
    async def run(self,ctx):
        await ctx.ch.send(VOTEURL)

command = C_Vote
