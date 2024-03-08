"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles monster pit buy back
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_character_data, load_datatable, get_template_id_from_path

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_buy_back_from_monster_pit = sanic.Blueprint("wex_profile_buy_back_from_monster_pit")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/BuyBackFromMonsterPit.md
@wex_profile_buy_back_from_monster_pit.route("/<accountId>/BuyBackFromMonsterPit", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def buy_back_from_monster_pit(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to buy back heroes and pets from the monster pit
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    if not request.json.get("characterTemplateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    hero_data = await load_character_data(request.json.get("characterTemplateId"))
    pit_unlocks = await request.ctx.profile.find_item_by_template_id("MonsterPitUnlock:Character",
                                                                     ProfileType.MONSTERPIT)
    sell_rewards = (await load_datatable(
        hero_data[0]["Properties"]["SellRewards"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
        "Properties"]["RequiredItems"]
    for pit_unlock_guid in pit_unlocks:
        pit_unlock = await request.ctx.profile.get_item_by_guid(pit_unlock_guid, ProfileType.MONSTERPIT)
        if pit_unlock["attributes"]["characterId"] == request.json.get("characterTemplateId"):
            await request.ctx.profile.change_item_attribute(pit_unlock_guid, "num_sold",
                                                            pit_unlock["attributes"]["num_sold"] - 1 if
                                                            pit_unlock["attributes"]["num_sold"] > 0 else 0,
                                                            ProfileType.MONSTERPIT)
            break
    else:
        await request.ctx.profile.add_item({
            "templateId": "MonsterPitUnlock:Character",
            "attributes": {
                "num_sold": 0,
                "characterId": request.json.get("characterTemplateId")
            },
            "quantity": 1
        }, ProfileType.MONSTERPIT)
    for sell_reward in sell_rewards:
        reward_template_id = await get_template_id_from_path(
            sell_reward["ItemDefinition"]["ObjectPath"])
        current_item = await request.ctx.profile.find_item_by_template_id(reward_template_id)
        if current_item:
            current_quantity = (await request.ctx.profile.get_item_by_guid(current_item[0]))["quantity"]
            if current_quantity < sell_reward["Count"]:
                raise errors.com.epicgames.world_explorers.bad_request(
                    errorMessage="You cannot afford to buy back this item")
            await request.ctx.profile.change_item_quantity(current_item[0],
                                                           current_quantity - sell_reward["Count"])
        else:
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage="You cannot afford to buy back this item")
    await request.ctx.profile.add_item({
        "templateId": request.json.get("characterTemplateId"),
        "attributes": {
            "gear_weapon_item_id": "",
            "weapon_unlocked": False,
            "sidekick_template_id": "",
            "level": 1,
            "is_new": True,
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
        "quantity": 1
    })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
