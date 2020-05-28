from chessbot.command import *

class CommandUnsubscribe(Command):
	name = "unsubscribe"
	helpstring = ["unsubscribe", "Unsubscribe your guild from notifications!"]
	flags = FLAG_MUST_HAVE_PERM_MANAGE_SERVER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", False)
		
		await ctx.ch.send("You have unsubscribed your guild from ChessBot notifications! You can resubscribe with {}subcribe".format(ctx.prefix))

class CommandSubscribe(Command):
	name = "subscribe"
	helpstring = ["subscribe", "Subscribe your guild to notifications!"]
	flags = FLAG_MUST_HAVE_PERM_MANAGE_SERVER

	@classmethod
	async def run(self,ctx):
		ctx.dbguild.set("subscribed", True)
		
		await ctx.ch.send("You have subscribed your guild from ChessBot notifications!")