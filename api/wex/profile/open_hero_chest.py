"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles opening a hero chest.
"""

import sanic

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
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), f"{active_chest['heroTrackId']}_progress", tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1)
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "level", tower_data["attributes"]["level"] + 1)
    await request.ctx.profile.add_item({
        "templateId": request.json.get("itemTemplateId"),
        "attributes": {
            "gear_weapon_item_id": "",
            "weapon_unlocked": False,
            "sidekick_template_id": "",
            "level": 1,
            "is_new": True,
            "num_sold": 0,
            "skill_level": 1,
            "sidekick_unlocked": False,
            "upgrades": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "used_as_sidekick": False,
            "gear_armor_item_id": "",
            "skill_xp": 0,
            "armor_unlocked": False,
            "foil_lvl": -1,
            "xp": 0,
            "rank": 0,
            "sidekick_item_id": ""
        },
        "quantity": 1
    })
    # TODO: chest activity
    await request.ctx.profile.change_item_attribute(request.json.get("towerId"), "active_chest", None)
    # TODO: add the next hero choices to the tower data
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
