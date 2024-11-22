"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles friends reconciliation.
"""
import sanic

from utils import types
from utils.friend_system import PlayerFriends
from utils.enums import ProfileType
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_reconcile = sanic.Blueprint("wex_profile_reconcile")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/Reconcile.md
@wex_profile_reconcile.route("/<accountId>/Reconcile", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def reconcile(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to determine whether epic friends have battle breakers or not.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    await request.ctx.profile.clear_notifications()
    results = {}
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    friends_list = request.json["friendIdList"]
    friends_list.extend(request.json["outgoingIdList"])
    friends_list.extend(request.json["incomingIdList"])
    async for account in request.app.ctx.db["accounts"].find({"_id": {"$in": friends_list}}, {"_id": 1}):
        results[account["_id"]] = True
    for account in results:
        if account not in results:
            results[account] = False
    await request.ctx.profile.add_notifications({
        "type": "WExpReconcileNotification",
        "primary": True,
        "results": results
    }, ProfileType.FRIENDS)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
