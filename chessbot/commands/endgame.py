from chessbot.command import *

class CommandResign(Command):
	name = "resign"
	aliases = ["forfeit"]
	helpstring = ["resign", "Resign your game."]
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		await reward_game(ctx.game.players[not ctx.game.players.index(ctx.mem.id)], ctx.mem.id, OUTCOME_RESIGN, ctx.game,ctx.ch,ctx.bot)


class CommandExit(Command):
    name = "exit"
    helpstring = ["exit", "Exit a game as if it were not ranked. ONLY USE THIS IF YOUR OPPONENT IS CHEATING OR WAITING YOU OUT. ABUSE WILL LEAD TO A BLACKLIST!"]
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        await reward_game(ctx.game.players[not ctx.game.players.index(ctx.mem.id)], ctx.mem.id, OUTCOME_EXIT, ctx.game,ctx.ch,ctx.bot)


class CommandDraw(Command):
    name = "draw"
    helpstring = ["draw", "Request to draw a game."]
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        m = await ctx.ch.send("{u1}, you are being offered a draw from {u2}!".format(u1=ment(ctx.game.players[not ctx.game.players.index(ctx.mem.id)]),u2=str(ctx.mem.mention)))
        await m.add_reaction(ACCEPT_MARK)
        await m.add_reaction(DENY_MARK)

        try:
            def check(reaction, user):
                return user.id == ctx.game.players[not ctx.game.players.index(ctx.mem.id)] and str(reaction) in [ACCEPT_MARK, DENY_MARK] and reaction.message.id == m.id

            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=15)

            if str(reaction) == ACCEPT_MARK:
                await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_DRAW, ctx.game,ctx.ch,ctx.bot)

            elif str(reaction) == DENY_MARK:
                await ctx.ch.send("You have declined the draw request!")

        except Exception as E:
            await ctx.ch.send("The request has timed out!")