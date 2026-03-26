"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles opening a gift box.
"""

import sanic
import sanic_ext
import sanic.log

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_path_from_template_id, load_datatable, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_open_gift_box = sanic.Blueprint("wex_profile_open_gift_box")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/OpenGiftBox.md
@wex_profile_open_gift_box.route("/<accountId>/OpenGiftBox", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.OpenGiftBox, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def open_gift_box(request: types.BBProfileRequest, accountId: str,
                        body: MCPValidation.OpenGiftBox,
                        query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to open a gift box.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    opened_gift_box = await request.ctx.profile.get_item_by_guid(request_body.get("itemId"), request.ctx.profile_id)
    if opened_gift_box is None or not opened_gift_box["templateId"].startswith("Giftbox:"):
        raise errors.com.epicgames.world_explorers.not_found(errorMessage="Gift box not found.")
    items = []
    tier_group_name = request_body.get("itemId")
    giftbox_data = (await load_datatable(
        (await get_path_from_template_id(opened_gift_box["templateId"])).replace(
            "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"]
    if giftbox_data.get("Loot") is not None:
        if giftbox_data["Loot"].get("Items") is not None:
            for item in giftbox_data["Loot"]["Items"]:
                item_id = None
                if item["ItemType"] == "Reagent:Reagent_Hero_Gold":
                    item["ItemType"] = "Token:TK_HeroMap_Lunar"
                if item["ItemType"].split(":")[0] not in ["Character", "Giftbox"]:
                    item_id = await request.ctx.profile.find_item_by_template_id(item["ItemType"])
                if not item_id:
                    match item["ItemType"].split(":")[0]:
                        case "Character":
                            item_id = await request.ctx.profile.grant_hero(item["ItemType"], quantity=item["Quantity"])
                        case "Giftbox":
                            item_id = await request.ctx.profile.add_item({
                                "templateId": item["ItemType"],
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 1
                                },
                                "quantity": item["Quantity"]
                            })
                        case _:
                            item_id = await request.ctx.profile.add_item({
                                "templateId": item["ItemType"],
                                "attributes": {},
                                "quantity": item["Quantity"]
                            })
                else:
                    item_id = item_id[0]
                    item_data = await request.ctx.profile.get_item_by_guid(item_id)
                    await request.ctx.profile.change_item_quantity(item_id, item_data["quantity"] + item["Quantity"])
                if isinstance(item_id, list):
                    for item_ids in item_id:
                        items.append({
                            "itemType": item["ItemType"],
                            "itemGuid": item_ids,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                else:
                    items.append({
                        "itemType": item["ItemType"],
                        "itemGuid": item_id,
                        "itemProfile": "profile0",
                        "quantity": item["Quantity"]
                    })
        else:
            items = await request.ctx.profile.grant_loot_from_tiergroup(giftbox_data["Loot"]["TierGroupName"])
    if not items:
        sanic.log.logger.warning(f"Gift box {opened_gift_box['templateId']} did not grant any items.")
        items.append({
            "itemType": "Reagent:Reagent_Shared_T02",
            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T02"),
            "itemProfile": "profile0",
            "quantity": 1
        })
    await request.ctx.profile.add_notifications({
        "type": "WExpGiftBoxOpened",
        "primary": True,
        "giftBoxTemplateId": opened_gift_box["templateId"],
        "lootResult": {
            "tierGroupName": tier_group_name,
            "items": items
        }
    })
    await request.ctx.profile.remove_item(request_body["itemId"])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
