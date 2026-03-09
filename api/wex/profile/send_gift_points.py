"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles sending gifts.
"""
import datetime

import sanic

from utils import types
from utils.utils import authorized as auth, format_time, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_send_gift = sanic.Blueprint("wex_profile_send_gift")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/QueryProfile(profile0).md
@wex_profile_send_gift.route("/<accountId>/SendGiftPoints", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def send_gift_points(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Handles the send gift point request
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    await request.ctx.profile.modify_stat("activity", {
        "a": {
            "date": await format_time(
                datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0, microsecond=0)),
            "claimed": False,
            "props": {
                "BaseBonus": 10
            }
        },
        "b": {
            "date": await format_time(datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0) - datetime.timedelta(
                days=1)),
            "claimed": True,
            "props": {
                "BaseBonus": 10
            }
        },
        "standardGift": 10
    })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
