from command import *

class C_Exit(Command):
    name = "exit"
    helpstring = ["exit", "Exit a game as if it were not ranked. ONLY USE THIS IF YOUR OPPONENT IS CHEATING OR WAITING YOU OUT. ABUSE WILL LEAD TO A BLACKLIST!"]
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        await reward_game(ctx.game.players[not ctx.game.players.index(ctx.mem.id)], ctx.mem.id, OUTCOME_EXIT, ctx.game,ctx.ch,ctx.bot)

command = C_Exit
