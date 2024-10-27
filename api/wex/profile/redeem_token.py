"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles redeeming tokens.
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_path_from_template_id, load_datatable, get_template_id_from_path

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_redeem_token = sanic.Blueprint("wex_profile_redeem_token")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/RollHammerChests.md
@wex_profile_redeem_token.route("/<accountId>/RedeemToken", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def redeem_token(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade tokens to the actual item (for migrating from old accounts)
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    token_id = await request.ctx.profile.find_item_by_template_id(request.json.get("tokenTemplate"))
    if not token_id:
        raise errors.com.epicgames.world_explorers.not_found(errorMessage="This token was not found in your profile.")
    item_path = (await get_path_from_template_id(request.json.get("tokenTemplate")))
    token_item = await request.ctx.profile.get_item_by_guid(token_id[0])
    try:
        reward_item = (await load_datatable(
            item_path.replace("res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0][
            "Properties"]
        reward_item["RewardItem"]
    except KeyError:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="This item cannot be redeemed.")
    if token_item["quantity"] < reward_item["RedeemQuantity"]:
        raise errors.com.epicgames.world_explorers.bad_request(reward_item["RedeemQuantity"], token_item["quantity"],
                                                               errorMessage=f"{reward_item['RedeemQuantity']}x "
                                                                            f"{request.json.get('tokenTemplate')}s "
                                                                            f"required to redeem. You only have "
                                                                            f"{token_item['quantity']}.")
    redeem_quantity = token_item["quantity"] // reward_item["RedeemQuantity"]
    new_item_id = (await request.ctx.profile.find_item_by_template_id(
        await get_template_id_from_path(reward_item["RewardItem"]["ObjectPath"])))
    if not new_item_id:
        new_item_id = await request.ctx.profile.add_item({
            "templateId": await get_template_id_from_path(reward_item["RewardItem"]["ObjectPath"]),
            "attributes": {},
            "quantity": redeem_quantity
        })
    else:
        new_item_id = new_item_id[0]
        new_item_quantity = (await request.ctx.profile.get_item_by_guid(new_item_id))["quantity"]
        await request.ctx.profile.change_item_quantity(new_item_id, new_item_quantity + redeem_quantity)
    if token_item["quantity"] - (redeem_quantity * reward_item["RedeemQuantity"]) > 0:
        await request.ctx.profile.change_item_quantity(token_id[0], token_item["quantity"] - (
                redeem_quantity * reward_item["RedeemQuantity"]))
    else:
        await request.ctx.profile.remove_item(token_id[0])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
