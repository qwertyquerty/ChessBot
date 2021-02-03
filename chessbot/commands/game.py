from chessbot.command import *

class CommandGames(Command):
    name = "games"
    help_string = "View a list of games a user has played"
    help_index = 180
    parameters = [ParamUser(required=False), ParamInt("page", required=False), ParamChoice("sort", required=False, options=["moves", "rated", "wins"])]

    @classmethod
    async def run(self, ctx):
        mention = ctx.args[0] if ctx.args[0] else ctx.mem
        page = ctx.args[1] - 1 if ctx.args[1] else 0
        sort = ctx.args[2] if ctx.args[2] else "recent"

        user = db.User.from_user_id(mention.id)

        if not user:
            await ctx.ch.send("No games found!")
            return

        games = user.get_games()

        if sort == "moves":
            games.sort(key=lambda x: len(x.moves), reverse=True)
        elif sort == "rated":
            games.sort(key=lambda x: x.ranked, reverse=True)
        elif sort == "wins":
            games.sort(key=lambda x: x.winner != mention.id)

        if len(games) == 0:
            await ctx.ch.send("No games found!")
            return

        pages = int(math.ceil(len(games) / PAGELENGTH))
        page = min(max(page, 0), pages-1)

        em = discord.Embed()
        em.title = "{}'s games ({}/{})".format(user.name, page+1, pages)
        em.colour = discord.Colour(config.EMBED_COLOR)
        em.type = "rich"

        games = games[page * PAGELENGTH : (page + 1) * PAGELENGTH]
        for game in games:
            em.add_field(name="{}".format(game.id), value="{} vs {} ({}) in {} Moves".format(db.User.from_user_id(game.white).name, db.User.from_user_id(game.black).name, OUTCOME_NAMES[game.outcome].lower(), math.ceil(len(db.Game.from_id(game.id).moves) / 2)), inline=False)

        await ctx.ch.send(embed=em)


class CommandGame(Command):
    name = "game"
    help_string = "View information about a specific game"
    help_index = 200
    parameters = [ParamUnion((ParamGameID(), ParamUser()), required=False)]

    @classmethod
    async def run(self,ctx):
        game = None

        if isinstance(ctx.args[0], discord.abc.User):
            game = db.Game.from_user_id_recent(ctx.args[0].id)
            
            if not game:
                await ctx.ch.send("{} hasn't played any games!".format(ctx.args[0].mention))

        elif isinstance(ctx.args[0], str):
            game = db.Game.from_id(ctx.args[0])

            if not game:
                await ctx.ch.send("Game not found!")
        
        else:
            game = db.Game.from_user_id_recent(ctx.mem.id)

            if not game:
                await ctx.ch.send("You haven't played any games!")

        if game:
            await ctx.ch.send(embed=embed_from_game(game))


class CommandFen(Command):
    name = "fen"
    help_string = "Get the FEN of a game"
    help_index = 220
    parameters = [ParamUnion((ParamGameID(), ParamUser()), required=False)]

    @classmethod
    async def run(self,ctx):
        game = None

        if isinstance(ctx.args[0], discord.abc.User):
            game = db.Game.from_user_id_recent(ctx.args[0].id)
            
            if not game:
                await ctx.ch.send("{} hasn't played any games!".format(ctx.args[0].mention))

        elif isinstance(ctx.args[0], str):
            game = db.Game.from_id(ctx.args[0])

            if not game:
                await ctx.ch.send("Game not found!")
        
        else:
            game = db.Game.from_user_id_recent(ctx.mem.id)

            if not game:
                await ctx.ch.send("You haven't played any games!")

        if game:
            await ctx.ch.send(codeblock(str(game.fen)))


class CommandRecord(Command):
    name = "record"
    aliases = ["compare", "vs"]
    help_string = "View the win ratio between two players"
    help_index = 190
    parameters = [ParamUser("user"), ParamUser("user 2", required=False)]

    @classmethod
    async def run(self,ctx):
        if ctx.args[1]:
            user_1 = ctx.args[0]
            user_2 = ctx.args[1]
        else:
            user_1 = ctx.user
            user_2 = ctx.args[0]

        user_1_games = user_1.list_of_games()
        mutual_games = [db.Game(game) for game in user_1_games if user_2.id in game.players]

        user_1_record = 0
        user_2_record = 0

        for game in mutual_games:
            if game.outcome == OUTCOME_UNFINISHED or game.outcome == OUTCOME_EXIT:
                continue
            
            if game.outcome == OUTCOME_CHECKMATE or game.outcome == OUTCOME_RESIGN:
                if game.winner == user_1.id:
                    user_1_record += 1
                elif game.winner == user_2.id:
                    user_2_record += 1
                continue

            if game.outcome == OUTCOME_DRAW:
                user_1_record += 0.5
                user_2_record += 0.5

        em = discord.Embed()
        em.colour = discord.Colour(EMBED_COLOR)
        em.title = f"{user_1.name} vs {user_2.name}"

        em.add_field(name="Record", value=f"{user_1_record} : {user_2_record}", inline=True)
        await ctx.ch.send(embed=em)