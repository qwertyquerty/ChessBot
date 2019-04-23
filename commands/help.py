from command import *

class C_Help(Command):
    name = "help"
    helpstring = ["help", "You're reading it, buddy..."]

    @classmethod
    async def run(self,ctx):
        page = 0
        if len(ctx.args) > 0:
            try:
                page = int(ctx.args[0])-1
                page = max(0, min(page, len(config.HELP)-1)) #CLAMP
            except:
                page = 0

        em = discord.Embed()
        em.title= "Help Page {}/{}".format(page+1,len(config.HELP))
        em.colour = discord.Colour(config.COLOR)
        em.type = "rich"

        for cmd,desc in config.HELP[page].items():
            em.add_field(name="{prefix}{cmd}".format(prefix=ctx.prefix,cmd=cmd),value=desc.format(prefix=ctx.prefix), inline=False)
        em.set_footer(text="{prefix}help (page)".format(prefix=ctx.prefix))

        await ctx.ch.send(embed=em)

command = C_Help
