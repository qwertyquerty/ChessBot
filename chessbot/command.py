from chessbot import config
from chessbot.config import *
from chessbot import db
from chessbot.parameter import *
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
import re
from bson.objectid import ObjectId

class Command():
    name = "command"
    flags = FLAG_NONE
    level = LEVEL_EVERYONE
    aliases = []
    enabled = True
    help_string = None
    help_index = 0
    parameters = []

    @classmethod
    async def call(self,ctx):
        if ctx.user.level < self.level:
            await ctx.ch.send("You do not have permission to run this command!")
            return

        if self.flags & FLAG_MUST_BE_IN_GAME and not ctx.game:
            await ctx.ch.send("You are not in a game! Make one with `{prefix}newgame <user>`".format(prefix=ctx.prefix))
            return

        if self.flags & FLAG_MUST_BE_SERVER_OWNER and ctx.mem != ctx.guild.owner:
            await ctx.ch.send("You must be the server owner to do this!")
            return
        
        if self.flags & FLAG_MUST_HAVE_PERM_MANAGE_SERVER and not ctx.mem.guild_permissions.manage_guild:
            await ctx.ch.send("You must have the permission `manage server` to do this!")
            return
        
        if self.flags & FLAG_MUST_NOT_BE_BLACKLISTED and ctx.user.flags & USER_FLAG_BLACKLISTED:
            await ctx.ch.send("You cannot run this command while blacklisted!")
            return         

        arg_num = 0

        for param in self.parameters:
            ctx.args.append(None)

            if len(ctx.raw_args) >= (arg_num + 1):
                arg = ctx.raw_args[arg_num]
                parsed_arg = await param.parse(ctx, arg)

                if parsed_arg == None:
                    await ctx.ch.send("Invalid input for: `{}` of type `{}`! {} **Usage:** `{}{}`".format(param.name, param.type_name, param.usage_string(), ctx.prefix, self.usage_string()))
                    return

                ctx.args[arg_num] = parsed_arg

            elif not param.required:
                ctx.args[arg_num] = None

            else:
                await ctx.ch.send("You must specify: `{}` of type `{}`! **Usage:** `{}{}`".format(param.name, param.type_name, ctx.prefix, self.usage_string()))
                return

            arg_num += 1


        await self.run(ctx)
    
    @classmethod
    def usage_string(self):
        usage_str = self.name
        for param in self.parameters:
            usage_str += " "
            if param.required:
                usage_str += "<{}>".format(param.name)
            else:
                usage_str += "[{}]".format(param.name)
        
        return usage_str

    @classmethod
    async def run(self,ctx):
        pass


