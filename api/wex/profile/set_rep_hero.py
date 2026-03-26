"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles setting friend hero
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_set_rep_hero = sanic.Blueprint("wex_profile_set_rep_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SetRepHero.md
@wex_profile_set_rep_hero.route("/<accountId>/SetRepHero", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.SetRepHero, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def set_rep_hero(request: types.BBProfileRequest, accountId: str,
                       body: MCPValidation.SetRepHero,
                       query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the player's rep hero
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    hero_id = request_body.get("heroId")
    slot_index = request_body.get("slotIdx")
    hero = await request.ctx.profile.get_item_by_guid(hero_id)
    if hero is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage=f"Hero with id {hero_id} not found")
    if not hero.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage=f"Invalid character item id {hero_id}")
    rep_heroes = await request.ctx.profile.get_stat("rep_hero_ids")
    max_rep_heroes = await request.ctx.profile.get_stat("max_rep_heroes")
    if slot_index >= max_rep_heroes:
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage=f"Slot index {slot_index} is greater than max rep heroes {max_rep_heroes}")
    if hero_id in rep_heroes:
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage=f"Hero with id {hero_id} already set on another slot")
    if len(rep_heroes) < slot_index + 1:
        for i in range(slot_index + 1 - len(rep_heroes)):
            rep_heroes.append("")
    rep_heroes[slot_index] = hero_id
    await request.ctx.profile.modify_stat("rep_hero_ids", rep_heroes)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
