"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles entitlement check
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, uuid_generator, format_time

wex_entitlement = sanic.Blueprint("wex_entitlement")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/entitlementCheck.md
@wex_entitlement.route("/api/entitlementCheck", methods=["GET"])
@auth
async def entitlement_check(request: types.BBRequest) -> sanic.response.HTTPResponse:
    """
    This endpoint is used to check if the user has access to the game, and if not, grant them (probably).
    :param request: The request object
    :return: The response object (204)
    """
    if await request.app.ctx.db["entitlements"].count_documents({"_id": request.ctx.owner, "entitlements": {
        "$elemMatch": {"catalogItemId": "e458e71024404176addca212860f9ef2"}}}) == 0:
        raise errors.com.epicgames.common.missing_action("PLAY", "{1}")
    return sanic.response.empty()


@wex_entitlement.route("/api/storeaccess/v1/request_access/<accountId>", methods=["POST"])
@auth(strict=True)
async def request_access(request: types.BBRequest, accountId: str) -> sanic.response.HTTPResponse:
    """
    This endpoint is used to request free access to the game.
    :param request: The request object
    :param accountId: The account id
    :return: The response object (204)
    """
    if await request.app.ctx.db["entitlements"].count_documents({"_id": request.ctx.owner, "entitlements": {
            "$elemMatch": {"catalogItemId": "e458e71024404176addca212860f9ef2"}}}):
        raise errors.com.epicgames.bad_request(errorMessage="Already have access to this game.")
    await request.app.ctx.db["entitlements"].update_one(
        {"_id": accountId, "entitlements": {"$exists": False}},
        {"$set": {"entitlements": []}}
    )
    await request.app.ctx.db["entitlements"].update_one({"_id": accountId}, {
        "$push": {
            "entitlements": {
                "id": await uuid_generator(),
                "entitlementName": "WorldExplorers_Free",
                "namespace": "wex",
                "catalogItemId": "e458e71024404176addca212860f9ef2",
                "accountId": accountId,
                "identityId": accountId,
                "entitlementType": "AUDIENCE",
                "grantDate": await format_time(),
                "consumed": False,
                "status": "ACTIVE",
                "active": True,
                "useCount": 0,
                "originalUseCount": 0,
                "platformType": "EPIC",
                "created": "2019-11-08T10:47:00.476Z",
                "updated": "2019-11-08T10:47:00.476Z",
                "groupEntitlement": False,
                "country": None
            }
        }
    })
    return sanic.response.empty()
    # TODO Check for bans
    # raise errors.com.epicgames.world_explorers.banned_access_found_when_granting()
    # raise errors.com.epicgames.bad_request(
    #     errorMessage = "Client requested access grant but has banned access entitlement.",
    #     numericErrorCode = 1001
    # )


@wex_entitlement.route("/api/storeaccess/v1/redeem_access/<accountId>", methods=["POST"])
@auth(strict=True)
async def redeem_access(request: types.BBRequest, accountId: str) -> sanic.response.HTTPResponse:
    """
    This endpoint is used to redeem access to the game.
    :param request: The request object
    :param accountId: The account id
    :return: The response object (204)
    """
    entitlements = await request.app.ctx.db["entitlements"].find_one({"_id": accountId})
    for entitlement in entitlements["entitlements"]:
        if entitlement.get("catalogItemId") == "e458e71024404176addca212860f9ef2":
            raise errors.com.epicgames.bad_request(errorMessage="Already have access to this game.")
    entitlements["entitlements"].append({
        "id": await uuid_generator(),
        "entitlementName": "WorldExplorers_Free",
        "namespace": "wex",
        "catalogItemId": "e458e71024404176addca212860f9ef2",
        "accountId": accountId,
        "identityId": accountId,
        "entitlementType": "AUDIENCE",
        "grantDate": await format_time(),
        "consumed": False,
        "status": "ACTIVE",
        "active": True,
        "useCount": 0,
        "originalUseCount": 0,
        "platformType": "EPIC",
        "created": "2019-11-08T10:47:00.476Z",
        "updated": "2019-11-08T10:47:00.476Z",
        "groupEntitlement": False,
        "country": None
    })
    await request.app.ctx.db["entitlements"].update_one({"_id": accountId}, {"$set": entitlements})
    return sanic.response.empty()
    # TODO Check for bans
    # raise errors.com.epicgames.world_explorers.banned_access_found_when_granting()


@wex_entitlement.route("/api/accesscontrol/status", methods=["GET"])
@auth
async def real_game_access(request: types.BBRequest, accountId: str) -> sanic.response.HTTPResponse:
    """
    This endpoint is used for something, who knows
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    # TODO: Check for bans
    if await request.app.ctx.db["entitlements"].count_documents({"_id": request.ctx.owner, "entitlements": {
            "$elemMatch": {"catalogItemId": "e458e71024404176addca212860f9ef2"}}}) == 0:
        return sanic.response.json({
            "play": False,
            "isBanned": False,
        })
    return sanic.response.json({
        "play": True,
        "isBanned": False,
    })
