"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles selling treasure.
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_sell_treasure = sanic.Blueprint("wex_profile_sell_treasure")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SellHero.md
@wex_profile_sell_treasure.route("/<accountId>/SellTreasure", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def sell_treasure(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to sell treasure
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    item_path = (await get_path_from_template_id(request.json.get("itemTemplateId")))
    try:
        value = (await load_datatable(
            item_path.replace("res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0][
            "Properties"]["GoldValue"]
    except KeyError:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="This item cannot be sold.")
    gold_id = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    item_guid = (await request.ctx.profile.find_item_by_template_id(request.json.get("itemTemplateId")))
    if not item_guid:
        raise errors.com.epicgames.world_explorers.not_found(
            errorMessage="We're sorry, but we were unable to sell your item as it was not found in your inventory.")
    else:
        item_guid = item_guid[0]
    item_quantity = (await request.ctx.profile.get_item_by_guid(item_guid))["quantity"]
    sell_quantity = request.json.get("quantity")
    if sell_quantity > item_quantity:
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage=f"Invalid quantity to sell for item {item_guid}")
    if sell_quantity < item_quantity:
        await request.ctx.profile.change_item_quantity(item_guid, item_quantity - sell_quantity)
    else:
        await request.ctx.profile.remove_item(item_guid)
    await request.ctx.profile.change_item_quantity(gold_id, current_gold + (value * sell_quantity))
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
