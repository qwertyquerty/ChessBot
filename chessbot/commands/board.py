from chessbot.command import *

class CommandBoard(Command):
	name = "board"
	aliases = ["bd"]
	help_string = "View the game board"
	help_index = 40
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		await ctx.ch.send(COLOR_NAMES[ctx.game.board.turn]+" to move...", file=makeboard(ctx.game.board))