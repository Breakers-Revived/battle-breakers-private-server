"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles updating the monster pit power.
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, calculate_hero_power, load_datatable, get_template_id_from_path, \
    extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_update_monster_pit_power = sanic.Blueprint("wex_profile_update_monster_pit_power")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateMonsterPitPower.md
@wex_profile_update_monster_pit_power.route("/<accountId>/UpdateMonsterPitPower", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpdateMonsterPitPower, query=MCPQueryValidation.MCPMonsterpit)
@compress.compress()
async def update_monster_pit_power(request: types.BBProfileRequest, accountId: str,
                                   body: MCPValidation.UpdateMonsterPitPower,
                                   query: MCPQueryValidation.MCPMonsterpit) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the monster pit power
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    all_pitted_hero_ids = await request.ctx.profile.find_items_by_type("Character", ProfileType.MONSTERPIT)
    total_pit_power = 0
    for hero_id in all_pitted_hero_ids:
        hero_data = await request.ctx.profile.get_item_by_guid(hero_id, ProfileType.MONSTERPIT)
        total_pit_power += await calculate_hero_power(hero_data, True)
    await request.ctx.profile.modify_stat("pit_power", total_pit_power, ProfileType.MONSTERPIT)
    monsterpit_levels_datatable = (await load_datatable("Content/Menus/Headquarters/MonsterPitLevels"))[0]["Rows"]
    current_pit_level = await request.ctx.profile.get_stat("pit_level", ProfileType.MONSTERPIT)
    new_pit_level = 0
    for level in monsterpit_levels_datatable:
        if monsterpit_levels_datatable[level]["TotalXpToGetToThisLevel"] <= total_pit_power:
            new_pit_level = monsterpit_levels_datatable[level]["Level"]
        else:
            break
    await request.ctx.profile.modify_stat("pit_level", new_pit_level, ProfileType.MONSTERPIT)
    highest_pit_power = await request.ctx.profile.get_stat("highest_pit_power", ProfileType.MONSTERPIT)
    if total_pit_power > highest_pit_power:
        await request.ctx.profile.modify_stat("highest_pit_power", total_pit_power, ProfileType.MONSTERPIT)
    highest_previous_level = 0
    for level in monsterpit_levels_datatable:
        if monsterpit_levels_datatable[level]["TotalXpToGetToThisLevel"] <= highest_pit_power:
            highest_previous_level = monsterpit_levels_datatable[level]["Level"]
        else:
            break
    if new_pit_level > highest_previous_level:
        levels_gained = new_pit_level - highest_previous_level
        items = []
        for i in range(levels_gained):
            level_data = monsterpit_levels_datatable[str(highest_previous_level + i + 1)]
            reward_path = level_data['RewardItem']['ObjectPath']
            reward_quantity = level_data['RewardCount']
            reward_template_id = await get_template_id_from_path(reward_path)
            if reward_template_id is None:
                raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                    errorMessage=f"Invalid reward template id for level {highest_previous_level + i + 1}")
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
                items.append({
                    "itemType": reward_template_id,
                    "itemGuid": await request.ctx.profile.grant_item(reward_template_id, reward_quantity),
                    "itemProfile": "profile0",
                    "quantity": reward_quantity
                })
        await request.ctx.profile.add_notifications({
            "type": "WExpMonsterPitLevelUp",
            "primary": True,
            "level": new_pit_level,
            "lootResult": {
                "tierGroupName": f"MonsterPit:{new_pit_level}",
                "items": items
            }
        }, ProfileType.MONSTERPIT)
    # TODO: activity chest
    await request.ctx.profile.modify_stat("pit_power_dirty", False, ProfileType.MONSTERPIT)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
