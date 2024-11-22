"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles finalizing levels
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.enums import ProfileType
from utils.utils import authorized as auth

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
        print(level_id)
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
    for unlocked_level_guids in (await request.ctx.profile.find_item_by_template_id("WorldUnlock:Level",
                                                                                    request.ctx.profile_id)):
        level_unlock = await request.ctx.profile.get_item_by_guid(unlocked_level_guids, request.ctx.profile_id)
        if level_unlock["attributes"]["levelId"] == level_id:
            break
    else:
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
    # TODO: implement ltg for level instance loot
    if request.json.get("claimDepth") < level_item["attributes"]["debug_roomcount"]:
        level_complete_notification[0]["completed"] = False
    await request.ctx.profile.add_notifications(level_complete_notification, ProfileType.LEVELS)
    # TODO: implement base account xp level to grant
    # grant bonus xp for playing breakers revived during launch
    level_complete_notification[0]["bonusAccountXp"] = int(level_complete_notification[0]["accountXp"] * (1.5 + ((await request.ctx.profile.get_stat("level")) / 100)))
    # TODO: update account level + xp + add perk choice + notification
    # TODO: activity gift box
    # TODO: award level loot
    # TODO: update battle pass xp/currency
    # TODO: update score
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
            }, ProfileType.MONSTERPIT)
    # TODO: LevelRunMarker for limited run rooms
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
