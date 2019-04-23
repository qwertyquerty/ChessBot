from command import *

class C_Ping(Command):
	name = "ping"
	helpstring = ["ping", "Check latency!"]

	@classmethod
	async def run(self,ctx):
		now = datetime.datetime.utcnow()
		delta = now-ctx.message.created_at
		await ctx.ch.send(str(delta.total_seconds()*1000)+'ms')

command = C_Ping
