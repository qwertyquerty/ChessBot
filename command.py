import discord
import chess
import db
import config
from config import *
from util import *
import random
import psutil
import datetime
import time
import traceback
import ctypes
import os
import math
import sys
from io import StringIO
import gc

class Command():
    name = "command"
    flags = FLAG_NONE
    level = LEVEL_EVERYONE
    aliases = []
    enabled = True
    helpstring = ["{prefix}command", "runs the command"]

    @classmethod
    async def call(self,ctx):
        if ctx.user.level < self.level:
            await ctx.ch.send("You do not have permission to run this command!")
            return

        if self.flags & FLAG_MUST_BE_IN_GAME and not ctx.game:
            await ctx.ch.send('You are not in a game! Make one with `{prefix}newgame [mention]`'.format(prefix=ctx.prefix))
            return

        if self.flags & FLAG_MUST_BE_SERVER_OWNER and ctx.mem != ctx.guild.owner:
            await ctx.ch.send("You must be the server owner to do this!")
            return


        await self.run(ctx)

    @classmethod
    async def run(self,ctx):
        pass
