"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles profile queries
"""

import sanic

from utils import types
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_query = sanic.Blueprint("wex_profile_query")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/QueryProfile(profile0).md
@wex_profile_query.route("/<accountId>/QueryProfile", methods=["GET", "POST"])
@auth(strict=True)
@compress.compress()
async def query_profile(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Handles the query profile request
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
