"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming friend gift points
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_gift_points = sanic.Blueprint("wex_profile_claim_gift_points")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimAccountReward.md
@wex_profile_claim_gift_points.route("/<accountId>/ClaimGiftPoints", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.ClaimGiftPoints, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def claim_gift_points(request: types.BBProfileRequest, accountId: str,
                            body: MCPValidation.ClaimGiftPoints,
                            query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim friend gift points
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
