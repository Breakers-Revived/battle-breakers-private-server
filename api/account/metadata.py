"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the account metadata endpoints
"""
import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, validate_mongo_key

from utils.sanic_gzip import Compress

compress = Compress()
account_metadata = sanic.Blueprint("account_metadata")


# undocumented
@account_metadata.route("/api/public/account/<accountId>/metadata", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def get_metadata(request: types.BBRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    Get all account metadata
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    account = await request.app.ctx.db["accounts"].find_one({"_id": accountId})
    if not account:
        raise errors.com.epicgames.account.account_not_found()
    return sanic.response.json(account.get("metadata", {}))


# undocumented
@account_metadata.route("/api/public/account/<accountId>/metadata/<key>", methods=["GET", "DELETE"])
@auth(strict=True)
@compress.compress()
async def get_delete_metadata(request: types.BBRequest, accountId: str, key: str) -> sanic.response.HTTPResponse:
    """
    Get/Delete a specific account metadata value
    :param request: The request object
    :param accountId: The account id
    :param key: The metadata key
    :return: The response object
    """
    key = validate_mongo_key(key)
    if request.method == "GET":
        account = await request.app.ctx.db["accounts"].find_one({"_id": accountId}, {"metadata": 1})
        if account and "metadata" in account:
            metadata = account["metadata"]
            try:
                return sanic.response.text(metadata.get(key, ""))
            except KeyError:
                raise errors.com.epicgames.account.metadata_key_not_found()
        else:
            raise errors.com.epicgames.account.metadata_key_not_found()
    else:
        update_result = await request.app.ctx.db["accounts"].update_one(
            {"_id": accountId, f"metadata.{key}": {"$exists": True}},
            {"$unset": {f"metadata.{key}": 1}}
        )
        if update_result.modified_count == 0:
            raise errors.com.epicgames.account.metadata_key_not_found()
        return sanic.response.empty()


# undocumented
@account_metadata.route("/api/public/account/<accountId>/metadata", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def set_metadata(request: types.BBRequest, accountId: str) -> sanic.response.HTTPResponse:
    """
    Set a specific account metadata value
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    account = await request.app.ctx.db["accounts"].find_one({"_id": accountId})
    if not account:
        raise errors.com.epicgames.account.account_not_found()
    if "metadata" not in account:
        account["metadata"] = {}
    if len(account["metadata"]) > 1000:
        raise errors.com.epicgames.account.metadata.too_many_keys()
    raw_key = request.json.get("key")
    raw_value = request.json.get("value")
    if not isinstance(raw_key, str):
        raise errors.com.epicgames.bad_request(errorMessage="Metadata key must be a string")
    key = validate_mongo_key(raw_key)
    if not isinstance(raw_value, (str, int, float, bool, type(None))):
        raise errors.com.epicgames.bad_request(errorMessage="Metadata value must be a valid type")
    key = key[:64]
    if isinstance(raw_value, str):
        raw_value = raw_value[:256]
    account["metadata"][key] = raw_value
    await request.app.ctx.db["accounts"].update_one(
        {"_id": accountId},
        {"$set": {"metadata": account["metadata"]}}
    )
    return sanic.response.empty()
