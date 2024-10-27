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
    # gift_id = await request.ctx.profile.add_item({
    #     "templateId": "Giftbox:CustomGiftbox",
    #     "attributes": {
    #         "sealed_days": 0,
    #         "params": {
    #             "message": "Hi Discord!\n\nThis is a custom test message.",
    #         },
    #         "min_level": 1
    #     },
    #     "quantity": 1
    # })
    opened_gift_box = await request.ctx.profile.get_item_by_guid(request.json.get("itemId"), request.ctx.profile_id)
    if opened_gift_box is None or not opened_gift_box["templateId"].startswith("Giftbox:"):
        raise errors.com.epicgames.world_explorers.not_found(errorMessage="Gift box not found.")
    items = []
    tier_group_name = request.json.get("itemId")
    giftbox_data = (await load_datatable(
        (await get_path_from_template_id(opened_gift_box["templateId"])).replace(
            "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"]
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
            match '.'.join(giftbox_data["Loot"]["TierGroupName"].split(".")[:-1]):
                case "LTG.GiftBox.AccountLevel":
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    match stage:
                        case "01":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_HeroMap_Elemental",
                                    "attributes": {},
                                    "quantity": 100
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 100)
                            items.append({
                                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 100
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": "Giftbox:GB_AccountLevel_Promo20",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 20
                                },
                                "quantity": 1
                            })    
                            items.append({
                                "itemType": "Giftbox:GB_AccountLevel_Promo20",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "02":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_HeroMap_Elemental",
                                    "attributes": {},
                                    "quantity": 300
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 300)
                            items.append({
                                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 300
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": "Giftbox:GB_AccountLevel_Promo50_KurohomuraOnly",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 50
                                },
                                "quantity": 1
                            })
                            items.append({
                                "itemType": "Giftbox:GB_AccountLevel_Promo50_KurohomuraOnly",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "03":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_SupplyPoints_Elite",
                                    "attributes": {},
                                    "quantity": 100
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 100)
                            items.append({
                                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 100
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": "Giftbox:GB_AccountLevel04",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 75
                                },
                                "quantity": 1
                            })
                            items.append({
                                "itemType": "Giftbox:GB_AccountLevel04",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "04":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_SuperRare")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_HeroMap_SuperRare",
                                    "attributes": {},
                                    "quantity": 50
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 50)
                            items.append({
                                "itemType": "Reagent:Reagent_HeroMap_SuperRare",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 50
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": "Giftbox:GB_AccountLevel05",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 100
                                },
                                "quantity": 1
                            })
                            items.append({
                                "itemType": "Giftbox:GB_AccountLevel05",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "05" | "06" | "07" | "09" | "10" | "11" | "12" | "14" | "15" | "16" | "17" | "18" | "20" | "21" | "22":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_HeroMap_Elemental",
                                    "attributes": {},
                                    "quantity": 500
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 500)
                            items.append({
                                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 500
                            })
                            if stage == "22":
                                new_giftbox_id = await request.ctx.profile.add_item({
                                    "templateId": f"Giftbox:GB_AccountLevel{str(int(stage) + 1).zfill(2)}",
                                    "attributes": {
                                        "sealed_days": 0,
                                        "params": {},
                                        "min_level": 999
                                    },
                                    "quantity": 1
                                })
                            else:
                                new_giftbox_id = await request.ctx.profile.add_item({
                                    "templateId": f"Giftbox:GB_AccountLevel{str(int(stage) + 1).zfill(2)}",
                                    "attributes": {
                                        "sealed_days": 0,
                                        "params": {},
                                        "min_level": 100 + (50 * (int(stage) - 5))
                                    },
                                    "quantity": 1
                                })
                            items.append({
                                "itemType": f"Giftbox:GB_AccountLevel{str(int(stage) + 1).zfill(2)}",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "08" | "13" | "19":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_SupplyPoints_Elite",
                                    "attributes": {},
                                    "quantity": 200
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 200)
                            items.append({
                                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 200
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": f"Giftbox:GB_AccountLevel{str(int(stage) + 1).zfill(2)}",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 100 + (50 * (int(stage) - 5))
                                },
                                "quantity": 1
                            })
                            items.append({
                                "itemType": f"Giftbox:GB_AccountLevel{str(int(stage) + 1).zfill(2)}",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                        case "23":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_SuperRare")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Reagent:Reagent_HeroMap_SuperRare",
                                    "attributes": {},
                                    "quantity": 100
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 100)
                            items.append({
                                "itemType": "Reagent:Reagent_HeroMap_SuperRare",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 100
                            })
                        case "Promo20":
                            reward_id = await request.ctx.profile.find_item_by_template_id("Currency:Gold")
                            if not reward_id:
                                reward_id = await request.ctx.profile.add_item({
                                    "templateId": "Currency:Gold",
                                    "attributes": {},
                                    "quantity": 150000
                                })
                            else:
                                reward_id = reward_id[0]
                                reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                                await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 150000)
                            items.append({
                                "itemType": "Currency:Gold",
                                "itemGuid": reward_id,
                                "itemProfile": "profile0",
                                "quantity": 150000
                            })
                            new_giftbox_id = await request.ctx.profile.add_item({
                                "templateId": "Giftbox:GB_AccountLevel02",
                                "attributes": {
                                    "sealed_days": 0,
                                    "params": {},
                                    "min_level": 25
                                },
                                "quantity": 1
                            })
                            items.append({
                                "itemType": "Giftbox:GB_AccountLevel02",
                                "itemGuid": new_giftbox_id,
                                "itemProfile": "profile0",
                                "quantity": 1
                            })
                            items.append({
                                "itemType": "StandIn:FN_STW_Razor",
                                "quantity": 0
                            })
                            # This item was scrapped from the collab, but would have been granted here
                            items.append({
                                "itemType": "StandIn:FN_Backbling_Cloudpuff",
                                "quantity": 0
                            })
                case "LTG.GiftBox.AccountLevel.Promo50":
                    reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite")
                    if not reward_id:
                        reward_id = await request.ctx.profile.add_item({
                            "templateId": "Reagent:Reagent_SupplyPoints_Elite",
                            "attributes": {},
                            "quantity": 100
                        })
                    else:
                        reward_id = reward_id[0]
                        reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                        await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 100)
                    items.append({
                        "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                        "itemGuid": reward_id,
                        "itemProfile": "profile0",
                        "quantity": 100
                    })
                    new_giftbox_id = await request.ctx.profile.add_item({
                        "templateId": "Giftbox:GB_AccountLevel04",
                        "attributes": {
                            "sealed_days": 0,
                            "params": {},
                            "min_level": 75
                        },
                        "quantity": 1
                    })
                    items.append({
                        "itemType": "Giftbox:GB_AccountLevel04",
                        "itemGuid": new_giftbox_id,
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
                    items.append({
                        "itemType": "StandIn:FN_STW_Kurohomura",
                        "quantity": 0
                    })
                case "LTG.GiftBox.BattlePass":
                    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
                    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
                    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 100)
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": mtx_item_id,
                        "itemProfile": "profile0",
                        "quantity": 100
                    })
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    if stage != "30":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_Battlepass{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 1,
                                "params": {},
                                "min_level": 1
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_Battlepass{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                case "LTG.GiftBox.DailyGems.Large":
                    # TODO: determine correct gem count
                    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
                    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
                    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 100)
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": mtx_item_id,
                        "itemProfile": "profile0",
                        "quantity": 100
                    })
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    if stage != "30":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_DailyGems_Large{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 1,
                                "params": {},
                                "min_level": 1
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_DailyGems_Large{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                case "LTG.GiftBox.DailyGems.Laundry":
                    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
                    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
                    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 50)
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": mtx_item_id,
                        "itemProfile": "profile0",
                        "quantity": 50
                    })
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    if stage != "30":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_DailyGems_Laundry{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 1,
                                "params": {},
                                "min_level": 1
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_DailyGems_Laundry{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                case "LTG.GiftBox.DailyGems.Short.Large":
                    # TODO: determine correct gem count
                    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
                    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
                    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 100)
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": mtx_item_id,
                        "itemProfile": "profile0",
                        "quantity": 100
                    })
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    if stage != "7":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_DailyGems_Short_Large{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 1,
                                "params": {},
                                "min_level": 1
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_DailyGems_Short_Large{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                case "LTG.GiftBox.DailyGems.Small":
                    # TODO: determine correct gem count
                    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
                    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
                    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 50)
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": mtx_item_id,
                        "itemProfile": "profile0",
                        "quantity": 50
                    })
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    if stage != "30":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_DailyGems_Small{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 1,
                                "params": {},
                                "min_level": 1
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_DailyGems_Small{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                case "LTG.GiftBox.LevelUpPackage.Basic":
                    stage = giftbox_data["Loot"]["TierGroupName"].split(".")[-1]
                    reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental")
                    if not reward_id:
                        reward_id = await request.ctx.profile.add_item({
                            "templateId": "Reagent:Reagent_HeroMap_Elemental",
                            "attributes": {},
                            "quantity": 1000
                        })
                    else:
                        reward_id = reward_id[0]
                        reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                        await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 1000)
                    items.append({
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": reward_id,
                        "itemProfile": "profile0",
                        "quantity": 1000
                    })
                    gold_id = await request.ctx.profile.find_item_by_template_id("Currency:Gold")
                    if not gold_id:
                        gold_id = await request.ctx.profile.add_item({
                            "templateId": "Currency:Gold",
                            "attributes": {},
                            "quantity": 100000
                        })
                    else:
                        gold_id = gold_id[0]
                        gold_data = await request.ctx.profile.get_item_by_guid(gold_id)
                        await request.ctx.profile.change_item_quantity(gold_id, gold_data["quantity"] + 100000)
                    items.append({
                        "itemType": "Currency:Gold",
                        "itemGuid": gold_id,
                        "itemProfile": "profile0",
                        "quantity": 100000
                    })
                    if stage != "15":
                        new_giftbox_id = await request.ctx.profile.add_item({
                            "templateId": f"Giftbox:GB_LevelUpPackage_Basic{str(int(stage) + 1).zfill(2)}",
                            "attributes": {
                                "sealed_days": 0,
                                "params": {},
                                "min_level": (stage + 1) * 10
                            },
                            "quantity": 1
                        })
                        items.append({
                            "itemType": f"Giftbox:GB_LevelUpPackage_Basic{str(int(stage) + 1).zfill(2)}",
                            "itemGuid": new_giftbox_id,
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    else:
                        reward_id = await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_SuperRare")
                        if not reward_id:
                            reward_id = await request.ctx.profile.add_item({
                                "templateId": "Reagent:Reagent_HeroMap_SuperRare",
                                "attributes": {},
                                "quantity": 100
                            })
                        else:
                            reward_id = reward_id[0]
                            reward_data = await request.ctx.profile.get_item_by_guid(reward_id)
                            await request.ctx.profile.change_item_quantity(reward_id, reward_data["quantity"] + 100)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_SuperRare",
                            "itemGuid": reward_id,
                            "itemProfile": "profile0",
                            "quantity": 100
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
    await request.ctx.profile.remove_item(request.json["itemId"])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions, True)
    )
