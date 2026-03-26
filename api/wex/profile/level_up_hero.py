"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles leveling up heroes.
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_level_up_hero = sanic.Blueprint("wex_profile_level_up_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/LevelUpHero.md
@wex_profile_level_up_hero.route("/<accountId>/LevelUpHero", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.LevelUpHero, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def level_up_hero(request: types.BBProfileRequest, accountId: str,
                        body: MCPValidation.LevelUpHero,
                        query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to level up heroes.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: Validation
    request_body = body.model_dump()
    if request_body.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"))
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    current_hero_level = hero_item["attributes"]["level"]
    new_level = current_hero_level + request_body.get("numLevelUps")
    xp_datatable = (await load_datatable("Content/Balance/Datatables/XPUnitLevels"))[0]["Rows"][
        "UnitXPTNLNormal"]["Keys"]
    for i in range(current_hero_level, new_level):
        try:
            await request.ctx.profile.consume_item("Currency:HeroXp_Basic", int(xp_datatable[i - 1]["Value"]))
        except errors.com.epicgames.modules.gameplayutils.recipe_failed:
            break
        if request_body.get("bIsInPit"):
            await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "level", i + 1,
                                                            ProfileType.MONSTERPIT)
        else:
            await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "level", i + 1)
        await request.ctx.profile.add_notifications({
            "type": "CharacterLevelUp",
            "primary": False,
            "itemId": request_body.get("heroItemId"),
            "level": i + 1
        })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
