"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles updating default party
"""
import sanic

from utils import types
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_set_default_party = sanic.Blueprint("wex_profile_set_default_party")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SetDefaultParty.md
@wex_profile_set_default_party.route("/<accountId>/SetDefaultParty", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def set_default_party(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the default hero party slot
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    party_id = request.json.get("partyId")
    party_type = request.json.get("type")
    parties = await request.ctx.profile.get_stat("default_parties", request.ctx.profile_id)
    parties[party_type] = party_id
    parties["LastPvePartyUsed"] = party_id
    await request.ctx.profile.modify_stat("default_parties", parties, request.ctx.profile_id)
    await request.ctx.profile.modify_stat("recent_party_id", party_id, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
