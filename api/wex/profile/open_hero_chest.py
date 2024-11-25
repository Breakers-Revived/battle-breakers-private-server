"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles opening a hero chest.
"""

import sanic

import utils.utils
from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_open_hero_chest = sanic.Blueprint("wex_profile_open_hero_chest")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/OpenHeroChest.md
@wex_profile_open_hero_chest.route("/<accountId>/OpenHeroChest", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def open_hero_chest(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to open a hero chest.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    tower_data = await request.ctx.profile.get_item_by_guid(request.json.get("towerId"))
    if tower_data is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid tower id")
    if not tower_data["attributes"].get("active_chest"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Tower has no active chest. Call PickHeroChest")
    active_chest = tower_data["attributes"]["active_chest"]
    currency_id = await request.ctx.profile.find_item_by_template_id(tower_data["attributes"][f"{active_chest['heroChestType']}_static_currency_template_id"])
    if not currency_id:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Required reagent not found")
    currency = await request.ctx.profile.get_item_by_guid(currency_id[0])
    if currency is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Required reagent not found")
    if currency["quantity"] < tower_data["attributes"][f"{active_chest['heroChestType']}_static_currency_amount"]:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough reagents")
    currency["quantity"] -= tower_data["attributes"][f"{active_chest['heroChestType']}_static_currency_amount"]
    if currency["quantity"] == 0:
        await request.ctx.profile.remove_item(currency_id[0])
    else:
        await request.ctx.profile.change_item_quantity(currency_id[0], currency["quantity"])
    if request.json.get("itemTemplateId").split(":")[0] != "Character":
        await request.ctx.profile.grant_item(request.json.get("itemTemplateId"), request.json.get("itemQuantity", 1))
    else:
        await request.ctx.profile.grant_hero(request.json.get("itemTemplateId"), foil_lvl=1 if active_chest["foilLevel"] > 0 else -1)
    # TODO: chest activity
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "active_chest", None)
    hero_tower_data = (await utils.utils.read_file("res/wex/api/game/v2/skybreaker/herotower.json"))[active_chest['heroTrackId']]
    new_page_index = tower_data["attributes"]["page_index"]
    if active_chest["heroTrackId"] == "CoreBasic":
        if tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1 > int(list(hero_tower_data[str(new_page_index)].keys())[-1]):
            await request.ctx.profile.change_item_attribute(request.json.get("towerId"), f"{active_chest['heroTrackId']}_progress", 0)
            track_progress = 0
            if tower_data["attributes"]["page_index"] + 1 > int(list(hero_tower_data.keys())[-1]):
                new_page_index = int(list(hero_tower_data.keys())[0])
                await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_SuperRare", 5)
            else:
                new_page_index = tower_data["attributes"]["page_index"] + 1
                await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_SuperRare", 1)
        else:
            await request.ctx.profile.change_item_attribute(request.json.get("towerId"), f"{active_chest['heroTrackId']}_progress", tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1)
            track_progress = tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1
    else:
        await request.ctx.profile.change_item_attribute(request.json.get("towerId"), f"{active_chest['heroTrackId']}_progress", tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1)
        track_progress = tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "level", tower_data["attributes"]["level"] + 1)
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "page_index", new_page_index)
    next_hero_track = list(hero_tower_data[str(new_page_index)].keys())[track_progress % len(hero_tower_data[str(new_page_index)])]
    new_chest_options = hero_tower_data[str(new_page_index)][str(next_hero_track)]
    new_chest_options["heroTrackId"] = active_chest['heroTrackId']
    new_chest_options["foilLevel"] = 1 if utils.utils.random.randint(0, 100) < 7 else 0
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "chest_options", [new_chest_options])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
