"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles opening a gift box.
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_path_from_template_id, load_datatable

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_open_gift_box = sanic.Blueprint("wex_profile_open_gift_box")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/OpenGiftBox.md
@wex_profile_open_gift_box.route("/<accountId>/OpenGiftBox", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def open_gift_box(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to open a gift box.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
    opened_gift_box = await request.ctx.profile.get_item_by_guid(request.json.get("itemId"), request.ctx.profile_id)
    if opened_gift_box is None or not opened_gift_box["templateId"].startswith("Giftbox:"):
        raise errors.com.epicgames.world_explorers.not_found(errorMessage="Gift box not found.")
    items = []
    tier_group_name = request.json.get("itemId")
    giftbox_data = (await load_datatable(
        (await get_path_from_template_id(opened_gift_box["templateId"])).replace(
            "res/Game/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"]
    if giftbox_data.get("Loot") is not None:
        if giftbox_data["Loot"].get("Items") is not None:
            for item in giftbox_data["Loot"]["Items"]:
                item_id = None
                if item["ItemType"].split(":")[0] not in ["Character", "Giftbox"]:
                    item_id = await request.ctx.profile.find_item_by_template_id(item["ItemType"])
                if not item_id:
                    match item["ItemType"].split(":")[0]:
                        case "Character":
                            item_id = await request.ctx.profile.add_item({
                                "templateId": item["ItemType"],
                                "attributes": {
                                    "gear_weapon_item_id": "",
                                    "weapon_unlocked": False,
                                    "sidekick_template_id": "",
                                    "is_new": True,
                                    "level": 1,
                                    "num_sold": 0,
                                    "skill_level": 1,
                                    "sidekick_unlocked": False,
                                    "upgrades": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    "used_as_sidekick": False,
                                    "gear_armor_item_id": "",
                                    "skill_xp": 0,
                                    "armor_unlocked": False,
                                    "foil_lvl": -1,
                                    "xp": 0,
                                    "rank": 0,
                                    "sidekick_item_id": ""
                                },
                                "quantity": item["Quantity"]
                            })
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
                items.append({
                    "itemType": item["ItemType"],
                    "itemGuid": item_id,
                    "itemProfile": "profile0",
                    "quantity": item["Quantity"]
                })
        else:
            # TODO: Implement more loot data
            match '.'.join(giftbox_data["Loot"]["LootTable"].split(".")[:-1]):
                case "LTG.GiftBox.AccountLevel":
                    pass
                case "LTG.GiftBox.AccountLevel.Promo20":
                    pass
                case "LTG.GiftBox.AccountLevel.Promo50":
                    pass
                case "LTG.GiftBox.BattlePass":
                    pass
                case "LTG.GiftBox.DailyGems.Large":
                    pass
                case "LTG.GiftBox.DailyGems.Laundry":
                    pass
                case "LTG.GiftBox.DailyGems.Short.Large":
                    pass
                case "LTG.GiftBox.DailyGems.Small":
                    pass
                case "LTG.GiftBox.LevelUpPackage.Basic":
                    pass
            pass
    await request.ctx.profile.add_notifications({
        "type": "WExpGiftBoxOpened",
        "primary": True,
        "giftBoxTemplateId": opened_gift_box["templateId"],
        "lootResult": {
            "tierGroupName": tier_group_name,
            "items": items
        }
    })
    await request.ctx.profile.remove_item(request.json["itemId"])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions, True)
    )
