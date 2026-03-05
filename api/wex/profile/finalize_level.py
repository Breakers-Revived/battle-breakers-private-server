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
import sanic.log

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
    if request.json.get("claimDepth") < level_item["attributes"]["debug_roomcount"]:
        level_complete_notification[0]["completed"] = False
    first_clear = False
    for unlocked_level_guids in (await request.ctx.profile.find_item_by_template_id("WorldUnlock:Level",
                                                                                    request.ctx.profile_id)):
        level_unlock = await request.ctx.profile.get_item_by_guid(unlocked_level_guids, request.ctx.profile_id)
        if level_unlock["attributes"]["levelId"] == level_id or not level_complete_notification[0]["completed"]:
            break
    else:
        first_clear = True
        await request.ctx.profile.add_item({
            "templateId": "WorldUnlock:Level",
            "attributes": {
                "levelId": level_id
            },
            "quantity": 1
        }, profile_id=request.ctx.profile_id)
        await request.ctx.profile.modify_stat("num_levels_completed", stars + difficulty)
    await request.ctx.profile.modify_stat("last_played_level", level_id, profile_id=request.ctx.profile_id)
    async with aiofiles.open("res/wex/api/calendar/battlepass.ics", "rb") as f:
        events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
            datetime.datetime.now(datetime.UTC)
        )
    event_data = await load_datatable(events[-1].get("DESCRIPTION")[1:])
    event_currency = await utils.utils.get_event_currency()
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
                chest_data = (await load_datatable(
                    (await utils.utils.get_path_from_template_id(item["itemTemplateId"])).replace(
                        "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0][
                    "Properties"]
                items = await request.ctx.profile.grant_loot_from_tiergroup(chest_data["TierGroup"])
                if items is not None:
                    level_complete_notification[0]["loot"].append({
                        "tierGroupName": chest_data["TierGroup"],
                        "items": items
                    })
    # TODO: implement rest of LGTs
    if first_clear:
        items = await request.ctx.profile.grant_loot_from_tiergroup(level_info['FirstCompletionLoot'])
        if items is not None:
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.FirstInstance",
                "items": items
            })
    if level_complete_notification[0]["completed"]:
        items = await request.ctx.profile.grant_loot_from_tiergroup(level_info['CompletionLoot'])
        if items is not None:
            level_complete_notification[0]["loot"].append({
                "tierGroupName": "Level.Instance",
                "items": items
            })
    # TODO: update account level + xp + add perk choice + notification
    # increase level
    account_level_datatable = (await load_datatable("Content/Balance/Datatables/XPAccountLevels"))[0]["Rows"]
    current_account_level = await request.ctx.profile.get_stat("level")
    sanic.log.logger.debug(f"Current account level: {current_account_level}")
    # TODO: implement base account xp level to grant
    # grant bonus xp for playing breakers revived during launch
    level_complete_notification[0]["bonusAccountXp"] = int(
        level_complete_notification[0]["accountXp"] * (1.5 + (current_account_level / 100)))
    level_complete_notification[0]["accountXp"] += level_complete_notification[0]["bonusAccountXp"]
    sanic.log.logger.debug(f"Granted bonus account XP: {level_complete_notification[0]['bonusAccountXp']}")
    xp = await request.ctx.profile.get_stat("xp")
    sanic.log.logger.debug(f"Current account XP: {xp}")
    account_xp = xp + account_level_datatable.get(str(current_account_level), {"XpTotal": 521341325, "XpToNextLevel": 1054090})["XpTotal"]
    sanic.log.logger.debug(f"Total account XP: {account_xp}")
    granted_xp = level_complete_notification[0]["accountXp"]
    sanic.log.logger.debug(f"Total granted account XP: {granted_xp}")
    if xp + granted_xp > account_level_datatable.get(str(current_account_level), {"XpTotal": 521341325, "XpToNextLevel": 1054090})["XpToNextLevel"] and current_account_level < 999:
        level_up_times = 1
        await request.ctx.profile.grant_item(
            f"AccountReward:AccountPerk_{await utils.utils.reward_for_level(current_account_level + level_up_times)}")
        while account_xp + granted_xp >= account_level_datatable.get(str(current_account_level + level_up_times), {"XpTotal": 521341325, "XpToNextLevel": 1054090})["XpTotal"] and current_account_level + level_up_times < 999:
            level_up_times += 1
            await request.ctx.profile.grant_item(
                f"AccountReward:AccountPerk_{await utils.utils.reward_for_level(current_account_level + level_up_times)}")
        sanic.log.logger.debug(f"Leveled up {level_up_times} times to level {current_account_level + level_up_times}")
        await request.ctx.profile.modify_stat("level", current_account_level + level_up_times)
        await request.ctx.profile.add_notifications({
            "type": "AccountLevelUp",
            "primary": False,
            "level": current_account_level + level_up_times
        }, ProfileType.PROFILE0)
        # calculate leftover xp after level up
        xp = account_level_datatable.get(str(current_account_level + level_up_times), {"XpTotal": 521341325, "XpToNextLevel": 1054090})["XpTotal"] - (granted_xp + account_xp)
        sanic.log.logger.debug(f"Calculating leftover XP after level up with: {account_level_datatable.get(str(current_account_level + level_up_times), {'XpTotal': 521341325, 'XpToNextLevel': 1054090})['XpTotal']} - ({granted_xp} + {account_xp}) = {xp}")
    else:
        sanic.log.logger.debug(f"No level up occurred.")
        xp += granted_xp
    sanic.log.logger.debug(f"Final account XP to set: {xp}")
    await request.ctx.profile.modify_stat("xp", xp)
    # add account reward account perk
    # TODO: activity gift box accountlevelup & energyspent
    # TODO: update battle pass xp (season_xp)
    # TODO: determine what happens for events with multiple currency
    event_loot = []
    for currency_path in event_data[0]["Properties"]["EventCurrency"]:
        event_currency = await utils.utils.get_template_id_from_path(currency_path["AssetPathName"])
        event_loot.append({
            "itemType": event_currency,
            "itemGuid": await request.ctx.profile.grant_item(event_currency, 64 + battlepassxp),
            "itemProfile": "profile0",
            "quantity": 64 + battlepassxp
        })
    if event_loot:
        level_complete_notification[0]["loot"].append({
            "tierGroupName": "Level.EventsLoot",
            "items": event_loot
        })
    # TODO: challenge bonus
    await request.ctx.profile.add_notifications(level_complete_notification, ProfileType.LEVELS)
    # event_currency = await utils.utils.get_template_id_from_path(
    #     (await utils.utils.process_choices(event_data[0]["Properties"]["EventCurrency"]))["AssetPathName"])
    # element = await utils.utils.process_choices(["Nature", "Fire", "Water", "Dark", "Light", "Gear"])
    # level_complete_notification[0]["loot"].append({
    #     "tierGroupName": "Level.FirstInstance",
    #     "items": [{
    #         "itemType": event_currency,
    #         "itemGuid": await request.ctx.profile.grant_item(event_currency, 200),
    #         "itemProfile": "profile0",
    #         "quantity": 200
    #     }, {
    #         "itemType": f"Reagent:Reagent_Shard_{element}",
    #         "itemGuid": await request.ctx.profile.grant_item(f"Reagent:Reagent_Shard_{element}", 1),
    #         "itemProfile": "profile0",
    #         "quantity": 1
    #     }]
    # })
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
