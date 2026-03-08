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
    items = await request.ctx.profile.grant_loot_from_tiergroup(loot_tier_group)
    match loot_tier_group:
        case "LTG.HammerChest.Evolve.Dark.Normal.Hit" | "LTG.HammerChest.Evolve.Fire.Normal.Hit" | "LTG.HammerChest.Evolve.Light.Normal.Hit" | "LTG.HammerChest.Evolve.Nature.Normal.Hit" | "LTG.HammerChest.Evolve.Water.Normal.Hit":
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
                quantity = random.randint(5, 8)
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                    "itemProfile": "profile0",
                    "quantity": quantity
                })
        case "LTG.HammerChest.Evolve.Dark.Rare.Hit" | "LTG.HammerChest.Evolve.Fire.Rare.Hit" | "LTG.HammerChest.Evolve.Light.Rare.Hit" | "LTG.HammerChest.Evolve.Nature.Rare.Hit" | "LTG.HammerChest.Evolve.Water.Rare.Hit":
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
                quantity = random.randint(8, 17)
                items.append({
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                    "itemProfile": "profile0",
                    "quantity": quantity
                })
        case "LTG.HammerChest.Evolve.Shards.Normal.Hit":
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
                    "itemGuid": await request.ctx.profile.grant_item(random_essence),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
        case "LTG.HammerChest.Hero.Bronze.Normal.Hit":
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
                        quantity = random.randint(6, 8)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 1:
                        quantity = random.randint(3, 8)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental",
                                                                             quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 2:
                        quantity = random.randint(1, 2)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Bronze",
                                                                             quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
        case "LTG.HammerChest.Hero.Bronze.Rare.Hit":
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
                        quantity = random.randint(12, 15)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 1:
                        quantity = random.randint(5, 10)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.find_item_by_template_id(
                                "Reagent:Reagent_HeroMap_Elemental", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
        case "LTG.HammerChest.Hero.Gold.Rare.Hit":
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
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_RXT_Parts_Small"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 1:
                        quantity = random.randint(10, 11)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 3:
                        quantity = random.randint(16, 25)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental",
                                                                             quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
        case "LTG.HammerChest.Hero.Silver.Normal.Hit":
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
                        quantity = random.randint(5, 12)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 1:
                        quantity = random.randint(10, 15)
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Elemental",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental",
                                                                             quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
        case "LTG.HammerChest.Hero.Silver.Rare.Hit":
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
                        quantity = random.randint(11, 16)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
                        })
                    case 1:
                        items.append({
                            "itemType": "Reagent:Reagent_RXT_Parts_Small",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_RXT_Parts_Small"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
                    case 2:
                        items.append({
                            "itemType": "Reagent:Reagent_HeroMap_Bronze",
                            "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Bronze"),
                            "itemProfile": "profile0",
                            "quantity": 1
                        })
        case "LTG.HammerChest.LevelResources.Normal.Hit":
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
                        quantity = random.randint(5, 8)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
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
                            "itemGuid": await request.ctx.profile.grant_item(map_drop[0], map_drop[1]),
                            "itemProfile": "profile0",
                            "quantity": map_drop[1]
                        })
        case "LTG.HammerChest.LevelResources.Rare.Hit":
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
                        quantity = random.randint(10, 16)
                        items.append({
                            "itemType": "Currency:MtxGiveaway",
                            "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", quantity),
                            "itemProfile": "profile0",
                            "quantity": quantity
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
                            "itemGuid": await request.ctx.profile.grant_item(map_drop[0], map_drop[1]),
                            "itemProfile": "profile0",
                            "quantity": map_drop[1]
                        })
        case "LTG.HammerChest.Upgrade.Mana.Rare.Hit":
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
                    "itemGuid": await request.ctx.profile.grant_item("UpgradePotion:UpgradeMana"),
                    "itemProfile": "profile0",
                    "quantity": 1
                })
    await request.ctx.profile.change_item_quantity(hammer_id[0], hammer_quantity)
    for item in items:
        if not item.get("itemGuid"):
            if item.get("itemType").startswith("Character:"):
                item["itemGuid"] = await request.ctx.profile.grant_hero(item.get("itemType"),
                                                                        quantity=item.get("quantity"))
                if isinstance(item["itemGuid"], list):
                    item["itemGuid"] = item["itemGuid"][0]
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
