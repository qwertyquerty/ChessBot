from command import *

class C_Move(Command):
	name = "move"
	aliases = ["m", "go", "g"]
	helpstring = ["move <LAN>", "Make a move using Long Notation, aka a2a3 to move the piece at a2 to a3. Promoting: a7a8q"]
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		if ctx.mem.id == ctx.game.players[ctx.game.board.turn]:
			if len(ctx.args) > 0:
				movecoord = ctx.args[0]

				if ctx.command in ["move", "m"]:
					try:
						move = chess.Move.from_uci(movecoord)
						if move in ctx.game.board.legal_moves:
							ctx.game.board.push(move)

							await ctx.ch.send(file=makeboard(ctx.game.board), content=ment(ctx.game.players[ctx.game.board.turn]))
							ctx.game.add_move(move.uci())

						else:
							await ctx.ch.send("That move is illegal!")
					except Exception as E:
						print(E)
						await ctx.ch.send("That move is invalid! Try something like: a2a4")

				elif ctx.command in ["go", "g"]:
					try:
						move = ctx.game.board.parse_san(movecoord)
						if move in ctx.game.board.legal_moves:
							ctx.game.board.push(move)

							await ctx.ch.send(file=makeboard(ctx.game.board), content=ment(ctx.game.players[ctx.game.board.turn]))
							ctx.game.add_move(move.uci())

						else:
							await ctx.ch.send("That move is illegal!")
					except Exception as E:
						print(E)
						await ctx.ch.send("That move is invalid! Try something like: Nf3")


				if ctx.game.board.is_checkmate() or ctx.game.board.is_variant_loss():
					await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_CHECKMATE, ctx.game,ctx.ch,ctx.bot)

				if ctx.game.board.is_stalemate() or ctx.game.board.is_fivefold_repetition() or ctx.game.board.is_seventyfive_moves() or ctx.game.board.is_variant_draw() or ctx.game.board.is_insufficient_material():
					await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_DRAW, ctx.game,ctx.ch,ctx.bot)

			else:
				await ctx.ch.send("You must specify what move you wish to make!")
		else:
			await ctx.ch.send("It is not your turn!")

		if ctx.game.board.is_check() and not ctx.game.board.is_checkmate():
			await ctx.ch.send('**Check!**')

command = C_Move
