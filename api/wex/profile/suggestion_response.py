"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles suggestion responses.
"""
import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_suggestion_response = sanic.Blueprint("wex_profile_suggestion_response")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SuggestionResponse.md
@wex_profile_suggestion_response.route("/<accountId>/SuggestionResponse", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.SuggestionResponse, query=MCPQueryValidation.MCPFriends)
@compress.compress()
async def suggestion_response(request: types.BBProfileRequest, accountId: str,
                              body: MCPValidation.SuggestionResponse,
                              query: MCPQueryValidation.MCPFriends) -> sanic.response.JSONResponse:
    """
    This endpoint is used to respond to friend suggestions
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    for friend_id in request_body.get("invitedFriendInstanceIds"):
        friend_instance = await request.ctx.profile.get_item_by_guid(friend_id, request.ctx.profile_id)
        if friend_instance["attributes"].get("status") == "SuggestedLegacy" and await request.app.ctx.db[
            "accounts"].find_one({"_id": friend_instance["attributes"].get("accountId")}, {"_id": 1}) is None:
            raise errors.com.epicgames.world_explorers.not_found(
                errorMessage="Unfortunately, this friend has not imported their saved account to the private server. "
                             "Mew should ask them to do so :)")
        else:
            if accountId not in request.app.ctx.friends:
                request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
            await request.app.ctx.friends[accountId].send_friend_request(request, request_body.get("friendAccountId"))
    for friend_id in request_body.get("rejectedFriendInstanceIds"):
        # TODO: add ignored suggestion list
        await request.ctx.profile.remove_item(friend_id, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
