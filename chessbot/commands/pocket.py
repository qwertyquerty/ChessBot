from chessbot.command import *

class CommandPocket(Command):
    name = "pocket"
    help_string = "View your crazyhouse pocket"
    help_index = 460
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