"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles adding heroes to monster pit
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_add_to_monster_pit = sanic.Blueprint("wex_profile_add_to_monster_pit")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/AddToMonsterPit.md
@wex_profile_add_to_monster_pit.route("/<accountId>/AddToMonsterPit", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def add_to_monster_pit(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to add heroes to the monster pit
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    character_item_id = request.json.get("characterItemId")
    character = await request.ctx.profile.get_item_by_guid(character_item_id)
    if not character.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    # TODO: un-equip sidekicks and gear
    await request.ctx.profile.remove_item(character_item_id)
    await request.ctx.profile.add_item(character, character_item_id, request.ctx.profile_id)
    await request.ctx.profile.modify_stat("pit_power_dirty", True, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
