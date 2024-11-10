"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles party update request
"""
import sanic

from utils import types
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_update_party = sanic.Blueprint("wex_profile_update_party")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateParty.md
@wex_profile_update_party.route("/<accountId>/UpdateParty", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def update_party(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the party
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    party_item_id = request.json.get("partyItemId")
    current_party_instance = (await request.ctx.profile.get_item_by_guid(party_item_id, request.ctx.profile_id)).get(
        "attributes"
    )
    new_party_instance = request.json.get("partyInstance")
    for attr, val in current_party_instance.items():
        if val != new_party_instance.get(attr) and new_party_instance.get(attr) is not None:
            await request.ctx.profile.change_item_attribute(party_item_id, attr, new_party_instance.get(attr),
                                                            request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
