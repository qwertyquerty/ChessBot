from command import *

class C_Board(Command):
	name = "board"
	aliases = ["bd"]
	helpstring = ["board", "View the board!"]
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		await ctx.ch.send(content= COLOR_NAMES[ctx.game.board.turn]+" to move...", file=makeboard(ctx.game.board))

command = C_Board
