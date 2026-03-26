"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles requesting the preregistration reward
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_request_prereg = sanic.Blueprint("wex_profile_request_prereg")


# undocumented
@wex_profile_request_prereg.route("/<accountId>/RequestPreregistrationReward", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.RequestPreregistrationReward, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def request_preregistration(request: types.BBProfileRequest, accountId: str,
                                  body: MCPValidation.RequestPreregistrationReward,
                                  query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim the preregistration reward.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Sorry, the promotion period has ended.")
