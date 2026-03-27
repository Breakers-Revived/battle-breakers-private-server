"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles generating a match with a friend for a profile.
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_generate_match_with_friend = sanic.Blueprint("wex_profile_generate_match_with_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/GenerateMatchWithFriend.md
@wex_profile_generate_match_with_friend.route("/<accountId>/GenerateMatchWithFriend", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.GenerateMatchWithFriend, query=MCPQueryValidation.MCPMultiplayer)
@compress.compress()
async def generate_match_with_friend(request: types.BBProfileRequest, accountId: str,
                                     body: MCPValidation.GenerateMatchWithFriend,
                                     query: MCPQueryValidation.MCPMultiplayer) -> sanic.response.JSONResponse:
    """
    This endpoint is used to spar with a friend.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
