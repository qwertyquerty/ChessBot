from chessbot import config
from chessbot.config import *
from chessbot import db
from chessbot.util import *

import discord
import chess
import random
import psutil
import datetime
import time
import traceback
import os
import math
import sys
import re
from bson.objectid import ObjectId
from io import StringIO

class Command():
    name = "command"
    flags = FLAG_NONE
    level = LEVEL_EVERYONE
    aliases = []
    enabled = True
    helpstring = ["{prefix}command", "runs the command"]
    parameters = []

    @classmethod
    async def call(self,ctx):
        if ctx.user.level < self.level:
            await ctx.ch.send("You do not have permission to run this command!")
            return

        if self.flags & FLAG_MUST_BE_IN_GAME and not ctx.game:
            await ctx.ch.send("You are not in a game! Make one with `{prefix}newgame [mention]`".format(prefix=ctx.prefix))
            return

        if self.flags & FLAG_MUST_BE_SERVER_OWNER and ctx.mem != ctx.guild.owner:
            await ctx.ch.send("You must be the server owner to do this!")
            return
        
        arg_num = 0

        for param in self.parameters:
            ctx.args.append(None)

            if len(ctx.raw_args) >= (arg_num + 1):
                arg = ctx.raw_args[arg_num]
                parsed_arg = param.parse(ctx, arg)

                if parsed_arg == None:
                    await ctx.ch.send("Invalid input for: `{}` of type `{}`".format(param.name, param.type_name))
                    return

                ctx.args[arg_num] = parsed_arg

            elif not param.required:
                ctx.args[arg_num] = None

            else:
                await ctx.ch.send("You must specify: `{}` of type `{}`".format(param.name, param.type_name))
                return

            arg_num += 1


        await self.run(ctx)

    @classmethod
    async def run(self,ctx):
        pass


class Parameter():
    type_name = "object"
    name = "arg"
    required = True

    def __init__(self, name = None, required = True):
        self.required = required
        if name:
            self.name = name
    
    def parse(self, ctx, arg):
        return None

class ParamUser(Parameter):
    type_name = "user"
    name = "user"

    def parse(self, ctx, arg):
        mention_re = re.search(r"^<@!?(\d+)>$", arg)
        id_re = re.search(r"^(\d+)$", arg)

        id = None

        if mention_re:
            id = mention_re.group(1)
        elif id_re:
            id = id_re.group(1)
        
        try:
            id = int(id)
        except:
            id = None
        
        return ctx.bot.get_user(id)

class ParamGameID(Parameter):
    type_name = "game_id"
    name = "game"

    def parse(self, ctx, arg):
        try:
            ObjectId(arg)
            return arg
        except:
            return None

class ParamString(Parameter):
    type_name = "text"
    name = "text"

    def parse(self, ctx, arg):
        return str(arg)

class ParamInt(Parameter):
    type_name = "number"
    name = "number"

    def parse(self, ctx, arg):
        try:
            return int(arg)
        except:
            return None

# This is probably a terrible idea, still think I'm a genius for it though
# You know you're doing something wrong when you self roll type unions
class ParamUnion(Parameter):
    name = "query"
    def __init__(self, params, name=None, required=False):
        super(ParamUnion, self).__init__(name, required)

        self.params = params
        self.type_name = "/".join([param.type_name for param in self.params])
    
    def parse(self, ctx, arg):
        for param in self.params:
            parsed = param.parse(ctx, arg)
            if parsed:
                return parsed
        
        return None