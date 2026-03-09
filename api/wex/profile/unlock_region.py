"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles unlocking map regions
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, extract_version_info

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_unlock_region = sanic.Blueprint("wex_profile_unlock_region")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UnlockRegion.md
@wex_profile_unlock_region.route("/<accountId>/UnlockRegion", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def unlock_region(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unlock a map region
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    unlocked_regions = await request.ctx.profile.find_item_by_template_id("WorldUnlock:Region", ProfileType.LEVELS)
    for region_guid in unlocked_regions:
        region = await request.ctx.profile.get_item_by_guid(region_guid, ProfileType.LEVELS)
        if region is not None and region["attributes"]["regionId"] == request.json.get("regionId"):
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage=f"Region {request.json.get('regionId')} is already unlocked.")
    await request.ctx.profile.add_item({
        "templateId": "WorldUnlock:Region",
        "attributes": {
            "regionId": request.json.get("regionId")
        },
        "quantity": 1
    }, profile_id=request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
