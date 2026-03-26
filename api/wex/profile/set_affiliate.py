"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles setting a sac code
"""

import sanic
import sanic_ext

from utils import types
from utils.utils import authorized as auth, format_time, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_set_sac = sanic.Blueprint("wex_profile_set_sac")


# undocumented
@wex_profile_set_sac.route("/<accountId>/SetAffiliate", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.SetAffiliate, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def set_sac(request: types.BBProfileRequest, accountId: str,
                  body: MCPValidation.SetAffiliate,
                  query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to set a sac code.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    await request.ctx.profile.modify_stat("affiliate_id", body.model_dump().get("affiliateId"))
    await request.ctx.profile.modify_stat("affiliate_set_time", await format_time())
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
