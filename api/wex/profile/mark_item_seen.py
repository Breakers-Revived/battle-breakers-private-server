"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles marking an item as seen
"""

import sanic

from utils import types
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_mark_item_seen = sanic.Blueprint("wex_profile_mark_item_seen")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/MarkItemSeen.md
@wex_profile_mark_item_seen.route("/<accountId>/MarkItemSeen", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def mark_item_seen(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to mark an item as seen
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    await request.ctx.profile.change_item_attribute(request.json.get("itemId"), "is_new", False, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
