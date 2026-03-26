"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles level abandon/exit profile mcp
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.utils import authorized as auth, format_time, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_abandon_level = sanic.Blueprint("wex_profile_abandon_level")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/AbandonLevel.md
@wex_profile_abandon_level.route("/<accountId>/AbandonLevel", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.AbandonLevel, query=MCPQueryValidation.MCPLevels)
@compress.compress()
async def abandon_level(request: types.BBProfileRequest, accountId: str,
                        body: MCPValidation.AbandonLevel,
                        query: MCPQueryValidation.MCPLevels) -> sanic.response.JSONResponse:
    """
    This endpoint is used to abandon the level
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    await request.ctx.profile.modify_stat("last_forgiven_abandon", await format_time(), ProfileType.LEVELS)
    await request.ctx.profile.remove_item(body.model_dump().get("levelItemId"), ProfileType.LEVELS)
    # TODO: calculate quests + handle rewards for completed rooms
    await request.ctx.profile.clear_notifications(ProfileType.LEVELS)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
