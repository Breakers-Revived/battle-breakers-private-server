"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles adding epic friend and fetching their wex specific data
"""

import sanic
import sanic_ext

from utils import types
from utils.friend_system import PlayerFriends
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

compress = Compress()
wex_profile_add_epic_friend = sanic.Blueprint("wex_profile_add_epic_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/AddEpicFriend.md
@wex_profile_add_epic_friend.route("/<accountId>/AddEpicFriend", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.AddEpicFriend, query=MCPQueryValidation.MCPFriends)
@compress.compress()
async def add_epic_friend(request: types.BBProfileRequest, accountId: str,
                          body: MCPValidation.AddEpicFriend,
                          query: MCPQueryValidation.MCPFriends) -> sanic.response.JSONResponse:
    """
    This endpoint is used to fetch a new friend's wex data

    When the friend type is incoming, 1.80+ clients call this endpoint with an empty friendAccountId.
    On 1.80+, the friend instance shouldnt exist in the profile at all, instead, on start the game checks your
    incoming friends via friend service, and adds placeholder friend entries in the social tab.
    This will call the endpoint correctly, but will only update on launch (rather than upon next mcp request),
    and will not appear in legacy clients; for this reason, we will instead use the legacy system.
    Currently, this has the drawback of not being able to choose which friend requests to accept.

    TODO: Modify profile depending on game version (low priority, current workaround is fine)
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    friendAccountId = body.model_dump().get("friendAccountId")
    if friendAccountId == "":
        incoming_list = (await request.app.ctx.friends[accountId].get_summary())["incoming"]
        for friend in incoming_list:
            await request.app.ctx.friends[accountId].send_friend_request(request, friend["accountId"])
    else:
        await request.app.ctx.friends[accountId].send_friend_request(request, friendAccountId)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
