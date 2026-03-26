"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles upgrading hero skills.
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_upgrade_hero_skills = sanic.Blueprint("wex_profile_upgrade_hero_skills")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpgradeHeroSkills.md
@wex_profile_upgrade_hero_skills.route("/<accountId>/UpgradeHeroSkills", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpgradeHeroSkills, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def upgrade_hero_skills(request: types.BBProfileRequest, accountId: str,
                              body: MCPValidation.UpgradeHeroSkills,
                              query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade hero skills
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: validation
    request_body = body.model_dump()
    if request_body.get("bIsInPit"):
        hero_data = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"), ProfileType.MONSTERPIT)
        if not hero_data.get("templateId").startswith("Character:"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
        await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "skill_level",
                                                        hero_data["attributes"]["skill_level"] + 1,
                                                        ProfileType.MONSTERPIT)
        if hero_data["attributes"]["skill_level"] != 0:
            await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "skill_xp", 0,
                                                            ProfileType.MONSTERPIT)
    else:
        hero_data = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"), request.ctx.profile_id)
        if not hero_data.get("templateId").startswith("Character:"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
        await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "skill_level",
                                                        hero_data["attributes"]["skill_level"] + 1)
        if hero_data["attributes"]["skill_level"] != 0:
            await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "skill_xp", 0)
    await request.ctx.profile.consume_item("Currency:SkillXP", request_body.get("xpToSpend"))
    # TODO: investigate skill xp attribute
    # Skill xp seems to be awarded sometimes after completing levels with a hero
    # The skill xp acts as a discount for the next skill level
    await request.ctx.profile.add_notifications({
        "type": "CharacterSkillLevelUp",
        "primary": False,
        "itemId": request_body.get("heroItemId"),
        "level": hero_data["attributes"]["skill_level"] + 1
    }, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
