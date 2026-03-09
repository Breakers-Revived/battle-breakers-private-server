"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming the notification opt-in reward
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_notification_opt_in_reward = sanic.Blueprint("wex_profile_claim_notification_opt_in_reward")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimNotificationOptInReward.md
@wex_profile_claim_notification_opt_in_reward.route("/<accountId>/ClaimNotificationOptInReward", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def claim_notification_opt_in_reward(request: types.BBProfileRequest,
                                           accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim the notification opt-in reward
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if await request.ctx.profile.get_stat("notification_optin_reward_claimed"):
        raise errors.com.epicgames.world_explorers.service_not_required(errorMessage="Already claimed reward")
    await request.ctx.profile.add_item({
        "templateId": "Giftbox:GB_NotificationOptInReward",
        "attributes": {
            "sealed_days": 0,
            "params": {},
            "min_level": 1
        },
        "quantity": 1
    })
    await request.ctx.profile.modify_stat("notification_optin_reward_claimed", True)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
