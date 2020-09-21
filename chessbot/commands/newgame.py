from chessbot.command import *

class CommandPlay(Command):
	name = "play"
	aliases = ["newgame", "ng"]
	help_string = "Start a new game against someone"
	help_index = 0
	parameters = [ParamUser(), ParamString("variant", required=False)]


	@classmethod
	async def run(self,ctx):
		if not ctx.game:
			game2 = db.Game.from_user_id(ctx.args[0].id)

			if not game2:
				if ctx.args[0].id == ctx.mem.id:
					await ctx.ch.send("You can't connect with yourself in this way. Why not take a walk?")

				else:
					variant = VARIANT_STANDARD
					if ctx.args[1] == "atomic": variant = VARIANT_ATOMIC
					elif ctx.args[1] == "koth": variant = VARIANT_KOTH
					elif ctx.args[1] == "antichess": variant = VARIANT_ANTICHESS
					elif ctx.args[1] == "crazyhouse": variant = VARIANT_CRAZYHOUSE
					elif ctx.args[1] == "horde": variant = VARIANT_HORDE
					elif ctx.args[1] == "racingkings": variant = VARIANT_RACINGKINGS
					elif ctx.args[1] == "960": variant = VARIANT_960

					rated = variant == VARIANT_STANDARD

					user2 = db.User.from_mem(ctx.args[0])
					
					if ctx.args[1] == "casual": rated = False

					if ctx.user.flags & USER_FLAG_BLACKLISTED or user2.flags & USER_FLAG_BLACKLISTED:
						rated = False

					m = await ctx.ch.send("{u1}, you are being challenged to a **{rated}** game of **{game}** by {u2}!".format(u1=ctx.args[0].mention,rated=RATED_NAMES[rated],game=VARIANT_NAMES[variant],u2=ctx.mem.mention))
												
					await m.add_reaction(ACCEPT_MARK)
					await m.add_reaction(DENY_MARK)
					try:

						def check(reaction, user):
							return user == ctx.args[0] and str(reaction) in [ACCEPT_MARK, DENY_MARK] and reaction.message.id == m.id
						reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=50)

						if str(reaction) == ACCEPT_MARK:
							await ctx.ch.trigger_typing()
							u1 = db.User.from_mem(ctx.mem)
							u2 = db.User.from_mem(ctx.args[0])
							if not db.Game.from_user_id(ctx.mem.id) and not db.Game.from_user_id(ctx.args[0].id):
								db.Game.new(u1.id, u2.id, variant=variant, rated=rated)

								if ctx.dbguild != None:
									ctx.dbguild.inc("games", 1)

								await ctx.ch.send('The game has started! Type {prefix}board to see the board!'.format(prefix=ctx.prefix))

								await ctx.bot.get_channel(config.LOGCHANNEL).send("`Create Game: "+str(u1.name)+" "+str(u2.name)+" "+str(ctx.guild.id)+"`")
								
								await update_activity(ctx.bot)

							else:
								await ctx.ch.send("{u1}, {u2} I dunno which, but one of you is already in a game!".format(u1=ctx.mem.mention,u2=ctx.args[0].mention))
						elif str(reaction) == DENY_MARK:
							await ctx.ch.send("{u1}, {u2} has declined the game request!".format(u1=ctx.mem.mention,u2=ctx.args[0].mention))
					except Exception as E:
						await ctx.ch.send("{u1}, the request has timed out!".format(u1=ctx.mem.mention))

			else:
				await ctx.ch.send('That user is currently in a game with another person!')
		else:
			await ctx.ch.send('You are already in a game! Resign it with {prefix}resign'.format(prefix=ctx.prefix))
