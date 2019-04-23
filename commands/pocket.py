from command import *

class C_Pocket(Command):
    name = "pocket"
    helpstring = ["game", "View your crazyhouse pocket."]
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        if ctx.game.variant == VARIANT_CRAZYHOUSE:
            pocket = ctx.game.board.pockets[ctx.game.players.index(ctx.user.id)]
            if len(pocket.pieces) == 0:
                await ctx.ch.send("Your pocket is empty!")
            else:
                await ctx.ch.send("In your pocket: ```{}```".format(' '.join(list(str(pocket)))))
        else:
            await ctx.ch.send("You are not in a Crazyhouse game!")

command = C_Pocket
