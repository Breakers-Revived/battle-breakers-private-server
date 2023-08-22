"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the entitlement checks for the launcher
"""

import sanic

from utils.utils import authorized as auth, read_file

from utils.sanic_gzip import Compress

compress = Compress()
entitlement = sanic.Blueprint("entitlement")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Entitlement%20Service/entitlement/api/account/accountId/entitlements.md
@entitlement.route("/api/account/<accountId>/entitlements", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def entitlements_route(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    Handles the entitlement check
    :param request: The request object
    :param accountId: The account id
    :return: The response object (204)
    """
    return sanic.response.json(await read_file(f"res/entitlement/api/account/{accountId}.json"))
