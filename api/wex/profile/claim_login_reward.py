"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles profile claim daily reward
"""
import datetime

import sanic

from utils import types
from utils.exceptions import errors
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, load_datatable, get_template_id_from_path, extract_version_info, format_time

compress = Compress()
wex_profile_claim_login = sanic.Blueprint("wex_profile_claim_login")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/QueryProfile(profile0).md
@wex_profile_claim_login.route("/<accountId>/ClaimLoginReward", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def claim_login_reward(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Handles the daily reward request
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    current_day = (await request.ctx.profile.get_stat("login_reward"))["next_level"]
    if datetime.datetime.strptime((await request.ctx.profile.get_stat("login_reward")).get("last_claim_time"),
                                  "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.UTC) > datetime.datetime.now(
            datetime.UTC).replace(hour=0, minute=0, second=0, microsecond=0):
        raise errors.com.epicgames.world_explorers.login_reward_not_available(current_day,
                                                                              await format_time(
                                                                                  datetime.datetime.now(
                                                                                      datetime.UTC).replace(hour=0,
                                                                                                            minute=0,
                                                                                                            second=0,
                                                                                                            microsecond=0)))
    if current_day >= 1800:
        await request.ctx.profile.modify_stat("login_reward", {
            # Effectively disable future login rewards as beyond this, the game crashes
            "last_claim_time": "9999-12-31T23:59:59.999Z",
            "next_level": 1800
        })
    else:
        # ugly but it works
        version_info = (await extract_version_info(request.headers.get("User-Agent")))[0]
        if version_info <= 1:
            datatable = "Content/Loot/DataTables/LoginRewards 1.0"
        elif version_info in [2, 3, 4, 5, 6, 7, 71]:
            if version_info == 6:
                version_info = 7
            datatable = f"Content/Loot/DataTables/LoginRewards 1.{version_info}"
        elif 80 <= version_info <= 81:
            datatable = "Content/Loot/DataTables/LoginRewards 1.80"
        elif 82 <= version_info <= 84:
            datatable = "Content/Loot/DataTables/LoginRewards 1.82"
        elif version_info == 85:
            datatable = "Content/Loot/DataTables/LoginRewards 1.85"
        else:
            datatable = "Content/Loot/DataTables/LoginRewards 1.86"
        login_reward = (await load_datatable(datatable))[0]["Rows"][str(current_day)]
        reward_path = login_reward['ItemDefinition']
        reward_quantity = login_reward['ItemCount']
        try:
            reward_path = reward_path["AssetPathName"]
        except:
            pass  # Backwards compat for datatables in the UE4.16 format
        reward_template_id = await get_template_id_from_path(reward_path)
        if reward_template_id.split(':')[0] == "Character":
            await request.ctx.profile.add_item({"templateId": reward_template_id,
                                                "attributes": {"gear_weapon_item_id": "", "weapon_unlocked": False,
                                                               "sidekick_template_id": "", "is_new": True, "level": 1,
                                                               "num_sold": 0, "skill_level": 1,
                                                               "sidekick_unlocked": False,
                                                               "upgrades": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                               "used_as_sidekick": False, "gear_armor_item_id": "",
                                                               "skill_xp": 0, "armor_unlocked": False, "foil_lvl": -1,
                                                               "xp": 0, "rank": 0, "sidekick_item_id": ""},
                                                "quantity": 1})
        else:
            current_item = await request.ctx.profile.find_item_by_template_id(reward_template_id)
            if current_item:
                current_quantity = (await request.ctx.profile.get_item_by_guid(current_item[0]))["quantity"]
                await request.ctx.profile.change_item_quantity(current_item[0], current_quantity + reward_quantity)
            else:
                await request.ctx.profile.add_item(
                    {"templateId": reward_template_id, "attributes": {}, "quantity": reward_quantity})
        await request.ctx.profile.modify_stat("login_reward", {
            "last_claim_time": await format_time(),
            "next_level": current_day + 1
        })
    await request.ctx.profile.modify_stat("hammer_quest_energy", {
        "energy_spent": 0,
        "energy_required": 100,
        "claim_count": 0
    })
    # TODO: Add gift chest activity
    giftboxes = await request.ctx.profile.find_items_by_type("Giftbox")
    for giftbox in giftboxes:
        sealed_days = (await request.ctx.profile.get_item_by_guid(giftbox))["attributes"]["sealed_days"]
        await request.ctx.profile.change_item_attribute(giftbox, "sealed_days", max(0, sealed_days - 1))
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
