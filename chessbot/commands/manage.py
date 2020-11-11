from chessbot.command import *

class CommandForce(Command):
	name = "force"
	help_string = "Force a game to end"
	parameters = [ParamGameID(), ParamChoice("outcome", options=["exit", "resign", "draw"]), ParamUser("winner", required=False)]
	level = LEVEL_ADMIN

	@classmethod
	async def run(self,ctx):
		game = db.Game.from_id(ctx.args[0])

		if not game:
			return await ctx.ch.send("Game not found!")
		
		if game.outcome != OUTCOME_UNFINISHED:
			return await ctx.ch.send("Game already ended!")
		
		if ctx.args[1] == "exit":
			return await reward_game(game.p1, game.p2, OUTCOME_EXIT, game, ctx.ch, ctx.bot)
		
		elif ctx.args[1] == "draw":
			return await reward_game(game.p1, game.p2, OUTCOME_DRAW, game, ctx.ch, ctx.bot)
		
		elif ctx.args[1] == "resign":
			if ctx.args[2] != None:
				if ctx.args[2].id not in game.players:
					return await ctx.ch.send("That user isn't a player in this game!")

				return await reward_game(ctx.args[2].id, game.players[not game.players.index(ctx.args[2].id)], OUTCOME_RESIGN, game, ctx.ch, ctx.bot)
			
			else:
				return await ctx.ch.send("You must specify a winner!") 