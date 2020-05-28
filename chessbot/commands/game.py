from chessbot.command import *

class CommandGames(Command):
    name = "games"
    help_string = "View a list of games a user has played"
    help_index = 180
    parameters = [ParamUser(required=False), ParamInt("page", required=False)]

    @classmethod
    async def run(self, ctx):
        mention = ctx.args[0] if ctx.args[0] else ctx.mem
        page = ctx.args[1] - 1 if ctx.args[1] else 0

        user = db.User.from_user_id(mention.id)

        if not user:
            await ctx.ch.send("No games found!")
            return

        games = user.get_games()
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
