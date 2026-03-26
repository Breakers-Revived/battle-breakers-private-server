"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles evolving heroes
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id, get_template_id_from_path, \
    extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_evolve_hero = sanic.Blueprint("wex_profile_evolve_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/EvolveHero.md
@wex_profile_evolve_hero.route("/<accountId>/EvolveHero", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.EvolveHero, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def evolve_hero(request: types.BBProfileRequest, accountId: str,
                      body: MCPValidation.EvolveHero,
                      query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to evolve heroes
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: validation
    request_body = body.model_dump()
    if request_body.get("bIsInPit"):
        old_hero = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        old_hero = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"))
    if old_hero is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    evolution_recipe = (await load_datatable(
        (await get_path_from_template_id(request_body.get("evoPathName"))).replace(
            "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"]
    if old_hero["attributes"]["level"] < evolution_recipe.get("RequiredCharacterLevel", 0):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Hero level is too low")
    cost_recipe = (await load_datatable(
        evolution_recipe["Recipe"]["ObjectPath"].replace("WorldExplorers/", "").replace(".0", "")))[0]["Properties"]
    for consumed_item in cost_recipe["ConsumedItems"]:
        consumed_item_id = await get_template_id_from_path(consumed_item["ItemDefinition"]["ObjectPath"])
        await request.ctx.profile.consume_item(consumed_item_id, consumed_item["Count"])
    new_hero_id = await get_template_id_from_path(evolution_recipe["EvolutionDestination"]["ObjectPath"])
    if not new_hero_id:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    await request.ctx.profile.add_notifications({
        "type": "WExpCharacterEvolution",
        "primary": True,
        "oldItemId": request_body.get("heroItemId"),
        "oldTemplateId": old_hero["templateId"],
        "newItemId": request_body.get("heroItemId")  # TODO: determine compatibility with old clients
    }, request.ctx.profile_id)
    old_hero["templateId"] = new_hero_id
    if request_body.get("bIsInPit"):
        await request.ctx.profile.add_item(old_hero, request_body.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        await request.ctx.profile.add_item(old_hero, request_body.get("heroItemId"))
    # TODO: chest activity
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
