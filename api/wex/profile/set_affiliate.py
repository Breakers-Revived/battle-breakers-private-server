"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles setting a sac code
"""

import sanic

import utils.utils
from utils import types
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_set_sac = sanic.Blueprint("wex_profile_set_sac")


# undocumented
@wex_profile_set_sac.route("/<accountId>/SetAffiliate", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def set_sac(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to set a sac code.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    await request.ctx.profile.modify_stat("affiliate_id", request.json.get("affiliateId"))
    await request.ctx.profile.modify_stat("affiliate_set_time", await utils.utils.format_time())
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
