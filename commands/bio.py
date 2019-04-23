from command import *

class C_Bio(Command):
	name = "bio"
	helpstring = ["bio <bio>", "Set your user profile bio!"]

	@classmethod
	async def run(self,ctx):
		if len(ctx.args) > 0:
			bio = ' '.join(ctx.args[0:])
			if len(bio)<=250:
				ctx.user.set("bio", bio)
				await ctx.ch.send("Bio set!")
			else:
				await ctx.ch.send('Your bio is too long! (Over 250 characters)')
		else:
			await ctx.ch.send('You must specify a bio!')

command = C_Bio
