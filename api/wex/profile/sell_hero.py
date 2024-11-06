"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles selling heroes.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, get_template_id_from_path, load_datatable, load_character_data

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_sell_hero = sanic.Blueprint("wex_profile_sell_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SellHero.md
@wex_profile_sell_hero.route("/<accountId>/SellHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def sell_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to sell heroes
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    if request.json.get("bIsInPit"):
        # hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="How did you do this?")
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if hero_item is None:
        raise errors.com.epicgames.world_explorers.not_found(
            errorMessage="We're sorry, but we were unable to sell your item as it was not found in your inventory.")
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    hero_data = await load_character_data(hero_item["templateId"])
    sell_rewards = (await load_datatable(
        hero_data[0]["Properties"]["SellRewards"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
        "Properties"]["RequiredItems"]
    foil_sell_rewards = (await load_datatable(
        hero_data[0]["Properties"]["FoilSellRewards"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
        "Properties"]["RequiredItems"]
    pit_unlocks = await request.ctx.profile.find_item_by_template_id("MonsterPitUnlock:Character",
                                                                     ProfileType.MONSTERPIT)
    # TODO: make this work with evolution alterations
    pit_copy_guid = await request.ctx.profile.find_item_by_template_id(hero_item["templateId"], ProfileType.MONSTERPIT)
    if pit_copy_guid:
        pit_copy = await request.ctx.profile.get_item_by_guid(pit_copy_guid[0], ProfileType.MONSTERPIT)
        if pit_copy["attributes"]["foil_lvl"] < 0 < hero_item["attributes"]["foil_lvl"]:
            await request.ctx.profile.change_item_attribute(pit_copy_guid[0], "foil_lvl",
                                                            hero_item["attributes"]["foil_lvl"], ProfileType.MONSTERPIT)
        elif pit_copy["attributes"]["foil_lvl"] > 0 and hero_item["attributes"]["foil_lvl"] > 0:
            for foil_reward in foil_sell_rewards:
                reward_template_id = await get_template_id_from_path(
                    foil_reward["ItemDefinition"]["ObjectPath"])
                current_item = await request.ctx.profile.find_item_by_template_id(reward_template_id)
                if current_item:
                    current_quantity = (await request.ctx.profile.get_item_by_guid(current_item[0]))["quantity"]
                    await request.ctx.profile.change_item_quantity(current_item[0],
                                                                   current_quantity + foil_reward["Count"])
                else:
                    await request.ctx.profile.add_item({
                        "templateId": reward_template_id,
                        "attributes": {},
                        "quantity": foil_reward["Count"]
                    })
    for pit_unlock_guid in pit_unlocks:
        pit_unlock = await request.ctx.profile.get_item_by_guid(pit_unlock_guid, ProfileType.MONSTERPIT)
        if pit_unlock["attributes"]["characterId"] == hero_item["templateId"]:
            await request.ctx.profile.change_item_attribute(pit_unlock_guid, "num_sold",
                                                            pit_unlock["attributes"]["num_sold"] + 1,
                                                            ProfileType.MONSTERPIT)
            break
    else:
        await request.ctx.profile.add_item({
            "templateId": "MonsterPitUnlock:Character",
            "attributes": {
                "num_sold": 1,
                "characterId": hero_item["templateId"]
            },
            "quantity": 1
        }, ProfileType.MONSTERPIT)
    for sell_reward in sell_rewards:
        reward_template_id = await get_template_id_from_path(
            sell_reward["ItemDefinition"]["ObjectPath"])
        current_item = await request.ctx.profile.find_item_by_template_id(reward_template_id)
        if current_item:
            current_quantity = (await request.ctx.profile.get_item_by_guid(current_item[0]))["quantity"]
            await request.ctx.profile.change_item_quantity(current_item[0],
                                                           current_quantity + sell_reward["Count"])
        else:
            await request.ctx.profile.add_item({
                "templateId": reward_template_id,
                "attributes": {},
                "quantity": sell_reward["Count"]
            })
    await request.ctx.profile.remove_item(request.json.get("heroItemId"))
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
