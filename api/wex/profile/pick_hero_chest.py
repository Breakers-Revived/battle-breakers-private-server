"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles picking a hero chest.
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_pick_hero_chest = sanic.Blueprint("wex_profile_pick_hero_chest")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/PickHeroChest.md
@wex_profile_pick_hero_chest.route("/<accountId>/PickHeroChest", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.PickHeroChest, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def pick_hero_chest(request: types.BBProfileRequest, accountId: str,
                          body: MCPValidation.PickHeroChest,
                          query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to pick a hero chest.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    tower_data = await request.ctx.profile.get_item_by_guid(request_body.get("towerId"))
    if tower_data is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid tower id")
    active_chest = tower_data["attributes"]["chest_options"][0]
    active_chest["heroChestType"] = request_body.get("heroChestType")
    if active_chest["heroTrackId"] != request_body.get("heroTrackId"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero track id")
    await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "active_chest", active_chest)
    if tower_data["attributes"]["chest_info_content_version"] != "1.88.244-r17036752":
        await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "chest_info_content_version",
                                                        "1.88.244-r17036752")
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
