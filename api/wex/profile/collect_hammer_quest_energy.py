"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles collecting hammer quests energy
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_collect_hammer_quest_energy = sanic.Blueprint("wex_profile_collect_hammer_quest_energy")


# undocumented
@wex_profile_collect_hammer_quest_energy.route("/<accountId>/CollectHammerQuest_Energy", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.CollectHammerQuest_Energy, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def collect_hammer_quest_energy(request: types.BBProfileRequest, accountId: str,
                                      body: MCPValidation.CollectHammerQuest_Energy,
                                      query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to collect hammer quests energy
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
