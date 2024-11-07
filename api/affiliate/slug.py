"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the sac code api
"""
import urllib.parse

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_account_id_from_display_name

from utils.sanic_gzip import Compress

compress = Compress()
sac_code = sanic.Blueprint("sac_code")


# undocumented
@sac_code.route("/api/public/affiliates/slug/<sacSlug>", methods=["GET"])
@auth(allow_basic=True)
@compress.compress()
async def sac_code_info(request: types.BBRequest, sacSlug: str) -> sanic.response.JSONResponse:
    """
    Get support a creator code info

    :param request: The request object
    :param sacSlug: The sac slug
    :return: The response object
    """
    search_dn = await get_account_id_from_display_name(request.app.ctx.db, urllib.parse.unquote(sacSlug))
    if search_dn is not None:
        return sanic.response.json({
            "id": search_dn,
            "slug": sacSlug,
            "displayName": sacSlug,
            "status": "ACTIVE",
            "verified": True
        })
    raise errors.com.epicgames.affiliate.slug_not_found(sacSlug)
