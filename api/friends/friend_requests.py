"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Should handle sending friend requests

I am hella not bothered to make a whole other class for just friends, so json it is
nvm
"""

import sanic

from utils import types
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
friend_request = sanic.Blueprint("friend_request")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Friends%20Service/friends/api/v1/accountId/friends/friendId.md
@friend_request.route("/api/v1/<accountId>/friends/<friendId>", methods=["POST", "DELETE"])
@auth(strict=True)
@compress.compress()
async def send_friend_request(request: types.BBFriendRequest, accountId: str,
                              friendId: str) -> sanic.response.HTTPResponse:
    """
    Sends a friend request to the specified account id
    :param request: The request object
    :param accountId: The account id
    :param friendId: The friend id
    :return: The response object
    """
    if request.method == "DELETE":
        delete_request = await request.ctx.friends.remove_friend(request, friendId)
        if delete_request is not None:
            raise sanic.exceptions.BadRequest(context=delete_request)
        return sanic.response.empty()
    sent_request = await request.ctx.friends.send_friend_request(request, friendId)
    # TODO: add info to wex friend profile
    if sent_request is not None:
        raise sanic.exceptions.BadRequest(context=sent_request)
    return sanic.response.empty()


@friend_request.route("/api/public/friends/<accountId>/<friendId>", methods=["POST", "DELETE"])
@auth(strict=True)
@compress.compress()
async def send_friend_request_deprecated(request: types.BBFriendRequest, accountId: str,
                                         friendId: str) -> sanic.response.HTTPResponse:
    """
    Identical to above, but serves as backwards compatability for old clients
    :param request: The request object
    :param accountId: The account id
    :param friendId: The friend id
    :return: The response object
    """
    if request.method == "DELETE":
        delete_request = await request.ctx.friends.remove_friend(request, friendId)
        if delete_request is not None and delete_request.get("errorCode") is not None:
            raise sanic.exceptions.BadRequest(context=delete_request)
        return sanic.response.empty()
    sent_request = await request.ctx.friends.send_friend_request(request, friendId)
    if sent_request is not None and sent_request.get("errorCode") is not None:
        raise sanic.exceptions.BadRequest(context=sent_request)
    return sanic.response.empty()


@friend_request.route("/api/v1/<accountId>/incoming/accept", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def accept_bulk_requests(request: types.BBFriendRequest, accountId: str) -> sanic.response.HTTPResponse:
    """
    Accepts all specified incoming friend requests
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    for friendId in request.args.getlist("targetIds"):
        await request.ctx.friends.send_friend_request(request, friendId)
    return sanic.response.empty()
