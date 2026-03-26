"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming quest rewards
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_quest_reward = sanic.Blueprint("wex_profile_claim_quest_reward")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimQuestReward.md
@wex_profile_claim_quest_reward.route("/<accountId>/ClaimQuestReward", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.ClaimQuestReward, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def claim_quest_reward(request: types.BBProfileRequest, accountId: str,
                             body: MCPValidation.ClaimQuestReward,
                             query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim quest rewards
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: validation
    quest_id = body.model_dump().get("questMcpId")
    quest_item = await request.ctx.profile.get_item_by_guid(quest_id)
    if quest_item is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid quest item id")
    if not quest_item["attributes"]["bIsCompleted"]:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="You have not completed this quest")
    if quest_item["attributes"]["requirements"]["required"] > quest_item["attributes"]["score"]:
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage="You have not met the requirements for this quest")
    for reward in quest_item["attributes"]["rewards"]:
        if reward["templateId"].startswith("Character:"):
            await request.ctx.profile.grant_hero(reward["templateId"], quantity=reward["quantity"])
        else:
            await request.ctx.profile.grant_item(reward["templateId"], reward["quantity"])
    await request.ctx.profile.remove_item(quest_id)
    await request.ctx.profile.add_notifications({
        "type": "WExpGiftPointReward",
        "primary": True,
        "totalPoints": 0,
        "lootResult": {
            "items": quest_item["attributes"]["rewards"]
        }
    }, request.ctx.profile_id)
    # TODO: modify activity chest
    # TODO: account leveling up & rewards
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
