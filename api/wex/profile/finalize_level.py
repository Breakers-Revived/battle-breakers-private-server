"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles finalizing levels
"""
import datetime

import aiofiles
import icalendar
import recurring_ical_events
import sanic

import utils.utils
from utils import types
from utils.exceptions import errors
from utils.enums import ProfileType
from utils.utils import authorized as auth, load_datatable

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_finalize_level = sanic.Blueprint("wex_profile_finalize_level")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/FinalizeLevel.md
@wex_profile_finalize_level.route("/<accountId>/FinalizeLevel", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def finalize_level(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to finalize a level upon completion / abandoning
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    try:
        level_item = await request.ctx.profile.get_item_by_guid(request.json.get("levelItemId"), request.ctx.profile_id)
        level_id = level_item["attributes"]["debug_name"]
        level_info = (await load_datatable("Content/World/Datatables/LevelInfo"))[0]["Rows"].get(level_id)
    except:
        raise errors.com.epicgames.world_explorers.level_not_found(
            errorMessage="Sorry, the level you completed could not be found.")
    stars = await request.ctx.profile.get_stat("num_levels_completed")
    try:
        difficulty = int(level_id[-1])
    except ValueError:
        difficulty = 1
    await request.ctx.profile.clear_notifications(ProfileType.LEVELS)
    await request.ctx.profile.remove_item(request.json.get("levelItemId"), request.ctx.profile_id)
    first_clear = True
    for unlocked_level_guids in (await request.ctx.profile.find_item_by_template_id("WorldUnlock:Level",
                                                                                    request.ctx.profile_id)):
        level_unlock = await request.ctx.profile.get_item_by_guid(unlocked_level_guids, request.ctx.profile_id)
        if level_unlock["attributes"]["levelId"] == level_id:
            break
    else:
        first_clear = False
        await request.ctx.profile.add_item({
            "templateId": "WorldUnlock:Level",
            "attributes": {
                "levelId": level_id
            },
            "quantity": 1
        }, profile_id=request.ctx.profile_id)
        await request.ctx.profile.modify_stat("num_levels_completed", stars + difficulty)
    await request.ctx.profile.modify_stat("last_played_level", level_id, profile_id=request.ctx.profile_id)
    level_complete_notification = [
        {
            "type": "WExpLevelCompleted",
            "primary": False,
            "accountXp": 0,
            "bonusAccountXp": 0,
            "levelId": level_id,
            "completed": True,
            "loot": []
        }
    ]
    battlepassxp = 0
    for item in request.json.get("claimedItems", []):
        match item["itemTemplateId"].split(":")[0]:
            case "Currency":
                item_id = await request.ctx.profile.grant_item(item["itemTemplateId"], item["quantity"])
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "",
                    "items": [{
                        "itemType": item["itemTemplateId"],
                        "itemGuid": item_id,
                        "itemProfile": "profile0",
                        "quantity": item["quantity"]
                    }]
                })
            case "StandIn":
                if item["itemTemplateId"] == "StandIn:AccountXp":
                    level_complete_notification[0]["accountXp"] += item["quantity"]
                elif item["itemTemplateId"] == "StandIn:BattlepassXp":
                    battlepassxp += item["quantity"]
            case "Container":
                # TODO: implement ltg for chest containers
                pass
    # TODO: implement rest of LGTs ("Reagent:Reagent_Shared_T03", 1) = placeholder
    if first_clear:
        match level_info["FirstCompletionLoot"]:
            case "LTG.Event.Completion.GrandArena.Bonus":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.EasternKingdoms.Beard":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map2":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map3":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map4":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map5":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map6":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map7":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Event.NewPlayer.Map8":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.AbyssalPrecipice.Map8.D1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.BurnyVolcano.Map1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Voucher:Voucher_Chest_Gold",
                        "itemGuid": await request.ctx.profile.grant_item("Voucher:Voucher_Chest_Gold", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }, {
                        "itemType": "Unlockable:Unlockable_Duels",
                        "itemGuid": await request.ctx.profile.grant_item("Unlockable:Unlockable_Duels", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ClassTraining.Normal":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ClassTraining.VeryHigh":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.CollapsedSpire.Map7.D1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Event.TKVoucher":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Event.TKVoucher.Silver":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental", 100),
                        "itemProfile": "profile0",
                        "quantity": 100
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map1.D2":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "UpgradePotion:UpgradeStrengthMinor",
                        "itemGuid": await request.ctx.profile.grant_item("UpgradePotion:UpgradeStrengthMinor", 5),
                        "itemProfile": "profile0",
                        "quantity": 5
                    }, {
                        "itemType": "Unlockable:Unlockable_Elixirs",
                        "itemGuid": await request.ctx.profile.grant_item("Unlockable:Unlockable_Elixirs", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map2":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Currency:HeroXp_Basic",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:HeroXp_Basic", 500),
                        "itemProfile": "profile0",
                        "quantity": 500
                    }, {
                        "itemType": "Character:Pet_C1_Water_Magekoi_T02",
                        "itemGuid": await request.ctx.profile.grant_hero("Character:Pet_C1_Water_Magekoi_T02"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }, {
                        "itemType": "Reagent:Reagent_HeroMap_Bronze",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Bronze", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map3":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Currency:HeroXp_Basic",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:HeroXp_Basic", 1500),
                        "itemProfile": "profile0",
                        "quantity": 1500
                    }, {
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental", 100),
                        "itemProfile": "profile0",
                        "quantity": 100
                    }, {
                        "itemType": "TreasureMap:TM_MapResource",
                        "itemGuid": await request.ctx.profile.grant_item("TreasureMap:TM_MapResource", 35),
                        "itemProfile": "profile0",
                        "quantity": 35
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map4":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "UpgradePotion:UpgradeHealthMinor",
                        "itemGuid": await request.ctx.profile.grant_item("UpgradePotion:UpgradeHealthMinor", 3),
                        "itemProfile": "profile0",
                        "quantity": 3
                    }, {
                        "itemType": "Voucher:Voucher_Hero_TreasureHunter_Water_PowerEfflux",
                        "itemGuid": await request.ctx.profile.grant_item("Voucher:Voucher_Hero_TreasureHunter_Water_PowerEfflux", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map5":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Reagent:Reagent_HeroMap_Elemental",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_Elemental", 100),
                        "itemProfile": "profile0",
                        "quantity": 100
                    }, {
                        "itemType": "Character:Warrior_Starter_Dark_RoboGuy_T02",
                        "itemGuid": await request.ctx.profile.grant_hero("Character:Warrior_Starter_Dark_RoboGuy_T02"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }, {
                        "itemType": "Character:Warrior_Starter_Dark_RoboGuy_T02",
                        "itemGuid": await request.ctx.profile.grant_hero("Character:Warrior_Starter_Dark_RoboGuy_T02"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }, {
                        "itemType": "Character:Warrior_Starter_Dark_RoboGuy_T02",
                        "itemGuid": await request.ctx.profile.grant_hero("Character:Warrior_Starter_Dark_RoboGuy_T02"),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map6":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }, {
                        "itemType": "Voucher:Voucher_Hero_Mage_Fire_BurningSword",
                        "itemGuid": await request.ctx.profile.grant_item("Voucher:Voucher_Hero_Mage_Fire_BurningSword", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map7":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "TreasureMap:TM_ForestOfMixedEmotions_Map8",
                        "itemGuid": await request.ctx.profile.grant_item("TreasureMap:TM_ForestOfMixedEmotions_Map8", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }, {
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 50),
                        "itemProfile": "profile0",
                        "quantity": 50
                    }, {
                        "itemType": "Unlockable:Unlockable_Quests",
                        "itemGuid": await request.ctx.profile.grant_item("Unlockable:Unlockable_Quests", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForestOfMixedEmotions.Map8":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 75),
                        "itemProfile": "profile0",
                        "quantity": 75
                    }]
                })
            case "LTG.FC.ForgottenLands.Default":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.ForgottenLands.Map11":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Mage.Water.BloodMagic":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.MTXPoints":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Currency:MtxGiveaway",
                        "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                        "itemProfile": "profile0",
                        "quantity": 20
                    }]
                })
            case "LTG.FC.MTXPointsExtreme":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.MTXPointsHigh":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.MTXPointsMedium":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.MTXPointsRidiculous":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.MTXPointsVeryHigh":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.OasisOfLife.Map1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Onboarding1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Onboarding2":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.OvergrownCastle.Map8":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.High.Dark":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.High.Fire":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.High.Light":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.High.Nature":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.High.Water":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.Low":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.Medium":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.RegionBoss.VeryHigh":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Special.AbyssalMaelstrom.D4":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Dark":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Dark.High":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Fire":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Fire.High":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Light":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Light.High":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Nature":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Nature.High":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Water":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.FC.Trial.Water.High":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.PE.MidgameChallenge.Completion":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Pet.Rockbeast":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Pet_Rockbeast",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Pet_Rockbeast", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.Special.LunarBonusMission.Region1":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TK.Special.GhostShip":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.ForestOfMixedEmotions.Map8":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.03":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.05":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.06":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.07":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.08":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.09":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.10":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.11":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.MapResource.12":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.OvergrownCastle.Map8":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.Special.BridgeOfLight":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.WaterfallValley.Map7":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case "LTG.TM.WaterfallValley.Map7.ClassTraining":
                level_complete_notification[0]["loot"].append({
                    "tierGroupName": "Level.FirstInstance",
                    "items": [{
                        "itemType": "Reagent:Reagent_Shared_T03",
                        "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                        "itemProfile": "profile0",
                        "quantity": 1
                    }]
                })
            case _:
                pass
    match level_info["CompletionLoot"]:
        case "LTG.BattlePass.EasternKingdoms.Completion.T00":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.BattlePass.EasternKingdoms.Completion.T01":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.BattlePass.EasternKingdoms.Completion.T02":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.BattlePass.EasternKingdoms.Completion.T03":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.BattlePass.EasternKingdoms.Completion.T04":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.BattlePass.EasternKingdoms.Completion.T05":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.AbyssalPrecipice.Map8.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.AbyssalPrecipice.Map8.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.AbyssalPrecipice.Map8.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.AbyssalPrecipice.Map8.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.All.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.All.Low":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.All.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.All.VeryLow":
            loot_choice = await utils.utils.process_choices([["Reagent:Reagent_Shared_T03", 1], ["Reagent:Reagent_Shared_T02", await utils.utils.process_choices([1, 2, 2, 3])], ["Currency:HeroXp_Basic", await utils.utils.process_choices([400, 600])]])
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": loot_choice[0],
                    "itemGuid": await request.ctx.profile.grant_item(loot_choice[0], loot_choice[1]),
                    "itemProfile": "profile0",
                    "quantity": loot_choice[1]
                }]
            })
        case "LTG.Completion.BlessedPlains.Map10.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BlessedPlains.Map10.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BlessedPlains.Map10.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BlessedPlains.Map10.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BurnyVolcano.Map6.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BurnyVolcano.Map6.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BurnyVolcano.Map6.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.BurnyVolcano.Map6.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Dark.Extreme":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Dark.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Dark.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Dark.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.CharacterShard":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.ElementalShard":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.ElixirsPack":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.Gold":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.HeroBronze":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.HeroSilver":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.MagicChest":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.PowerfulEssence":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.PowerSources":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.RareMine":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.BossChallenge.TreasureMap":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.ElementalShard":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Dark":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Fire":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Light":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Nature":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Silver.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Silver.Low":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Silver.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Silver.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.TKVoucher.Water":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.Weekend.CharacterShard":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.Weekend.MapFragments":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.Weekend.PortalEnergy":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Event.Weekend.PowerSources":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.FieldsOfDespair.Map8.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.FieldsOfDespair.Map8.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.FieldsOfDespair.Map8.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.FieldsOfDespair.Map8.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Fire.Extreme":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Fire.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Fire.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Fire.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map10":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map11":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map5":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map6":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map7":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map8":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.ForgottenLands.Map9":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Blitz":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Element.Dark":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Element.Fire":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Element.Light":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Element.Nature":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Element.Water":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Elixirs.Major":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Elixirs.Mana":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HallsOfFadedGlory.Elixirs.Minor":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HauntedWoods.Map7.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HauntedWoods.Map7.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HauntedWoods.Map7.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HauntedWoods.Map7.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HeavenlyPlane.Map8.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HeavenlyPlane.Map8.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HeavenlyPlane.Map8.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.HeavenlyPlane.Map8.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.JungleOfTheBeasts.Map7.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.JungleOfTheBeasts.Map7.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.JungleOfTheBeasts.Map7.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.JungleOfTheBeasts.Map7.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.LeafyTreeland.Map7.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.LeafyTreeland.Map7.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.LeafyTreeland.Map7.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.LeafyTreeland.Map7.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Light.Extreme":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Light.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Light.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Light.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map1.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map1.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map1.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map1.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map2.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map2.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map2.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map2.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map3.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map3.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map3.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map3.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map4.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map4.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map4.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Mine.Map4.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.MoltenCaverns.Map9.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.MoltenCaverns.Map9.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.MoltenCaverns.Map9.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.MoltenCaverns.Map9.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Nature.Extreme":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Nature.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Nature.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Nature.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.OasisOfLife.Map4.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.OasisOfLife.Map4.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.OasisOfLife.Map4.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.OasisOfLife.Map4.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.OvergrownCastle.Map8":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.BridgeOfLight":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.EasterEggDesert":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.GhostShip.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.GhostShip.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.GhostShip.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.GhostShip.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.MeegCity":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.PlanetCore.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.PlanetCore.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.PlanetCore.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.PlanetCore.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterForest.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterForest.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterForest.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterForest.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterTunnel.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterTunnel.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterTunnel.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Special.UnderwaterTunnel.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Water.Extreme":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Water.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Water.Medium":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.Water.VeryHigh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map6.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map6.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map6.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map6.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map7.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map7.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map7.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WaterfallValley.Map7.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WindingRivers.Map7.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WindingRivers.Map7.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WindingRivers.Map7.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WindingRivers.Map7.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WithinTheVolcano.Map9.D1":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WithinTheVolcano.Map9.D2":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WithinTheVolcano.Map9.D3":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Completion.WithinTheVolcano.Map9.D4":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Completion.Bonus":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Daily.Kailani":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Daily.Kaleb":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Daily.Mirra":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Medusa.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Week1.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Week2.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.DarkGenerals.Week3.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.ChallengeSet.NinjaPlusATK":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.ChallengeSet.NoDefPuzzle":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.ChallengeSet.NoManaPuzzle":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.ChallengeSet.Rainbow":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkFrost":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkFrost.Bonus":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.East":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.Final":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.North":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.South":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.StandingStones":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DarkGenerals.West":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Ambush":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Escape":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Intel":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Quartermaster":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Sellsword":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Steal":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.SupplyBase":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.DisruptingTheLegion.Thugs":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.GrandArena.Core":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.GrandArena.MainStage":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.GrandArena.Unsanctioned":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.ForestNinja":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.ForestNinja.MB":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.GroundLava":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.GroundLava.MB":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.MageBane":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.TheivesGuild.MB":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.ThievesGuild":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.UnnaturalBlade":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.SE.UnnaturalBlade.MB":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.Skyfall":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.Skyfall.Final":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.Completion.Skyfall.Story":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.DisruptTheLegion.MB":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.EasternKingdoms.Beard":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.FifthGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.FirstGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.FourthGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.GatePrime":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.SecondGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.SeventhGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.SixthGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.ThirdGate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Alcazar.WorldKey":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.AppealDark":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.AppealLight":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Darkwood.Basin":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Darkwood.Falls":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Darkwood.Overlook":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Darkwood.Scar":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Darkwood.Wall":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.DuelingPrince.DarkLabyrinth":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.DuelingPrince.FrontLines":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.DuelingPrince.LightLabyrinth":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Manipulators":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.MoltenPeak.Descent":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.MoltenPeak.Grotto":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.MoltenPeak.Heart":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.MoltenPeak.Pit":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.MoltenPeak.Warden":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Fifth":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.First":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Fourth":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Second":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Seventh":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Sixth":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.Nightbane.Third":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Cardinalate":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Cathedral":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Conclave":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Fervor":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Redwind":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.GC.SunScarred.Wellhaven":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.MorrowBlackSite.Apothecary.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.MorrowBlackSite.Block.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.MorrowBlackSite.BotanicVault.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.MorrowBlackSite.Containment.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Event.MorrowBlackSite.Laboratory.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.FC.MTXPoints":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": await request.ctx.profile.grant_item("Currency:MtxGiveaway", 20),
                    "itemProfile": "profile0",
                    "quantity": 20
                }]
            })
        case "LTG.PE.MidgameChallenge.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.PE.MidgameChallenge.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.PE.MidgamePet.Completion":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.PE.MidgamePet.Panda":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Seraph.Elixirs.Rewards":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Seraph.Evo.Rewards":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Seraph.Evo.Rewards.Complete":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Seraph.SkillXP.Rewards":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Special.Cloud5":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.Special.Cloud5.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.WC.Completion.WeekendReward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.WC.FC.WeekendReward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.WinterHoliday.Currency.Gather":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.WinterHoliday.Currency.High":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case "LTG.WinterHoliday.Reindeer.Reward":
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": [{
                    "itemType": "Reagent:Reagent_Shared_T03",
                    "itemGuid": await request.ctx.profile.grant_item("Reagent:Reagent_Shared_T03", 1),
                    "itemProfile": "profile0",
                    "quantity": 1
                }]
            })
        case _:
            pass
    if request.json.get("claimDepth") < level_item["attributes"]["debug_roomcount"]:
        level_complete_notification[0]["completed"] = False
    await request.ctx.profile.add_notifications(level_complete_notification, ProfileType.LEVELS)
    # TODO: implement base account xp level to grant
    # grant bonus xp for playing breakers revived during launch
    level_complete_notification[0]["bonusAccountXp"] = int(
        level_complete_notification[0]["accountXp"] * (1.5 + ((await request.ctx.profile.get_stat("level")) / 100)))
    # TODO: update account level + xp + add perk choice + notification
    # TODO: activity gift box
    # TODO: update battle pass xp
    async with aiofiles.open("res/wex/api/calendar/battlepass.ics", "rb") as f:
        events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
            datetime.datetime.now(datetime.UTC)
        )
    event_data = await load_datatable(events[-1].get("DESCRIPTION")[1:])
    # TODO: determine what happens for events with multiple currency
    # TODO: fix crash
    for currency_path in event_data[0]["Properties"]["EventCurrency"]:
        event_currency = await utils.utils.get_template_id_from_path(currency_path["AssetPathName"])
        level_complete_notification[0]["loot"].append({
            "tierGroupName": "Level.EventsLoot",
            "items": [{
                "itemType": event_currency,
                "itemGuid": await request.ctx.profile.grant_item(event_currency, 64 + battlepassxp),
                "itemProfile": "profile0",
                "quantity": 64 + battlepassxp
            }]
        })
    # TODO: update score for daily quests
    pit_unlocks = await request.ctx.profile.find_item_by_template_id("MonsterPitUnlock:Character",
                                                                     ProfileType.MONSTERPIT)
    seen_characters = request.json.get("seenCharacters", [])
    for character in seen_characters:
        for pit_unlock_guid in pit_unlocks:
            pit_unlock = await request.ctx.profile.get_item_by_guid(pit_unlock_guid, ProfileType.MONSTERPIT)
            if pit_unlock["attributes"]["characterId"] == character:
                break
        else:
            await request.ctx.profile.add_item({
                "templateId": "MonsterPitUnlock:Character",
                "attributes": {
                    "num_sold": 0,
                    "characterId": character
                },
                "quantity": 1
            }, profile_id=ProfileType.MONSTERPIT)
    # TODO: LevelRunMarker for limited run rooms
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
