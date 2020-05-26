from chessbot.command import *

class CommandProfile(Command):
	name = "profile"
	aliases = ["pf"]
	helpstring = ["profile [mention]", "View your, or someone else's profile!"]
	parameters = [ParamUser(required=False)]

	@classmethod
	async def run(self,ctx):
		mention = ctx.args[0] if ctx.args[0] else ctx.mem

		user = db.User.from_user_id(mention.id)

		em = discord.Embed()
		em.title=mention.name
		em.set_thumbnail(url=mention.avatar_url)
		em.colour = discord.Colour(EMBED_COLOR)
		em.type = "rich"
		if user.bio !=None:
			em.description = user.bio
		em.add_field(name="Elo", value=int(round(user.elo, 0)), inline=True)
		em.add_field(name="Rank", value="#{}".format(user.get_rank()+1), inline=True)
		em.add_field(name="Wins", value=user.wins, inline=True)
		em.add_field(name="Losses", value=user.loss, inline=True)
		try:
			em.add_field(name="W/G", value=str(int((user.wins/user.games)*100))+"%", inline=True)
		except:
			em.add_field(name="W/G", value="None", inline=True)
		em.add_field(name="Draws", value=user.draws, inline=True)
		em.add_field(name="Games", value=user.games, inline=True)
		em.add_field(name="Votes", value=user.votes, inline=True)

		if len(user.badges) > 0:
			em.add_field(name="Badges",value=' '.join([config.BADGES[i] for i in user.badges]),inline=True)
		else:
			em.add_field(name="Badges",value="None",inline=True)
		await ctx.ch.send(embed=em)



class CommandBio(Command):
	name = "bio"
	helpstring = ["bio <bio>", "Set your user profile bio!"]

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