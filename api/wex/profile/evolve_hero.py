"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles evolving heroes
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id, get_template_id_from_path

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_evolve_hero = sanic.Blueprint("wex_profile_evolve_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/EvolveHero.md
@wex_profile_evolve_hero.route("/<accountId>/EvolveHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def evolve_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to evolve heroes
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    if request.json.get("bIsInPit"):
        old_hero = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        old_hero = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if old_hero is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    evolution_recipe = (await load_datatable(
        (await get_path_from_template_id(request.json.get("evoPathName"))).replace(
            "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"]
    if old_hero["attributes"]["level"] < evolution_recipe.get("RequiredCharacterLevel", 0):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Hero level is too low")
    cost_recipe = (await load_datatable(
        evolution_recipe["Recipe"]["ObjectPath"].replace("WorldExplorers/", "").replace(".0", "")))[0]["Properties"]
    pending_items = []
    for consumed_item in cost_recipe["ConsumedItems"]:
        consumed_item_id = (await request.ctx.profile.find_item_by_template_id(
            await get_template_id_from_path(consumed_item["ItemDefinition"]["ObjectPath"])))[0]
        consumed_item_quantity = (await request.ctx.profile.get_item_by_guid(consumed_item_id))["quantity"]
        if consumed_item_quantity < consumed_item["Count"]:
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage=f"Not enough {consumed_item['ItemDefinition']['ObjectName']}")
        pending_items.append({
            "itemId": consumed_item_id,
            "quantity": consumed_item_quantity - consumed_item["Count"]
        })
    new_hero_id = (
        await get_template_id_from_path(evolution_recipe["EvolutionDestination"]["ObjectPath"]))
    if not new_hero_id:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    for pending_item in pending_items:
        await request.ctx.profile.change_item_quantity(pending_item["itemId"], pending_item["quantity"])
    await request.ctx.profile.add_notifications({
        "type": "WExpCharacterEvolution",
        "primary": True,
        "oldItemId": request.json.get("heroItemId"),
        "oldTemplateId": old_hero["templateId"],
        "newItemId": request.json.get("heroItemId")  # TODO: determine compatibility with old clients
    }, request.ctx.profile_id)
    old_hero["templateId"] = new_hero_id
    if request.json.get("bIsInPit"):
        await request.ctx.profile.add_item(old_hero, request.json.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        await request.ctx.profile.add_item(old_hero, request.json.get("heroItemId"))
    # TODO: chest activity
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
