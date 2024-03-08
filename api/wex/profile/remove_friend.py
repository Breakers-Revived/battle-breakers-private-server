"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles removing friends (presumably the same as deletefriend)
"""
import sanic

from utils import types
from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_remove_friend = sanic.Blueprint("wex_profile_remove_friend")


# undocumented
@wex_profile_remove_friend.route("/<accountId>/RemoveFriend", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def remove_friend(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unfriend a friend.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    if isinstance(request.json.get("friendInstanceIds"), list):
        for friend_id in request.json.get("friendInstanceIds"):
            friend_acc_id = (await request.ctx.profile.get_item_by_guid(friend_id,
                                                                        request.ctx.profile_id)).get("attributes",
                                                                                                     "").get(
                "accountId", "")
            await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
    else:
        friend_acc_id = (await request.ctx.profile.get_item_by_guid(request.json.get("friendInstanceId"),
                                                                    request.ctx.profile_id)).get("attributes",
                                                                                                 "").get(
            "accountId", "")
        await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
