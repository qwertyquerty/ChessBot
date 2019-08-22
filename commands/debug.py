from command import *

class C_Debug(Command):
    name = "debug"
    helpstring = ["debug", "Debug command for developers!"]
    aliases = ["debug", "exec", "await", "oof"]
    level = LEVEL_OWNER

    @classmethod
    async def run(self,ctx):
        user = ctx.user
        guild = ctx.guild
        ch = ctx.ch
        msg = ctx.msg
        dbguild = ctx.dbguild
        game = ctx.game
        if ctx.command == "exec":
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()

            try:
                exec(ctx.content.replace(ctx.prefix+ctx.command+" ",""))
                o = redirected_output.getvalue()
                if o != "":
                    await ctx.ch.send(codeblock(o))
                else:
                    await ctx.ch.send(codeblock("No output!"))
            except Exception as E:
                await ctx.ch.send(codeblock(traceback.format_exc()))

            sys.stdout = old_stdout

        elif ctx.command == "debug":
            try:
                o = eval(ctx.content.replace(ctx.prefix+ctx.command+" ",""))
                await ctx.ch.send(codeblock(o))
            except Exception as E:
                await ctx.ch.send(codeblock(traceback.format_exc()))

        elif ctx.command == "await":
            try:
                o = await eval(ctx.content.replace(ctx.prefix+ctx.command+" ",""))
                await ctx.ch.send(codeblock(o))
            except Exception as E:
                await ctx.ch.send(codeblock(traceback.format_exc()))
        
        elif ctx.command == "oof":
            await ctx.ch.send("im doin it")
            i = 0
            for g in ctx.bot.guilds:
                if len(g.members) > 20:
                    continue
                gg = db.Guild.from_id(g.id)
                if gg:
                    if gg.calls > 5:
                        continue
                i += 1
                await g.leave()
                if gg:
                    gg.delete()
            await ctx.ch.send(str(i))


command = C_Debug
