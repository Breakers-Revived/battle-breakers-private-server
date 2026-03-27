"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles generating matches
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_generate_matches = sanic.Blueprint("wex_profile_generate_matches")


# undocumented
@wex_profile_generate_matches.route("/<accountId>/GenerateMatches", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.GenerateMatches, query=MCPQueryValidation.MCPMultiplayer)
@compress.compress()
async def generate_matches(request: types.BBProfileRequest, accountId: str,
                           body: MCPValidation.GenerateMatches,
                           query: MCPQueryValidation.MCPMultiplayer) -> sanic.response.JSONResponse:
    """
    This endpoint is used to generate matches.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
