"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles deleting friend suggestions / unfriending friends
"""

import sanic
import sanic_ext

from utils import types
from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_delete_friend = sanic.Blueprint("wex_profile_delete_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/AddEpicFriend.md
@wex_profile_delete_friend.route("/<accountId>/DeleteFriend", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.DeleteFriend, query=MCPQueryValidation.MCPFriends)
@compress.compress()
async def delete_friend(request: types.BBProfileRequest, accountId: str,
                        body: MCPValidation.DeleteFriend,
                        query: MCPQueryValidation.MCPFriends) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unfriend or get rid of a suggestion, and is the only friend endpoint called on old versions
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    request_body = body.model_dump()
    if isinstance(request_body.get("friendInstanceIds"), list):
        for friend_id in request_body.get("friendInstanceIds"):
            friend_acc_id = (await request.ctx.profile.get_item_by_guid(friend_id,
                                                                        request.ctx.profile_id)).get("attributes",
                                                                                                     "").get(
                "accountId", "")
            await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
    else:
        friend_acc_id = (await request.ctx.profile.get_item_by_guid(request_body.get("friendInstanceId"),
                                                                    request.ctx.profile_id)).get("attributes",
                                                                                                 "").get(
            "accountId", "")
        await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
