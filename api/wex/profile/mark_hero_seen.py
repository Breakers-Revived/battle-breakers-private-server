"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles marking a hero as seen
"""

import sanic
import sanic_ext

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

compress = Compress()
wex_profile_mark_hero_seen = sanic.Blueprint("wex_profile_mark_hero_seen")


# undocumented
@wex_profile_mark_hero_seen.route("/<accountId>/MarkHeroSeen", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.MarkHeroSeen, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def mark_hero_seen(request: types.BBProfileRequest, accountId: str,
                         body: MCPValidation.MarkHeroSeen,
                         query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used in older versions of the game to mark a hero as seen. It's deprecated and replaced by item
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    await request.ctx.profile.change_item_attribute(body.model_dump().get("heroItemId"), "is_new", False,
                                                    request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
