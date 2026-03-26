"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles adding an external account
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_client_ext_acc = sanic.Blueprint("wex_profile_client_ext_acc")


# undocumented
@wex_profile_client_ext_acc.route("/<accountId>/ClientAddedExternalAccount", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.ClientAddedExternalAccount, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def client_added_external_account(request: types.BBProfileRequest, accountId: str,
                                        body: MCPValidation.ClientAddedExternalAccount,
                                        query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to add an external account.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    raise errors.com.epicgames.not_implemented()
