"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the external auths endpoint
"""
import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, verify_google_token

from utils.sanic_gzip import Compress

compress = Compress()
external_auths = sanic.Blueprint("account_external_auths")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Account%20Service/account/api/public/account/accountId/externalAuths.md
@external_auths.route("/api/public/account/<accountId>/externalAuths", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def external_auth(request: types.BBRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Get external auths
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    data = await request.app.ctx.db["accounts"].find_one({"_id": accountId}, {"externalAuths": 1, "_id": 0})
    if data and "externalAuths" in data:
        return sanic.response.json([data["externalAuths"]])
    else:
        return sanic.response.json([])


# undocumented
@external_auths.route("/api/public/account/<accountId>/externalAuths", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def add_external_auth(request: types.BBRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Adds an external auth to an account.
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    data = await request.app.ctx.db["accounts"].find_one({"_id": accountId},
                                                         {"externalAuths": 1, "_id": 0, "name": 1, "lastName": 1})
    # not bothered to add ALL of the external auths, only adding google cause mobile (fb blocked insecure sign in)
    match request.json.get("authType"):
        case "google_user_id":
            if request.app.config.LOGIN['ALLOW-GOOGLE-LOGIN'] == "False":
                raise errors.com.epicgames.account.ext_auth.login_not_allowed()
            google_token = await verify_google_token(request.json.get("externalAuthToken"))
            if google_token is None:
                raise errors.com.epicgames.account.external_auth_validate_failed()
            data["externalAuths"]["google"] = {
                "accountId": accountId,
                "type": "google",
                "externalAuthId": google_token.get("sub"),
                "externalAuthIdType": "google_user_id",
                "externalDisplayName": "",
                "authIds": [
                    {
                        "id": google_token.get("sub"),
                        "type": "google_user_id"
                    }
                ]
            }
        case "google_id_token":
            if request.app.config.LOGIN['ALLOW-GOOGLE-LOGIN'] == "False":
                raise errors.com.epicgames.account.ext_auth.login_not_allowed()
            google_token = await verify_google_token(request.json.get("externalAuthToken"))
            if google_token is not None:
                data["externalAuths"]["google"] = {
                    "accountId": accountId,
                    "type": "google",
                    "externalAuthId": google_token.get("sub"),
                    "externalAuthIdType": "google_id_token",
                    "externalDisplayName": google_token.get("name"),
                    "authIds": [
                        {
                            "id": google_token.get("sub"),
                            "type": "google_id_token"
                        }
                    ]
                }
        case _:
            raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
    await request.app.ctx.db["accounts"].update_one({"_id": accountId},
                                                    {"$set": {"externalAuths": data["externalAuths"]}})
    return sanic.response.json([data["externalAuths"]])


# undocumented
@external_auths.route("/api/public/account/<accountId>/externalAuths/<authType>", methods=["GET", "DELETE"])
@auth(strict=True)
@compress.compress()
async def manage_external_auth(request: types.BBRequest, accountId: str,
                               authType: str) -> sanic.response.JSONResponse | sanic.response.HTTPResponse:
    """
    Manage external auths by type
    :param request: The request object
    :param accountId: The account id
    :param authType: The external auth type
    :return: The response object
    """
    match request.method:
        case "GET":
            if authType not in ("google", "facebook", "psn", "xbl", "nintendo"):
                raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
            external_auth_account = await request.app.ctx.db["accounts"].find_one(
                {"_id": accountId}, {"externalAuths.$": 1, "_id": 0})
            if external_auth_account and "externalAuths" in external_auth_account:
                for auth_type, auth_data in external_auth_account["externalAuths"].items():
                    if auth_data.get("type") == authType:
                        return sanic.response.json(auth_data)
                raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
            else:
                raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
        case "DELETE":
            if authType not in ("google", "facebook", "psn", "xbl", "nintendo"):
                raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
            result = await request.app.ctx.db["accounts"].update_one({"_id": accountId},
                                                                     {"$pull": {"externalAuths": {"type": authType}}})
            if result.matched_count == 1 and result.modified_count == 1:
                return sanic.response.empty()
            else:
                raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
        case _:
            raise errors.com.epicgames.common.method_not_allowed()
