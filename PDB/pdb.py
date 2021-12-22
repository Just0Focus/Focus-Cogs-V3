

#   Starting section for loading in requisites

###
#   ---   This is Init
###
#   --------------      From ch.py
import asyncio
import json
import re
from collections import Counter, defaultdict
from inspect import getfile
from itertools import chain
from os import path
from pathlib import Path
from types import MethodType

import discord
import yaml

###
#   ---   This section is Core
###
from redbot.core import commands

###
#   ---   Extended Core
###
#   --------------      From ch.py
from redbot.core import Config
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import menus, predicates
from redbot.core.utils.chat_formatting import box, pagify

###
#   ---   Exteded Init
###
#   --------------      From ch.py
from tabulate import tabulate

from . import themes
from .core import ARROWS, GLOBAL_CATEGORIES, set_menu
from .core.base_help import EMPTY_STRING, BaguetteHelp

from .core.utils import LINK_REGEX, emoji_converter

#   ---   End Of Init
###
###


# YALM Based Data structures
#
# PDB should respond in menus
#   But may have them disabled
#
# My Goal is to have sheets returned on searched fields
#
# Allow any Member add extrees
#   Entrees are stored as user data.
#           That so Entrees may be searched/purged by Member
#       But not update them
#   Updates can be Submitted
#       But must be Approved
#           Updates transfer Entree to new Member
#       Fields are only available if present in given list
#
# -----------       Wishlist
# Guild/Role based permissions
#   on
#       - DataField Lists
#       - DataField Returneds
#       - Approval
#       - Purging


#   TODO Now
# - Figure out
#       How Yalm works,
#           Making entrees
#       How to store entrees for recal

#   TODO
# Rewriting everything
# Need To: right my own code


#
#
#



#   Starting section for Functions

###
#   ---   This is
###
#   --------------      From ch.py
_ = Translator("PDB", __file__)

#   Default Structure >?
"""
Config Structure:
    {
      "profiles":
      [
            {
                "name" : name
                "level" :level
                "desc" : desc
                "long_desc":longer description
                "tags" : []
                "reaction":None

                "Av" :Av
                "Bp" :Bp
                "SDK" :SDK
                "Mk" :Mk
                "Bf" :Bf
                "Sp" :Sp
                "IPS" :IPS
                "Sc" :Sc
                "VIP" :VIP
                "Cash" :Cash
            }
     ]
    }
"""



@cog_i18n(_)
class CustomHelp(commands.Cog):
    """
    A custom customisable help for fun and profit
    """

    __version__ = "0.8.2"

    def __init__(self, bot: Red):
        self.bot = bot
        self.feature_list = {
            "category": "format_category_help",
            "main": "format_bot_help",
            "cog": "format_cog_help",
            "command": "format_command_help",
        }
        self.config = Config.get_conf(
            self,
            identifier=278198241009,
            force_registration=True,  # I'm gonna regret this
        )
        self.chelp_global = {
            "profiles": [],
            "uncategorised": {
                "name": None,
                "desc": None,
                "long_desc": None,
                "reaction": None,
            },
            "settings": {
                "react": True,
                "set_formatter": False,
                "thumbnail": None,
                "timeout": 120,
                "replies": True,
                "buttons": False,
                "deletemessage": False,
                "arrows": {
                    "right": "\N{BLACK RIGHTWARDS ARROW}\N{VARIATION SELECTOR-16}",
                    "left": "\N{LEFTWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}",
                    "cross": "\N{CROSS MARK}",
                    "home": "\U0001f3d8\U0000fe0f",
                    "force_right": "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\N{VARIATION SELECTOR-16}",
                    "force_left": "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\N{VARIATION SELECTOR-16}",
                },
            },
            "blacklist": {"blocked": [], "dev": []},
        }
        self.config.register_global(**self.chelp_global)


#   Default Structure >?
    def cog_unload(self):
        self.bot.reset_db_formatter()

    def format_db_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

#   ---   End Of Default Structure
###
###





    async def refresh_arrows(self):
        """This is to make the emoji arrows objects be in their proper types"""
        arrows = await self.config.settings.arrows()
        for name, emoji in arrows.items():
            # Just using the IDS to prevent issues with emojis missing when bot loads
            ARROWS[name] = emoji

    async def refresh_cache(self):
        """Get's the config and re-populates the GLOBAL_CATEGORIES"""
        # Blocking?
        # await self.config.clear_all()
        my_categories = await self.config.categories()
        # GLOBAL_CATEGORIES[:] = [Category(**i) for i in my_categories]
        # Correct the emoji types
        GLOBAL_CATEGORIES[:] = []
        for cat in my_categories:
            cat_obj = Category(**cat)
            cat_obj.reaction = emoji_converter(self.bot, cat_obj.reaction)
            GLOBAL_CATEGORIES.append(cat_obj)

        # make the uncategorised cogs
        all_loaded_cogs = set(self.bot.cogs.keys())
        uncategorised = all_loaded_cogs - set(
            chain(*(category["cogs"] for category in my_categories))
        )

        uncat_config = await self.config.uncategorised()
        GLOBAL_CATEGORIES.append(
            Category(
                name=uncat_config["name"] or "uncategorised",
                desc=uncat_config["desc"] or "No category commands",
                long_desc=uncat_config["long_desc"] or "",
                reaction=emoji_converter(self.bot, uncat_config["reaction"]),
                cogs=list(uncategorised),
            )
        )







class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
