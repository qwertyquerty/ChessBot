from chessbot.command import *

class CommandPing(Command):
    name = "ping"
    help_string = "Check the bot's latency"
    help_index = 300

    @classmethod
    async def run(self,ctx):
        now = datetime.datetime.utcnow()
        delta = now-ctx.message.created_at
        await ctx.ch.send(str(delta.total_seconds()*1000)+'ms')



class CommandStats(Command):
    name = "stats"
    help_string = "View some stats about the bot"
    help_index = 320

    @classmethod
    async def run(self,ctx):
        em = discord.Embed()
        em.title = "All Systems Operational"
        em.colour = discord.Colour(EMBED_COLOR)
        em.type = "rich"

        pingnow = datetime.datetime.utcnow()
        pingdelta = pingnow-ctx.message.created_at
        ping = pingdelta.total_seconds()*1000

        emotes = ["\U0000203c", "\U00002705"]

        v = int(psutil.cpu_percent()*10)/10
        em.add_field(name="CPU Usage",value="{}% {}".format(v, emotes[v<70]))

        v = int(psutil.virtual_memory().percent*10)/10
        em.add_field(name="RAM Usage",value="{}% {}".format(v, emotes[v<80]))

        v = int(ping*10)/10
        em.add_field(name="Latency",value="{}ms {}".format(v, emotes[v<300]))

        v = db.games.count()
        em.add_field(name="Games",value="{} {}".format(v, emotes[bool(v)]))

        em.add_field(name="Processes",value="{} ({})".format(PROCESSES, ctx.bot.pid))

        em.add_field(name="Shards",value="{} ({})".format(str(ctx.bot.shard_ids), ctx.guild.shard_id))

        await ctx.ch.send(embed=em)


class CommandAnalytics(Command):
    name = "analytics"
    help_string = "View the bot's analytics"
    parameters = [ParamInt("days", required=False)]
    level = LEVEL_MOD

    @classmethod
    async def run(self,ctx):
        em = discord.Embed()
        
        em.colour = discord.Colour(EMBED_COLOR)
        em.type = "rich"

        days_ago = 30

        if ctx.args[0]: days_ago = ctx.args[0]

        em.title = "ChessBot Analytics (Past {} Days)".format(days_ago)

        games = db.games.find({"timestamp": {"$gte": datetime.datetime.now() - datetime.timedelta(days_ago)}})
        num_games = games.count()

        em.add_field(name="Games", value="{} ({}/d)".format(num_games, int(round(num_games/days_ago, 0))))

        
        total_moves = 0

        active_users = []

        for game in games:
            if game["1"] not in active_users: active_users.append(game["1"])
            if game["2"] not in active_users: active_users.append(game["2"])

            total_moves += len(game["moves"])

        em.add_field(name="Active Users", value="{}".format(len(active_users)))

        em.add_field(name="Total Moves", value="{} ({}/d {}/g)".format(total_moves, int(round(total_moves/days_ago, 0)), int(round(total_moves/num_games, 0))))


        await ctx.ch.send(embed=em)