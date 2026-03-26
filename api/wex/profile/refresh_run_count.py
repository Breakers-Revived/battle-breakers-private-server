"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles refreshing the run count
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_refresh_run_count = sanic.Blueprint("wex_profile_refresh_run_count")


# undocumented
@wex_profile_refresh_run_count.route("/<accountId>/RefreshRunCount", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.RefreshRunCount, query=MCPQueryValidation.MCPLevels)
@compress.compress()
async def refresh_run_count(request: types.BBProfileRequest, accountId: str,
                            body: MCPValidation.RefreshRunCount,
                            query: MCPQueryValidation.MCPLevels) -> sanic.response.JSONResponse:
    """
    This endpoint is used to refresh the run count.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
