from chessbot.command import *

class CommandUnsubscribe(Command):
	name = "unsubscribe"
	help_string = "Unsubscribe your guild from notifications"
	help_index = 500
	flags = FLAG_MUST_HAVE_PERM_MANAGE_SERVER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", False)
		
		await ctx.ch.send("You have unsubscribed your guild from ChessBot notifications! You can resubscribe with {}subcribe".format(ctx.prefix))

class CommandSubscribe(Command):
	name = "subscribe"
	help_string = "Subscribe your guild to notifications"
	help_index = 480
	flags = FLAG_MUST_HAVE_PERM_MANAGE_SERVER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", True)
		
		await ctx.ch.send("You have subscribed your guild from ChessBot notifications!")