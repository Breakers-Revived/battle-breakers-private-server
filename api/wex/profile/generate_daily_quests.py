"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles generating daily quests for a profile.
"""

import sanic

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, format_time

compress = Compress()
wex_profile_generate_daily_quests = sanic.Blueprint("wex_profile_generate_daily_quests")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/GenerateDailyQuests.md
@wex_profile_generate_daily_quests.route("/<accountId>/GenerateDailyQuests", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def generate_daily_quests(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to generate daily quests for a profile, and fetch friend gift points.
    :param request: The request object
    :param accountId: The account id
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
                                                     request.ctx.profile_revisions)
    )
