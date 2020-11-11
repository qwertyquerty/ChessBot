from chessbot.command import *

class CommandProfile(Command):
	name = "profile"
	aliases = ["pf", "me"]
	help_string = "View your profile, or someone else's profile"
	help_index = 140
	parameters = [ParamUser(required=False)]

	@classmethod
	async def run(self,ctx):
		mention = ctx.args[0] if ctx.args[0] else ctx.mem

		user = db.User.from_mem(mention)

		em = discord.Embed()
		em.title=mention.name
		em.set_thumbnail(url=mention.avatar_url)
		em.colour = discord.Colour(EMBED_COLOR)
		em.type = "rich"
		if user.bio != None:
			em.description = user.bio
		em.add_field(name="Rating", value=int(round(user.rating, 0)), inline=True)
		em.add_field(name="Rank", value="#{}".format(user.get_rank()+1), inline=True)
		em.add_field(name="Wins", value=user.win_count(), inline=True)
		em.add_field(name="Losses", value=user.loss_count(), inline=True)
		try:
			em.add_field(name="W/G", value=str(int((user.win_count()/user.game_count())*100))+"%", inline=True)
		except:
			em.add_field(name="W/G", value="None", inline=True)
		em.add_field(name="Draws", value=user.draw_count(), inline=True)
		em.add_field(name="Games", value=user.game_count(), inline=True)
		em.add_field(name="Votes", value=user.votes, inline=True)

		if len(user.badges()) > 0:
			em.add_field(name="Badges",value=' '.join([config.BADGES[i] for i in user.badges()]),inline=True)
		else:
			em.add_field(name="Badges",value="None",inline=True)
		await ctx.ch.send(embed=em)



class CommandBio(Command):
	name = "bio"
	help_string = "Set your user profile bio!"
	help_index = 240

	@classmethod
	async def run(self,ctx):
		if len(ctx.raw_args) > 0:
			bio = ' '.join(ctx.raw_args[0:])
			if len(bio)<=250:
				ctx.user.set("bio", bio)
				await ctx.ch.send("Bio set!")
			else:
				await ctx.ch.send('Your bio is too long! (Over 250 characters)')
		else:
			await ctx.ch.send('You must specify a bio!')