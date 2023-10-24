"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles adding an external account
"""

import sanic

from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_client_ext_acc = sanic.Blueprint("wex_profile_client_ext_acc")


# undocumented
@wex_profile_client_ext_acc.route("/<accountId>/ClientAddedExternalAccount", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def client_added_external_account(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to add an external account.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()