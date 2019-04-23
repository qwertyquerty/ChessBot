from command import *

class C_Draw(Command):
    name = "draw"
    helpstring = ["draw", "Request to draw a game."]
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        m = await ctx.ch.send("{u1}, you are being offered a draw from {u2}!".format(u1=ment(ctx.game.players[not ctx.game.players.index(ctx.mem.id)]),u2=str(ctx.mem.mention)))
        await m.add_reaction(config.ACCEPT_MARK)
        await m.add_reaction(config.DENY_MARK)

        try:
            def check(reaction, user):
                return user.id == ctx.game.players[not ctx.game.players.index(ctx.mem.id)] and str(reaction) in [config.ACCEPT_MARK, config.DENY_MARK] and reaction.message.id == m.id

            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=15)

            if str(reaction) == config.ACCEPT_MARK:
                await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_DRAW, ctx.game,ctx.ch,ctx.bot)

            elif str(reaction) == config.DENY_MARK:
                await ctx.ch.send("You have declined the draw request!")

        except Exception as E:
            await ctx.ch.send("The request has timed out!")

command = C_Draw
