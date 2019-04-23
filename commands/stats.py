from command import *

class C_Stats(Command):
    name = "stats"
    helpstring = ["stats", "View the bot stats."]

    @classmethod
    async def run(self,ctx):
        em = discord.Embed()
        em.title = "All Systems Operational"
        em.colour = discord.Colour(config.COLOR)
        em.type = "rich"

        pingnow = datetime.datetime.utcnow()
        pingdelta = pingnow-ctx.message.created_at
        ping = pingdelta.total_seconds()*1000

        emotes = ["\U0000203c", "\U00002705"]

        uptime = int(time.time())-ctx.stats.starttime

        v = int(psutil.cpu_percent()*10)/10
        em.add_field(name="CPU Usage",value="{}% {}".format(v, emotes[v<70]))
        v = int(psutil.virtual_memory().percent*10)/10
        em.add_field(name="RAM Usage",value="{}% {}".format(v, emotes[v<70]))
        v = int(psutil.disk_usage("/").percent*10)/10
        em.add_field(name="Disk Usage",value="{}% {}".format(v, emotes[v<70]))
        v = int(ping*10)/10
        em.add_field(name="Latency",value="{}ms {}".format(v, emotes[v<300]))
        v = (ctx.stats.messages,int(((ctx.stats.messages/(uptime/60))*10))/10)
        em.add_field(name="Messages",value="{} {}/m {}".format(v[0], v[1], emotes[bool(v[1])]))
        v = (ctx.stats.commandcalls,int(ctx.stats.commandcalls/(uptime/60/60/24)))
        em.add_field(name="Calls",value="{} {}/d {}".format(v[0], v[1], emotes[bool(v[1])]))
        v = (len(ctx.bot.guilds),int((len(ctx.bot.guilds)-ctx.stats.startguilds)/(uptime/60/60/24)))
        em.add_field(name="Guilds",value="{} {}/d {}".format(v[0], v[1], emotes[bool(v[0])]))
        v = (len(ctx.bot.users), int((len(ctx.bot.users)-ctx.stats.startusers)/(uptime/60/60/24)))
        em.add_field(name="Users",value="{} {}/d {}".format(v[0], v[1], emotes[bool(v[0])]))
        v = (db.games.count(), int((db.games.count()-ctx.stats.startgames)/(uptime/60/60/24)))
        em.add_field(name="Games",value="{} {}/d {}".format(v[0], v[1], emotes[bool(v[0])]))

        await ctx.ch.send(embed=em)

command = C_Stats
