"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles selecting a hammer chest
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_select_hammer_chest = sanic.Blueprint("wex_profile_select_hammer_chest")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SelectHammerChest.md
@wex_profile_select_hammer_chest.route("/<accountId>/SelectHammerChest", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def select_hammer_chest(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to select a hammer chest to begin the unlock process
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    chest_item = await request.ctx.profile.get_item_by_guid(request.json.get("chestId"))
    if chest_item is None or not chest_item.get("templateId").startswith("HammerChest:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid chest ID")
    await request.ctx.profile.modify_stat("active_hammer_chest", request.json.get("chestId"))
    other_chests = await request.ctx.profile.find_items_by_type("HammerChest")
    for other_chests_id in other_chests:
        if other_chests_id != request.json.get("chestId"):
            await request.ctx.profile.remove_item(other_chests_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
