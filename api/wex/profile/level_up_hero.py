"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles leveling up heroes.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_level_up_hero = sanic.Blueprint("wex_profile_level_up_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/LevelUpHero.md
@wex_profile_level_up_hero.route("/<accountId>/LevelUpHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def level_up_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to level up heroes.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: Validation
    xp_guid = (await request.ctx.profile.find_item_by_template_id("Currency:HeroXp_Basic"))[0]
    current_xp = (await request.ctx.profile.get_item_by_guid(xp_guid))["quantity"]
    if request.json.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    current_hero_level = hero_item["attributes"]["level"]
    new_level = current_hero_level + request.json.get("numLevelUps")
    xp_datatable = (await load_datatable("Content/Balance/Datatables/XPUnitLevels"))[0]["Rows"][
        "UnitXPTNLNormal"]["Keys"]
    for i in range(current_hero_level, new_level):
        if current_xp < int(xp_datatable[i - 1]["Value"]):
            break
        await request.ctx.profile.change_item_quantity(xp_guid, current_xp - int(xp_datatable[i - 1]["Value"]))
        current_xp -= int(xp_datatable[i - 1]["Value"])
        if request.json.get("bIsInPit"):
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "level", i + 1,
                                                            ProfileType.MONSTERPIT)
        else:
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "level", i + 1)
        await request.ctx.profile.add_notifications({
            "type": "CharacterLevelUp",
            "primary": False,
            "itemId": request.json.get("heroItemId"),
            "level": i + 1
        })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
