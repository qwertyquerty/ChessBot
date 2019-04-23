from command import *

class C_Profile(Command):
	name = "profile"
	aliases = ["pf"]
	helpstring = ["profile [mention]", "View your, or someone else's profile!"]

	@classmethod
	async def run(self,ctx):
		if ctx.mentions:
			member = await ctx.bot.get_user_info(ctx.mentions[0].id)
			user = db.User.from_mem(ctx.mentions[0])

		else:
			member = await ctx.bot.get_user_info(ctx.mem.id)
			user = ctx.user


		em = discord.Embed()
		em.title=member.name
		em.set_thumbnail(url=member.avatar_url)
		em.colour = discord.Colour(user.color)
		em.type = "rich"
		if user.bio !=None:
			em.description = user.bio
		em.add_field(name="Elo",value=user.elo,inline=True)
		em.add_field(name="Wins",value=user.wins,inline=True)
		em.add_field(name="Losses",value=user.loss,inline=True)
		try:
			em.add_field(name="W/G",value=str(int((user.wins/user.games)*100))+"%",inline=True)
		except:
			em.add_field(name="W/G",value="None",inline=True)
		em.add_field(name="Draws",value=user.draws,inline=True)
		em.add_field(name="Games",value=user.games,inline=True)
		em.add_field(name="Votes",value=user.votes,inline=True)

		if len(user.badges) > 0:
			em.add_field(name="Badges",value=' '.join([config.BADGES[i] for i in user.badges]),inline=True)
		else:
			em.add_field(name="Badges",value="None",inline=True)
		await ctx.ch.send(embed=em)

command = C_Profile
