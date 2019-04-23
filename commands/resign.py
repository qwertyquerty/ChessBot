from command import *

class C_Resign(Command):
	name = "resign"
	aliases = ["forfeit"]
	helpstring = ["resign", "Resign your game."]
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		await reward_game(ctx.game.players[not ctx.game.players.index(ctx.mem.id)], ctx.mem.id, OUTCOME_RESIGN, ctx.game,ctx.ch,ctx.bot)

command = C_Resign
