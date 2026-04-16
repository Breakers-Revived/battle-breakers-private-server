"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming rewards from events
"""
import datetime

import aiofiles
import icalendar
import recurring_ical_events
import sanic
import sanic.log
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info, load_datatable, get_template_id_from_path
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_event_rewards = sanic.Blueprint("wex_profile_claim_event_rewards")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimEventRewards.md
@wex_profile_claim_event_rewards.route("/<accountId>/ClaimEventRewards", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.ClaimEventRewards, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def claim_event_rewards(request: types.BBProfileRequest, accountId: str,
                              body: MCPValidation.ClaimEventRewards,
                              query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used claim rewards from events
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # current_xp = await request.ctx.profile.get_stat("season_xp")
    current_claim_level = max(0, (await request.ctx.profile.get_stat("season_regular_claim_level")))
    current_premium_claim_level = max(0, (await request.ctx.profile.get_stat("season_premium_claim_level")))
    await request.app.ctx.calendar.update_required_events()
    current_event = request.app.ctx.calendar.battlepass.states[0].state.get("seasonId", "2018_1")
    is_premium = current_event in await request.ctx.profile.get_stat("battlepass_purchase_history")
    battlepass_tracker_ids = await request.ctx.profile.find_item_by_template_id("MajorEventTracker:BattlepassSeason")
    for battlepass_tracker_id in battlepass_tracker_ids:
        battlepass_tracker = await request.ctx.profile.get_item_by_guid(battlepass_tracker_id)
        if battlepass_tracker["attributes"]["seasonId"] == current_event:
            break
    else:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="No battlepass tracker for current season")
    current_battlepass_level = battlepass_tracker["attributes"]["level"]
    async with aiofiles.open("res/wex/api/calendar/battlepass.ics", "rb") as f:
        events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
            datetime.datetime.now(datetime.UTC)
        )
    event_data = await load_datatable(events[-1].get("DESCRIPTION")[1:])
    rewards_table = (await load_datatable(
        event_data[0]["Properties"]["RewardsTable"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
        "Rows"]
    free_tiers_to_claim = [str(i) for i in range(current_claim_level + 1, current_battlepass_level + 1)]
    sanic.log.logger.debug(f"Free tiers to claim: {free_tiers_to_claim}")
    premium_tiers_to_claim = [str(i) for i in range(current_premium_claim_level + 1, current_battlepass_level + 1)]
    sanic.log.logger.debug(f"Premium tiers to claim: {premium_tiers_to_claim}")
    items = []
    for tier in free_tiers_to_claim:
        reward = rewards_table[tier]
        if reward["bIsPremium"]:
            continue
        reward_path = reward['RewardItem']['ObjectPath']
        reward_quantity = reward['RewardCount']
        reward_template_id = await get_template_id_from_path(reward_path)
        if reward_template_id is None:
            raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                errorMessage=f"Invalid reward template id for level {tier}")
        if reward_template_id.startswith("Character:"):
            item_ids = await request.ctx.profile.grant_hero(reward_template_id, quantity=reward_quantity)
            if isinstance(item_ids, list):
                for item_id in item_ids:
                    items.append({"itemType": reward_template_id, "itemGuid": item_id, "itemProfile": "profile0",
                                  "quantity": 1})
            else:
                items.append({"itemType": reward_template_id, "itemGuid": item_ids, "itemProfile": "profile0",
                              "quantity": reward_quantity})
        else:
            attributes = None
            if reward_template_id.startswith("Gear:"):
                attributes = {
                    "is_new": True,
                    "is_disabled": False,
                    "hero_item_id": "",
                    "extra_affixes": [],
                    "rarity": reward["GearRarity"][13:]
                }
                if reward["GearAffix1"] is not None:
                    attributes["extra_affixes"].append(reward["GearAffix1"]["ObjectName"][14:-1])
                if reward["GearAffix2"] is not None:
                    attributes["extra_affixes"].append(reward["GearAffix2"]["ObjectName"][14:-1])
            items.append({
                "itemType": reward_template_id,
                "itemGuid": await request.ctx.profile.grant_item(reward_template_id, reward_quantity, attributes),
                "itemProfile": "profile0",
                "quantity": reward_quantity
            })
    await request.ctx.profile.modify_stat("season_regular_claim_level", current_battlepass_level)
    if is_premium:
        for tier in premium_tiers_to_claim:
            reward = rewards_table[tier]
            if not reward["bIsPremium"]:
                continue
            reward_path = reward['RewardItem']['ObjectPath']
            reward_quantity = reward['RewardCount']
            reward_template_id = await get_template_id_from_path(reward_path)
            if reward_template_id is None:
                raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                    errorMessage=f"Invalid reward template id for level {tier}")
            if reward_template_id.startswith("Character:"):
                item_ids = await request.ctx.profile.grant_hero(reward_template_id, quantity=reward_quantity)
                if isinstance(item_ids, list):
                    for item_id in item_ids:
                        items.append({"itemType": reward_template_id, "itemGuid": item_id, "itemProfile": "profile0",
                                      "quantity": 1})
                else:
                    items.append({"itemType": reward_template_id, "itemGuid": item_ids, "itemProfile": "profile0",
                                  "quantity": reward_quantity})
            else:
                attributes = None
                if reward_template_id.startswith("Gear:"):
                    attributes = {
                        "is_new": True,
                        "is_disabled": False,
                        "hero_item_id": "",
                        "extra_affixes": [],
                        "rarity": reward["GearRarity"][13:]
                    }
                    if reward["GearAffix1"] is not None:
                        attributes["extra_affixes"].append(reward["GearAffix1"]["ObjectName"][14:-1])
                    if reward["GearAffix2"] is not None:
                        attributes["extra_affixes"].append(reward["GearAffix2"]["ObjectName"][14:-1])
                items.append({
                    "itemType": reward_template_id,
                    "itemGuid": await request.ctx.profile.grant_item(reward_template_id, reward_quantity, attributes),
                    "itemProfile": "profile0",
                    "quantity": reward_quantity
                })
        await request.ctx.profile.modify_stat("season_premium_claim_level", current_battlepass_level)
    await request.ctx.profile.add_notifications({
        "type": "WExpGiftPointReward",
        "primary": True,
        "totalPoints": current_battlepass_level,
        "lootResult": {
            "items": items
        }
    })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
