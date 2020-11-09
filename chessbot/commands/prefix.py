from chessbot.command import *

class CommandPrefix(Command):
	name = "prefix"
	help_string = "Set a new prefix for your server"
	help_index = 280
	parameters = [ParamString("prefix")]
	flags = FLAG_MUST_HAVE_PERM_MANAGE_SERVER

	@classmethod
	async def run(self,ctx):
		if len(ctx.args[0]) < 3:
			del ctx.bot.prefix_cache[ctx.guild.id]
			ctx.dbguild.set("prefix", ctx.args[0])
			await ctx.ch.send("Prefix set!")
		else:
			await ctx.ch.send("That prefix is too long!")