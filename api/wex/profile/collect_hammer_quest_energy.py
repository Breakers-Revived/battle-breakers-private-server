"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles collecting hammer quests energy
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_collect_hammer_quest_energy = sanic.Blueprint("wex_profile_collect_hammer_quest_energy")


# undocumented
@wex_profile_collect_hammer_quest_energy.route("/<accountId>/CollectHammerQuest_Energy", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def collect_hammer_quest_energy(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to collect hammer quests energy
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
