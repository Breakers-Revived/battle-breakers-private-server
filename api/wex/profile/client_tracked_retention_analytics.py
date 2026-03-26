"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles tracking level milestones
"""

import sanic
import sanic_ext

from utils import types
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_client_tracked_retention_analytics = sanic.Blueprint("wex_profile_client_tracked_retention_analytics")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClientTrackedRetentionAnalytics.md
@wex_profile_client_tracked_retention_analytics.route("/<accountId>/ClientTrackedRetentionAnalytics", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.ClientTrackedRetentionAnalytics, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def client_tracked_retention_analytics(request: types.BBProfileRequest, accountId: str,
                                             body: MCPValidation.ClientTrackedRetentionAnalytics,
                                             query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to track account level milestones (either for the level 20/50 fortnite promotions,
    or analytics)
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    current_level = await request.ctx.profile.get_stat("level", request.ctx.profile_id)
    await request.ctx.profile.modify_stat("last_reported_account_level_milestone", current_level,
                                          request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
