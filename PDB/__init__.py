import json
from pathlib import Path

from redbot.core.bot import Red

from .pdb import PDB


async def setup(bot: Red) -> None:
    cog = PDB(bot)
    bot.add_cog(cog)
    #

    '''

    '''

    await cog._setup()
