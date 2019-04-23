from command import *

class C_Listserver(Command):
    name = "listserver"
    aliases = ["ls"]
    helpstring = ["listserver", "List your server invite in the ChessBot server!"]
    flags = FLAG_MUST_BE_SERVER_OWNER

    @classmethod
    async def run(self,ctx):

        dbguild = db.Guild.from_guild(ctx.guild)

        try:
            inv = await ctx.ch.create_invite()
            await ctx.bot.get_channel(433475984751329283).send(str(inv))
            dbguild.set("listed",True)
            await ctx.ch.send("Server listed!")
        except Exception as E:
            await ctx.ch.send("I do not have permission to make an invite link in this channel!")


command = C_Listserver
