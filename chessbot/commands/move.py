from chessbot.command import *

class CommandMove(Command):
	name = "move"
	aliases = ["m", "go", "g"]
	help_string = "Make a move using Long Notation, aka a2a3 to move the piece at a2 to a3. Promoting: a7a8q"
	help_index = 20
	parameters = [ParamString("move")]
	flags = FLAG_MUST_BE_IN_GAME

	@classmethod
	async def run(self,ctx):
		if ctx.mem.id == ctx.game.players[ctx.game.board.turn]:
			move = None

			# Yes I know this is a mess but there is little way to do this better, seriously
			try:
				move = chess.Move.from_uci(ctx.args[0]) # Check if the move is normal lan
				assert move in ctx.game.board.legal_moves
			except:
				try:
					move = chess.Move.from_uci(ctx.args[0]+"q") # Check if the move is lan but try promotion
					assert move in ctx.game.board.legal_moves
				except:
					try:
						move = ctx.game.board.parse_san(ctx.args[0]) # Check if the move is normal san			
					except:
						try:
							move = ctx.game.board.parse_san(ctx.args[0]+"=Q") # Check if the move is san but try promotion
						except:
							await ctx.ch.send("That move is illegal or invalid! Try something like: a2a4")
							move = None # lol

			if move:
				if move in ctx.game.board.legal_moves:
					ctx.game.board.push(move)
					ctx.game.add_move(move.uci())

					await ctx.ch.send(file=makeboard(ctx.game.board), content=ment(ctx.game.players[ctx.game.board.turn]))
					
				else:
					await ctx.ch.send("That move is illegal!")

			if ctx.game.board.is_checkmate() or ctx.game.board.is_variant_loss():
				await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_CHECKMATE, ctx.game, ctx.ch, ctx.bot)

			if type(ctx.game.board).uci_variant == "antichess" and ctx.game.board.is_variant_win():
				await reward_game(ctx.game.players[not ctx.game.players.index(ctx.mem.id)], ctx.mem.id, OUTCOME_CHECKMATE, ctx.game, ctx.ch, ctx.bot)

			if ctx.game.board.is_stalemate() or ctx.game.board.is_fivefold_repetition() or ctx.game.board.is_seventyfive_moves() or ctx.game.board.is_variant_draw() or ctx.game.board.is_insufficient_material():
				await reward_game(ctx.mem.id, ctx.game.players[not ctx.game.players.index(ctx.mem.id)], OUTCOME_DRAW, ctx.game, ctx.ch, ctx.bot)
		
		else:
			await ctx.ch.send("It is not your turn!")

		if ctx.game.board.is_check() and not ctx.game.board.is_checkmate():
			await ctx.ch.send('**Check!**')