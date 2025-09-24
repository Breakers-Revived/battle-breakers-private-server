"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the account endpoint
"""
import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_account_data, get_account_data_owner

from utils.sanic_gzip import Compress

compress = Compress()
account_info = sanic.Blueprint("account_info")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Account%20Service/account/api/public/account/accountId.md
@account_info.route("/api/public/account/<accountId>", methods=["GET"])
@auth
@compress.compress()
async def account_route(request: types.BBRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Get account info
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    if request.ctx.is_owner:
        account_data = await get_account_data_owner(request.app.ctx.db, accountId)
        if not account_data:
            raise errors.com.epicgames.account.account_not_found(accountId)
        return sanic.response.json(account_data)
    account_data = await get_account_data(request.app.ctx.db, accountId)
    if not account_data:
        raise errors.com.epicgames.account.account_not_found(accountId)
    return sanic.response.json(account_data)
