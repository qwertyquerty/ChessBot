from chessbot.command import *

class CommandSuggestion(Command):
    name = "suggestion"
    aliases = ["suggest"]
    help_string = "Suggest a feature, report a bug, and more"
    help_index = 260
    flags = FLAG_MUST_NOT_BE_BLACKLISTED

    @classmethod
    async def run(self,ctx):
        if len(ctx.raw_args) > 0:
            await ctx.ch.send("Suggestion sent!")
            em = discord.Embed()
            em.description=' '.join(ctx.raw_args[0:])
            em.colour = discord.Colour(EMBED_COLOR)
            em.set_author(name=str(ctx.mem), icon_url=ctx.mem.avatar_url)
            ch = await ctx.bot.fetch_channel(SUGGESTIONCHANNEL)
            msg = await ch.send(embed=em)
            await msg.add_reaction(ACCEPT_MARK)
            await msg.add_reaction(DENY_MARK)