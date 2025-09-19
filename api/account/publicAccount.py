"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the public facing account info endpoint
"""
import urllib.parse

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_account_id_from_email, get_account_id_from_display_name, \
    get_account_data, get_account_data_owner

from utils.sanic_gzip import Compress

compress = Compress()
public_account = sanic.Blueprint("account_public")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Account%20Service/account/api/public/account.md
@public_account.route("/api/public/account", methods=["GET"])
@auth
@compress.compress()
async def public_account_info(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Bulk get account info
    :param request: The request object
    :return: The response object
    """
    account_ids = request.args.getlist("accountId")
    if len(account_ids) > 100:
        raise errors.com.epicgames.account.invalid_account_id_count(100)
    account_cursor = request.app.ctx.db["accounts"].find(
        {"_id": {"$in": account_ids}},
        {
            "displayName": 1,
            "externalAuths": 1
        }
    )
    final_accounts = await account_cursor.to_list(length=len(account_ids))
    for account in final_accounts:
        account["id"] = account.pop("_id")
    return sanic.response.json(final_accounts)


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Account%20Service/account/api/public/account/displayName/displayName.md
@public_account.route("/api/public/account/displayName/<displayName>", methods=["GET"])
@auth
@compress.compress()
async def account_displayname(request: types.BBRequest, displayName: str) -> sanic.response.JSONResponse:
    """
    Get an account by name
    :param request: The request object
    :param displayName: The display name
    :return: The response object
    """
    displayName = urllib.parse.unquote(displayName)
    requested_id = await get_account_id_from_display_name(request.app.ctx.db, displayName)
    if requested_id is None:
        raise errors.com.epicgames.account.account_not_found(displayName)
    if requested_id == request.ctx.owner:
        account_data = await get_account_data_owner(request.app.ctx.db, requested_id)
        if not account_data:
            raise errors.com.epicgames.account.account_not_found(displayName)
        return sanic.response.json(account_data)
    account_data = await get_account_data(request.app.ctx.db, requested_id)
    if not account_data:
        raise errors.com.epicgames.account.account_not_found(displayName)
    return sanic.response.json(account_data)


@public_account.route("/api/public/account/email/<email>", methods=["GET"])
@auth
@compress.compress()
async def account_email(request: types.BBRequest, email: str) -> sanic.response.JSONResponse:
    """
    Get account by email (deprecated on official API)
    :param request: The request object
    :param email: The email
    :return: The response object
    """
    requested_id = await get_account_id_from_email(request.app.ctx.db, email)
    if requested_id is None:
        raise errors.com.epicgames.account.account_not_found(email)
    if requested_id == request.ctx.owner:
        account_data = await get_account_data_owner(request.app.ctx.db, requested_id)
        if not account_data:
            raise errors.com.epicgames.account.account_not_found(email)
        return sanic.response.json(account_data)
    account_data = await get_account_data(request.app.ctx.db, requested_id)
    if not account_data:
        raise errors.com.epicgames.account.account_not_found(email)
    return sanic.response.json(account_data)


# undocumented
@public_account.route("/api/public/account/lookup/externalId", methods=["POST"])
@auth()
@compress.compress()
async def external_id_lookup(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Look up accounts by external id
    same response structure as above
    :param request: The request object
    :return: The response object
    """
    raise errors.com.epicgames.not_implemented()


# undocumented
@public_account.route("/api/public/account/lookup/externalAuth/<externalAuthType>/displayName/<displayName>",
                      methods=["GET"])
@auth()
@compress.compress()
async def external_id_lookup_by_name(request: types.BBRequest, externalAuthType: str,
                                     displayName: str) -> sanic.response.JSONResponse:
    """
    Look up accounts by external id
    same response structure as above
    :param request: The request object
    :param externalAuthType: The external auth type
    :param displayName: The display name
    :return: The response object
    """
    raise errors.com.epicgames.not_implemented()
