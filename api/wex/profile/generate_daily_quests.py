"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles generating daily quests for a profile.
"""

import sanic
import sanic_ext

from utils import types
from utils.utils import authorized as auth, format_time, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_generate_daily_quests = sanic.Blueprint("wex_profile_generate_daily_quests")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/GenerateDailyQuests.md
@wex_profile_generate_daily_quests.route("/<accountId>/GenerateDailyQuests", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.GenerateDailyQuests, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def generate_daily_quests(request: types.BBProfileRequest, accountId: str,
                                body: MCPValidation.GenerateDailyQuests,
                                query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to generate daily quests for a profile, and fetch friend gift points.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    await request.ctx.profile.modify_stat("daily_quest_last_refresh", await format_time())
    # TODO: add daily quests
    # TODO: add gift point rewards from friends
    await request.ctx.profile.add_notifications({
        "type": "WExpGiftPointReward",
        "primary": True,
        "totalPoints": 0,
        "lootResult": {
            "items": []
        }
    }, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
