"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles updating the monster pit power.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.utils import authorized as auth, calculate_hero_power, load_datatable, get_template_id_from_path

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_update_monster_pit_power = sanic.Blueprint("wex_profile_update_monster_pit_power")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateMonsterPitPower.md
@wex_profile_update_monster_pit_power.route("/<accountId>/UpdateMonsterPitPower", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def update_monster_pit_power(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the monster pit power
    :param request: The request object
    :param accountId: The account id
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
        awarded_history = {}
        items = []
        for i in range(levels_gained):
            level_data = monsterpit_levels_datatable[str(highest_previous_level + i + 1)]
            reward_path = level_data['RewardItem']['ObjectPath']
            reward_quantity = level_data['RewardCount']
            reward_template_id = await get_template_id_from_path(reward_path)
            if reward_template_id.split(':')[0] == "Character":
                item_id = await request.ctx.profile.add_item({"templateId": reward_template_id,
                                                    "attributes": {"gear_weapon_item_id": "", "weapon_unlocked": False,
                                                                   "sidekick_template_id": "", "is_new": True, "level": 1,
                                                                   "num_sold": 0, "skill_level": 1,
                                                                   "sidekick_unlocked": False,
                                                                   "upgrades": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   "used_as_sidekick": False, "gear_armor_item_id": "",
                                                                   "skill_xp": 0, "armor_unlocked": False, "foil_lvl": -1,
                                                                   "xp": 0, "rank": 0, "sidekick_item_id": ""},
                                                    "quantity": reward_quantity})
                items.append({"itemType": reward_template_id, "itemGuid": item_id, "itemProfile": "profile0", "quantity": reward_quantity})
            else:
                current_item = await request.ctx.profile.find_item_by_template_id(reward_template_id)
                if reward_template_id in awarded_history:
                    current_quantity = awarded_history[reward_template_id]["quantity"]
                    await request.ctx.profile.change_item_quantity(awarded_history[reward_template_id]["guid"], current_quantity + reward_quantity)
                    awarded_history[reward_template_id]["quantity"] = current_quantity + reward_quantity
                    items.append({"itemType": reward_template_id, "itemGuid": awarded_history[reward_template_id]["guid"], "itemProfile": "profile0", "quantity": reward_quantity})
                elif current_item:
                    current_quantity = (await request.ctx.profile.get_item_by_guid(current_item[0]))["quantity"]
                    await request.ctx.profile.change_item_quantity(current_item[0], current_quantity + reward_quantity)
                    awarded_history[reward_template_id] = {"guid": current_item[0], "quantity": reward_quantity + current_quantity}
                    items.append({"itemType": reward_template_id, "itemGuid": current_item[0], "itemProfile": "profile0", "quantity": reward_quantity})
                else:
                    current_item_id = await request.ctx.profile.add_item(
                        {"templateId": reward_template_id, "attributes": {}, "quantity": reward_quantity})
                    awarded_history[reward_template_id] = {"guid": current_item_id, "quantity": reward_quantity}
                    items.append({"itemType": reward_template_id, "itemGuid": current_item_id, "itemProfile": "profile0", "quantity": reward_quantity})
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
                                                     request.ctx.profile_revisions, True)
    )
