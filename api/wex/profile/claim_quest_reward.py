"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming quest rewards
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_quest_reward = sanic.Blueprint("wex_profile_claim_quest_reward")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimQuestReward.md
@wex_profile_claim_quest_reward.route("/<accountId>/ClaimQuestReward", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def claim_quest_reward(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim quest rewards
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    quest_item = await request.ctx.profile.get_item_by_guid(request.json.get("questMcpId"))
    if quest_item is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid quest item id")
    if not quest_item["attributes"]["bIsCompleted"]:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="You have not completed this quest")
    if quest_item["attributes"]["requirements"]["required"] > quest_item["attributes"]["score"]:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="You have not met the requirements for this quest")
    for reward in quest_item["attributes"]["rewards"]:
        current_reward_id = await request.ctx.profile.find_item_by_template_id(reward["templateId"])
        if not current_reward_id:
            await request.ctx.profile.add_item(reward["templateId"], reward["quantity"])
        else:
            current_reward_item = await request.ctx.profile.get_item_by_guid(current_reward_id[0])
            await request.ctx.profile.change_item_quantity(current_reward_id[0], current_reward_item["quantity"] + reward["quantity"])
    await request.ctx.profile.remove_item(request.json.get("questMcpId"))
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
                                                     request.ctx.profile_revisions)
    )
