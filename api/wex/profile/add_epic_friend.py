"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles adding epic friend and fetching their wex specific data
"""
import datetime

import sanic

from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_add_epic_friend = sanic.Blueprint("wex_profile_add_epic_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/wex-public-service-live-prod.ol.epicgames.com/wex/api/game/v2/profile/ec0ebb7e56f6454e86c62299a7b32e21/AddEpicFriend.md
@wex_profile_add_epic_friend.route("/<accountId>/AddEpicFriend", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def add_epic_friend(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
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
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = PlayerFriends(accountId)
    if request.json.get("friendAccountId") == "":
        incoming_list = (await request.app.ctx.friends[accountId].get_summary())["incoming"]
        for friend in incoming_list:
            await request.app.ctx.friends[accountId].send_friend_request(request, friend["accountId"])
    else:
        await request.app.ctx.friends[accountId].send_friend_request(request, request.json.get("friendAccountId"))
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
