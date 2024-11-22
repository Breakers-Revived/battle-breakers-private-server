"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles tapping the hammer chest.
"""
import random

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, calculate_streakbreaker

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_tap_hammer_chest = sanic.Blueprint("wex_profile_tap_hammer_chest")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/TapHammerChest.md
@wex_profile_tap_hammer_chest.route("/<accountId>/TapHammerChest", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def tap_hammer_chest(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to tap the hammer chest
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    hammer_id = await request.ctx.profile.find_item_by_template_id("Currency:Hammer")
    if not hammer_id:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="You do not have any hammers")
    hammer_item = await request.ctx.profile.get_item_by_guid(hammer_id[0])
    if hammer_item is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hammer ID")
    if hammer_item.get("quantity") < 1:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="You do not have enough hammers")
    chest_id = await request.ctx.profile.get_stat("active_hammer_chest")
    if chest_id is None or chest_id == "":
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="There is no active hammer chest")
    chest_item = await request.ctx.profile.get_item_by_guid(chest_id)
    if chest_item is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid chest ID")
    if not chest_item.get("templateId").startswith("HammerChest:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid chest ID")
    if chest_item.get("attributes").get("taps_remaining") < 1:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="There are no taps remaining on this chest")
    streakbreaker_id = await request.ctx.profile.find_item_by_template_id("Currency:SB_HammerRare")
    if streakbreaker_id:
        streakbreaker_id = streakbreaker_id[0]
        current_streakbreaker = (await request.ctx.profile.get_item_by_guid(streakbreaker_id)).get("quantity")
    else:
        current_streakbreaker = 0
    chest_data = await load_datatable(
        f"Content/Loot/AccountItems/HammerChests/{chest_item.get('templateId').split(':')[1]}")
    hammer_quantity = hammer_item.get("quantity") - 1
    if chest_item.get("attributes").get("taps_remaining") == 1:
        # Original game server would change the taps remaining & applied here before removing the chest
        await request.ctx.profile.remove_item(chest_id)
        await request.ctx.profile.modify_stat("active_hammer_chest", "")
        loot_tier_group = chest_data[0]["Properties"]["OnCompletionLootPackage"]
        completed = True
    else:
        await request.ctx.profile.change_item_attribute(chest_id, "taps_remaining",
                                                        chest_item.get("attributes").get("taps_remaining") - 1)
        await request.ctx.profile.change_item_attribute(chest_id, "taps_applied",
                                                        chest_item.get("attributes").get("taps_applied") + 1)
        loot_tier_group = chest_data[0]["Properties"]["OnDamageLootPackage"]
        completed = False
    items = []
    match loot_tier_group:
        case "LTG.HammerChest.Evolve.Dark.Normal.Hit":
            for _ in range(2):
                items.append({
                    "itemType": "Reagent:Reagent_Shared_T02",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 12)
                })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 8)
                })
        case "LTG.HammerChest.Evolve.Dark.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shard_Dark",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Dark"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Evolve.Dark.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_Shared_T02",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 30)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(8, 17)
                })
        case "LTG.HammerChest.Evolve.Dark.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shard_Dark",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Dark"),
                "itemProfile": "profile0",
                "quantity": random.randint(4, 8)
            })
        case "LTG.HammerChest.Evolve.Fire.Normal.Hit":
            for _ in range(2):
                items.append({
                    "itemType": "Reagent:Reagent_Shared_T02",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 12)
                })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 8)
                })
        case "LTG.HammerChest.Evolve.Fire.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Fire",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Fire"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Evolve.Fire.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_Shared_T02",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 30)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(8, 17)
                })
        case "LTG.HammerChest.Evolve.Fire.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Fire",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Fire"),
                "itemProfile": "profile0",
                "quantity": random.randint(4, 8)
            })
        case "LTG.HammerChest.Evolve.Light.Normal.Hit":
            for _ in range(2):
                items.append({
                    "itemType": "Reagent:Reagent_Shared_T02",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 12)
                })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 8)
                })
        case "LTG.HammerChest.Evolve.Light.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Light",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Light"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Evolve.Light.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_Shared_T02",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 30)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(8, 17)
                })
        case "LTG.HammerChest.Evolve.Light.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Light",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Light"),
                "itemProfile": "profile0",
                "quantity": random.randint(4, 8)
            })
        case "LTG.HammerChest.Evolve.Nature.Normal.Hit":
            for _ in range(2):
                items.append({
                    "itemType": "Reagent:Reagent_Shared_T02",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 12)
                })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 8)
                })
        case "LTG.HammerChest.Evolve.Nature.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Nature",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Nature"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Evolve.Nature.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_Shared_T02",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 30)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(8, 17)
                })
        case "LTG.HammerChest.Evolve.Nature.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Nature",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Nature"),
                "itemProfile": "profile0",
                "quantity": random.randint(4, 8)
            })
        case "LTG.HammerChest.Evolve.Shards.Normal.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(5, 14)
                    })
                case 1:
                    items.append({
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                        "itemProfile": "profile0",
                        "quantity": 7
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                random_essence = random.choice(
                    ["Reagent:Reagent_Shared_Dark", "Reagent:Reagent_Shared_Fire", "Reagent:Reagent_Shared_Light",
                     "Reagent:Reagent_Shared_Nature", "Reagent:Reagent_Shared_Water"])
                items.append({
                    "itemType": random_essence,
                    "itemGuid": await request.ctx.profile.find_item_by_template_id(random_essence),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
        case "LTG.HammerChest.Evolve.Shards.Normal.Destroy":
            for _ in range(5):
                random_essence = random.choice(
                    ["Reagent:Reagent_Shared_Dark", "Reagent:Reagent_Shared_Fire", "Reagent:Reagent_Shared_Light",
                     "Reagent:Reagent_Shared_Nature", "Reagent:Reagent_Shared_Water"])
                items.append({
                    "itemType": random_essence,
                    "itemGuid": await request.ctx.profile.find_item_by_template_id(random_essence),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
        case "LTG.HammerChest.Evolve.Shards.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    random_essence = random.choice(
                        ["Reagent:Reagent_Shared_Dark", "Reagent:Reagent_Shared_Fire", "Reagent:Reagent_Shared_Light",
                         "Reagent:Reagent_Shared_Nature", "Reagent:Reagent_Shared_Water"])
                    items.append({
                        "itemType": random_essence,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(random_essence),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(19, 30)
                    })
        case "LTG.HammerChest.Evolve.Shards.Rare.Destroy":
            for _ in range(5):
                random_essence = random.choice(
                    ["Reagent:Reagent_Shared_Dark", "Reagent:Reagent_Shared_Fire", "Reagent:Reagent_Shared_Light",
                     "Reagent:Reagent_Shared_Nature", "Reagent:Reagent_Shared_Water"])
                items.append({
                    "itemType": random_essence,
                    "itemGuid": await request.ctx.profile.find_item_by_template_id(random_essence),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
        case "LTG.HammerChest.Evolve.Water.Normal.Hit":
            for _ in range(2):
                items.append({
                    "itemType": "Reagent:Reagent_Shared_T02",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 12)
                })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(5, 8)
                })
        case "LTG.HammerChest.Evolve.Water.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Water",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Water"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Evolve.Water.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_Shared_T02",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 30)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                    "itemProfile": "profile0",
                    "quantity": random.randint(8, 17)
                })
        case "LTG.HammerChest.Evolve.Water.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_Water",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_Water"),
                "itemProfile": "profile0",
                "quantity": random.randint(4, 8)
            })
        case "LTG.HammerChest.Hammer.Normal.Hit":
            items.append({
                "itemType": "Currency:Hammer",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:Hammer"),
                "itemProfile": "profile0",
                "quantity": random.randint(1, 2)
            })
        case "LTG.HammerChest.Hammer.Normal.Destroy":
            items.append({
                "itemType": "Currency:Hammer",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:Hammer"),
                "itemProfile": "profile0",
                "quantity": random.randint(3, 5)
            })
        case "LTG.HammerChest.Hero.Bronze.Normal.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(20, 40)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_RXT_Parts_Small",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_RXT_Parts_Small"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 2):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(6, 8)
                        })
                    case 1:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Elemental"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(3, 8)
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(1, 2)
                        })
        case "LTG.HammerChest.Hero.Bronze.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Bronze",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Bronze"),
                "itemProfile": "profile0",
                "quantity": 2
            })
        case "LTG.HammerChest.Hero.Bronze.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(50, 100)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_RXT_Parts_Small",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_RXT_Parts_Small"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 1):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(12, 15)
                        })
                    case 1:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Elemental"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(5, 10)
                        })
        case "LTG.HammerChest.Hero.Bronze.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Bronze",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Bronze"),
                "itemProfile": "profile0",
                "quantity": random.randint(3, 5)
            })
        case "LTG.HammerChest.Hero.Gold.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(20, 50)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_RXT_Parts_Small",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_RXT_Parts_Small"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 3):
                    case 0:
                        items.append({
                            "itemType": "Reagent:Reagent_RXT_Parts_Small",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_RXT_Parts_Small"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 1:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(10, 11)
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 3:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Elemental"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(16, 25)
                        })
        case "LTG.HammerChest.Hero.Gold.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental"),
                "itemProfile": "profile0",
                "quantity": random.randint(213, 218)
            })
        case "LTG.HammerChest.Hero.Silver.Normal.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(20, 50)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_RXT_Parts_Small",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_RXT_Parts_Small"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 2):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(5, 12)
                        })
                    case 1:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Elemental"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(10, 15)
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
        case "LTG.HammerChest.Hero.Silver.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental"),
                "itemProfile": "profile0",
                "quantity": random.randint(81, 122)
            })
        case "LTG.HammerChest.Hero.Silver.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": 58
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_HeroMap_Elemental"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(10, 20)
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 2):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(11, 16)
                        })
                    case 1:
                        items.append({
                            "itemType": "Reagent:Reagent_RXT_Parts_Small",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_RXT_Parts_Small"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
        case "LTG.HammerChest.Hero.Silver.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Elemental",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Elemental"),
                "itemProfile": "profile0",
                "quantity": 255
            })
        case "LTG.HammerChest.LevelResources.Normal.Hit":
            items.append({
                "itemType": "TreasureMap:TM_MapResource",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("TreasureMap:TM_MapResource"),
                "itemProfile": "profile0",
                "quantity": random.randint(3, 8)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 1):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(5, 8)
                        })
                    case 1:
                        map_drop = random.choice([["TreasureMap:TM_Special_Cloud5", 5],
                                                  ["TreasureMap:TM_Special_MeegCity", 5],
                                                  ["TreasureMap:TM_Special_GhostShip", 3],
                                                  ["TreasureMap:TM_Special_EasterEggDesert", 1],
                                                  ["TreasureMap:TM_Special_PlanetCore", 1],
                                                  ["TreasureMap:TM_Special_UnderwaterForest", 1],
                                                  ["TreasureMap:TM_Special_UnderwaterTunnel", 1]])
                        items.append({
                            "itemType": map_drop[0],
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(map_drop[0]),
                            "itemProfile": "profile0",
                            "quantity": map_drop[1]
                        })
        case "LTG.HammerChest.LevelResources.Normal.Destroy":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "TreasureMap:TM_MapResource",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("TreasureMap:TM_MapResource"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(20, 30)
                    })
                case 1:
                    map_drop = random.choice([["TreasureMap:TM_Special_Cloud5", 5],
                                              ["TreasureMap:TM_Special_MeegCity", 5],
                                              ["TreasureMap:TM_Special_GhostShip", 3],
                                              ["TreasureMap:TM_Special_EasterEggDesert", 1],
                                              ["TreasureMap:TM_Special_PlanetCore", 1],
                                              ["TreasureMap:TM_Special_UnderwaterForest", 1],
                                              ["TreasureMap:TM_Special_UnderwaterTunnel", 1]])
                    items.append({
                        "itemType": map_drop[0],
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(map_drop[0]),
                        "itemProfile": "profile0",
                        "quantity": map_drop[1]
                    })
        case "LTG.HammerChest.LevelResources.Rare.Hit":
            items.append({
                "itemType": "TreasureMap:TM_MapResource",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("TreasureMap:TM_MapResource"),
                "itemProfile": "profile0",
                "quantity": random.randint(8, 12)
            })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                match random.randint(0, 1):
                    case 0:
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                            "itemProfile": "profile0",
                            "quantity": random.randint(10, 16)
                        })
                    case 1:
                        map_drop = random.choice([["TreasureMap:TM_Special_Cloud5", 5],
                                                  ["TreasureMap:TM_Special_MeegCity", 5],
                                                  ["TreasureMap:TM_Special_GhostShip", 3],
                                                  ["TreasureMap:TM_Special_EasterEggDesert", 1],
                                                  ["TreasureMap:TM_Special_PlanetCore", 1],
                                                  ["TreasureMap:TM_Special_UnderwaterForest", 1],
                                                  ["TreasureMap:TM_Special_UnderwaterTunnel", 1]])
                        items.append({
                            "itemType": map_drop[0],
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(map_drop[0]),
                            "itemProfile": "profile0",
                            "quantity": map_drop[1]
                        })
        case "LTG.HammerChest.LevelResources.Rare.Destroy":
            for _ in range(2):
                map_drop = random.choice([["TreasureMap:TM_Special_Cloud5", 5], ["TreasureMap:TM_Special_MeegCity", 5],
                                          ["TreasureMap:TM_Special_GhostShip", 3],
                                          ["TreasureMap:TM_Special_EasterEggDesert", 1],
                                          ["TreasureMap:TM_Special_PlanetCore", 1],
                                          ["TreasureMap:TM_Special_UnderwaterForest", 1],
                                          ["TreasureMap:TM_Special_UnderwaterTunnel", 1]])
                items.append({
                    "itemType": map_drop[0],
                    "itemGuid": await request.ctx.profile.find_item_by_template_id(map_drop[0]),
                    "itemProfile": "profile0",
                    "quantity": map_drop[1]
                })
        case "LTG.HammerChest.MTX.Normal.Hit":
            items.append({
                "itemType": "Currency:MtxGiveaway",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                "itemProfile": "profile0",
                "quantity": random.randint(5, 8)
            })
        case "LTG.HammerChest.MTX.Normal.Destroy":
            items.append({
                "itemType": "Currency:MtxGiveaway",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                "itemProfile": "profile0",
                "quantity": random.randint(52, 99)
            })
        case "LTG.HammerChest.MTX.Rare.Hit":
            items.append({
                "itemType": "Currency:MtxGiveaway",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                "itemProfile": "profile0",
                "quantity": random.randint(10, 18)
            })
        case "LTG.HammerChest.MTX.Rare.Destroy":
            items.append({
                "itemType": "Currency:MtxGiveaway",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"),
                "itemProfile": "profile0",
                "quantity": random.randint(130, 195)
            })
        case "LTG.HammerChest.Pet.Normal.Hit":
            items.append({
                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 5)
            })
        case "LTG.HammerChest.Pet.Normal.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite"),
                "itemProfile": "profile0",
                "quantity": random.randint(20, 25)
            })
        case "LTG.HammerChest.Pet.Rare.Hit":
            items.append({
                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite"),
                "itemProfile": "profile0",
                "quantity": random.randint(3, 7)
            })
        case "LTG.HammerChest.Pet.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_SupplyPoints_Elite",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_SupplyPoints_Elite"),
                "itemProfile": "profile0",
                "quantity": random.randint(38, 40)
            })
        case "LTG.HammerChest.Tutorial.Hit":
            match random.randint(0, 2):
                case 0:
                    items.append({
                        "itemType": "Currency:HeroXp_Basic",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:HeroXp_Basic"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(1000, 2000)
                    })
                case 1:
                    items.append({
                        "itemType": "Currency:Gold",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:Gold"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(5000, 10000)
                    })
                case 2:
                    items.append({
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(
                            "Reagent:Reagent_HeroMap_Elemental"),
                        "itemProfile": "profile0",
                        "quantity": 100
                    })
            # legion spearman
        case "LTG.HammerChest.Tutorial.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_HeroMap_Bronze",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_HeroMap_Bronze"),
                "itemProfile": "profile0",
                "quantity": 1
            })
        case "LTG.HammerChest.Upgrade.Advanced.Normal.Hit":
            potion = random.choice(["UpgradePotion:UpgradeHealthMajor", "UpgradePotion:UpgradeStrengthMajor"])
            items.append({
                "itemType": potion,
                "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 5)
            })
        case "LTG.HammerChest.Upgrade.Advanced.Normal.Destroy":
            items.append({
                "itemType": "UpgradePotion:UpgradeMana",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana"),
                "itemProfile": "profile0",
                "quantity": random.randint(2, 4)
            })
        case "LTG.HammerChest.Upgrade.Advanced.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    potion = random.choice(["UpgradePotion:UpgradeHealthMajor", "UpgradePotion:UpgradeStrengthMajor"])
                    items.append({
                        "itemType": potion,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                        "itemProfile": "profile0",
                        "quantity": random.randint(3, 7)
                    })
                case 1:
                    items.append({
                        "itemType": "UpgradePotion:UpgradeMana",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    })
        case "LTG.HammerChest.Upgrade.Advanced.Rare.Destroy":
            items.append({
                "itemType": "UpgradePotion:UpgradeMana",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana"),
                "itemProfile": "profile0",
                "quantity": random.randint(3, 6)
            })
        case "LTG.HammerChest.Upgrade.Basic.Normal.Hit":
            match random.randint(0, 2):
                case 0:
                    potion = random.choice(["UpgradePotion:UpgradeHealthMinor", "UpgradePotion:UpgradeStrengthMinor"])
                    items.append({
                        "itemType": potion,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                        "itemProfile": "profile0",
                        "quantity": random.randint(6, 10)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(11, 22)
                    })
                case 2:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(46, 96)
                    })
        case "LTG.HammerChest.Upgrade.Basic.Normal.Destroy":
            match random.randint(0, 2):
                case 0:
                    potion = random.choice(["UpgradePotion:UpgradeHealthMinor", "UpgradePotion:UpgradeStrengthMinor"])
                    items.append({
                        "itemType": potion,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                        "itemProfile": "profile0",
                        "quantity": random.randint(53, 64)
                    })
                case 1:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(1141, 1923)
                    })
                case 2:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(187, 193)
                    })
        case "LTG.HammerChest.Upgrade.Basic.Rare.Hit":
            match random.randint(0, 2):
                case 0:
                    potion = random.choice(["UpgradePotion:UpgradeHealthMinor", "UpgradePotion:UpgradeStrengthMinor"])
                    items.append({
                        "itemType": potion,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                        "itemProfile": "profile0",
                        "quantity": random.randint(9, 20)
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(26, 47)
                    })
                case 2:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(123, 129)
                    })
        case "LTG.HammerChest.Upgrade.Basic.Rare.Destroy":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": 3761
                    })
                case 1:
                    items.append({
                        "itemType": "Reagent:Reagent_Shared_T02",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_T02"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(202, 243)
                    })
        case "LTG.HammerChest.Upgrade.Mana.Rare.Hit":
            match random.randint(0, 1):
                case 0:
                    items.append({
                        "itemType": "Currency:SkillXP",
                        "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:SkillXP"),
                        "itemProfile": "profile0",
                        "quantity": random.randint(50, 100)
                    })
                case 1:
                    potion = random.choice(["UpgradePotion:UpgradeHealthMajor", "UpgradePotion:UpgradeStrengthMajor"])
                    items.append({
                        "itemType": potion,
                        "itemGuid": await request.ctx.profile.find_item_by_template_id(potion),
                        "itemProfile": "profile0",
                        "quantity": random.randint(3, 6)
                    })
            streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, 50000, 2000)
            if streakbreaker_id:
                await request.ctx.profile.change_item_quantity(streakbreaker_id, streakbreaker_roll[1] + 1)
            else:
                await request.ctx.profile.add_item({
                    "templateId": "Currency:SB_Hammer",
                    "attributes": {},
                    "quantity": streakbreaker_roll[1] + 1
                })
            if streakbreaker_roll[0]:
                items.append({
                    "itemType": "UpgradePotion:UpgradeMana",
                    "itemGuid": await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana"),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
        case "LTG.HammerChest.Upgrade.Mana.Rare.Destroy":
            items.append({
                "itemType": "UpgradePotion:UpgradeMana",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana"),
                "itemProfile": "profile0",
                "quantity": random.randint(6, 10)
            })
        case "LTG.HammerChest.WhatThe.Rare.Hit":
            element = random.choice(["Dark", "Fire", "Light", "Nature", "Water"])
            tier = random.choice(["T03", "T04"])
            items.append({
                "itemType": f"Character:Special_Treasure_{element}_{tier}",
                "itemGuid": [],
                "itemProfile": "profile0",
                "quantity": 1
            })
        case "LTG.HammerChest.WhatThe.Rare.Destroy":
            items.append({
                "itemType": "Reagent:Reagent_Shared_MysteryGoo",
                "itemGuid": await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_MysteryGoo"),
                "itemProfile": "profile0",
                "quantity": random.randint(1, 2)
            })
    await request.ctx.profile.change_item_quantity(hammer_id[0], hammer_quantity)
    for item in items:
        if not item.get("itemGuid"):
            if item.get("itemType").startswith("Character:"):
                guid = await request.ctx.profile.add_item({
                    "templateId": item.get("itemType"),
                    "attributes": {
                        "gear_weapon_item_id": "",
                        "weapon_unlocked": False,
                        "sidekick_template_id": "",
                        "is_new": True,
                        "level": 1,
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
                    "quantity": item.get("quantity")
                })
                item["itemGuid"] = guid
            else:
                await request.ctx.profile.add_item({
                    "templateId": item.get("itemType"),
                    "attributes": {},
                    "quantity": item.get("quantity")
                })
        else:
            current_quantity = (await request.ctx.profile.get_item_by_guid(item.get("itemGuid")[0])).get("quantity")
            await request.ctx.profile.change_item_quantity(item.get("itemGuid")[0],
                                                           current_quantity + item.get("quantity"))
            item["itemGuid"] = item.get("itemGuid")[0]
    await request.ctx.profile.add_notifications({
        "type": "WExpHammerChestOpened",
        "primary": True,
        "templateId": chest_item.get("templateId"),
        "bCompleted": completed,
        "lootResult": {
            "tierGroupName": loot_tier_group,
            "items": items
        }
    })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
