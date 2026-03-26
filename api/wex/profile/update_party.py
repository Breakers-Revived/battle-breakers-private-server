"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles party update request
"""
import sanic
import sanic_ext

from utils import types
from utils.utils import authorized as auth, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_update_party = sanic.Blueprint("wex_profile_update_party")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateParty.md
@wex_profile_update_party.route("/<accountId>/UpdateParty", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpdateParty, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def update_party(request: types.BBProfileRequest, accountId: str,
                       body: MCPValidation.UpdateParty,
                       query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the party
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    party_item_id = request_body.get("partyItemId")
    current_party_instance = (await request.ctx.profile.get_item_by_guid(party_item_id, request.ctx.profile_id)).get(
        "attributes"
    )
    new_party_instance = request_body.get("partyInstance")
    for attr, val in new_party_instance.items():
        if val != current_party_instance.get(attr) and new_party_instance.get(attr) is not None:
            await request.ctx.profile.change_item_attribute(party_item_id, attr, new_party_instance.get(attr),
                                                            request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
