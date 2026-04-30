"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles removing a hero from the monster pit
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_remove_from_monster_pit = sanic.Blueprint("wex_profile_remove_from_monster_pit")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/RemoveFromMonsterPit.md
@wex_profile_remove_from_monster_pit.route("/<accountId>/RemoveFromMonsterPit", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.RemoveFromMonsterPit, query=MCPQueryValidation.MCPMonsterpit)
@compress.compress()
async def remove_from_monster_pit(request: types.BBProfileRequest, accountId: str,
                                  body: MCPValidation.RemoveFromMonsterPit,
                                  query: MCPQueryValidation.MCPMonsterpit) -> sanic.response.JSONResponse:
    """
    This endpoint is used to remove a hero from the monster pit
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    character_item_id = body.model_dump().get("characterItemId")
    character = await request.ctx.profile.get_item_by_guid(character_item_id, request.ctx.profile_id)
    if not character.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    await request.ctx.profile.consume_mtx(50)
    await request.ctx.profile.remove_item(character_item_id, request.ctx.profile_id)
    await request.ctx.profile.add_item(character, character_item_id)
    # This isnt done on the original server, but imo it should be
    await request.ctx.profile.change_item_attribute(character_item_id, "is_new", True)
    await request.ctx.profile.modify_stat("pit_power_dirty", True, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
