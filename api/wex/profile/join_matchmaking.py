"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles joining matchmaking.
"""

import sanic

from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_join_matchmaking = sanic.Blueprint("wex_profile_join_matchmaking")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/JoinMatchmaking.md
@wex_profile_join_matchmaking.route("/<accountId>/JoinMatchmaking", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def join_matchmaking(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to join matchmaking.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: Check eligibility
    raise errors.com.epicgames.world_explorers.bad_request()
