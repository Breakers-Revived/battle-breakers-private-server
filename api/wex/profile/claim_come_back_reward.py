"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming the come back reward
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_comeback = sanic.Blueprint("wex_profile_claim_comeback")


# undocumented
@wex_profile_claim_comeback.route("/<accountId>/ClaimComeBackReward", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def claim_comeback(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim the comeback reward.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Sorry, the promotion period has ended.")
