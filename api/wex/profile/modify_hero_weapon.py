"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles modifying hero weapons.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_modify_hero_weapon = sanic.Blueprint("wex_profile_modify_hero_weapon")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ModifyHeroWeapon.md
# noinspection IncorrectFormatting
@wex_profile_modify_hero_weapon.route("/<accountId>/ModifyHeroWeapon", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def modify_hero_weapon(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to modify hero weapons.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if request.json.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
        if not hero_item["templateId"].startswith("Character:"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
        if not hero_item["templateId"].startswith("Character:"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    if request.json.get("gearWeaponItemId") != "":
        if not (await request.ctx.profile.get_item_by_guid(request.json.get("gearWeaponItemId")))[
                "templateId"].startswith("Gear:"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid gear weapon item id")
        await request.ctx.profile.change_item_attribute(request.json.get("gearWeaponItemId"), "is_disabled", True)
        await request.ctx.profile.change_item_attribute(request.json.get("gearWeaponItemId"), "hero_item_id",
                                                        request.json.get("heroItemId"))
        if request.json.get("bIsInPit"):
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "gear_weapon_item_id",
                                                            request.json.get("gearWeaponItemId"),
                                                            ProfileType.MONSTERPIT)
        else:
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "gear_weapon_item_id",
                                                            request.json.get("gearWeaponItemId"))
    else:
        if request.json.get("bIsInPit"):
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "gear_weapon_item_id", "",
                                                            ProfileType.MONSTERPIT)
        else:
            await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "gear_weapon_item_id", "")
        if hero_item["attributes"]["gear_weapon_item_id"] != "":
            await request.ctx.profile.change_item_attribute(hero_item["attributes"]["gear_weapon_item_id"],
                                                            "is_disabled", False)
            await request.ctx.profile.change_item_attribute(hero_item["attributes"]["gear_weapon_item_id"],
                                                            "hero_item_id", "")
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
