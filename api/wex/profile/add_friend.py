"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles adding friends and fetching their wex specific data
"""
import sanic

from utils import types
from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_add_friend = sanic.Blueprint("wex_profile_add_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/AddEpicFriend.md
@wex_profile_add_friend.route("/<accountId>/AddFriend", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def add_friend(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to fetch a new friend's wex data; it's called by 1.0-1.71, for the old wex friend system
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    await request.app.ctx.friends[accountId].send_friend_request(request, request.json.get("friendAccountId"))
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
