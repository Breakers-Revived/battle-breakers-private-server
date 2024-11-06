"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles selling multiple gear.
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_sell_multiple_gear = sanic.Blueprint("wex_profile_sell_multiple_gear")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SellHero.md
@wex_profile_sell_multiple_gear.route("/<accountId>/SellMultipleGear", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def sell_multiple_gear(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to sell multiple gear
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # EWExpRarity::Common       - 1
    # EWExpRarity::Uncommon     - 2
    # EWExpRarity::Rare         - 4
    # EWExpRarity::VeryRare     - 8
    # EWExpRarity::SuperRare    - 20
    gear_guid = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shard_Gear")
    gear_quantity = 0
    if gear_guid:
        gear_quantity = (await request.ctx.profile.get_item_by_guid(gear_guid[0]))["quantity"]
    if not request.json.get("itemIds"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="No items to sell")
    if len(request.json.get("itemIds")) == 1:
        if (await request.ctx.profile.get_item_by_guid(request.json.get("itemIds")[0])) is None:
            raise errors.com.epicgames.world_explorers.not_found(
                errorMessage="We're sorry, but we were unable to sell your item as it was not found in your inventory.")
    for item_guid in request.json.get("itemIds"):
        # TODO: validate the item to sell
        match (await request.ctx.profile.get_item_by_guid(item_guid))["attributes"]["rarity"]:
            case "Common":
                value = 1
            case "Uncommon":
                value = 2
            case "Rare":
                value = 4
            case "VeryRare":
                value = 8
            case "SuperRare":
                value = 20
            case _:
                # raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid rarity")
                # silently fail so that other items can be sold still
                continue
        if gear_guid:
            gear_quantity += value
            await request.ctx.profile.change_item_quantity(gear_guid[0], gear_quantity)
        else:
            gear_quantity += value
            gear_guid = [(await request.ctx.profile.add_item({
                "templateId": "Reagent:Reagent_Shard_Gear",
                "attributes": {},
                "quantity": value}
            ))]
        await request.ctx.profile.remove_item(item_guid)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
