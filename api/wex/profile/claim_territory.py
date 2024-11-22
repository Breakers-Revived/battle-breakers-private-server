"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles claiming territory
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_claim_territory = sanic.Blueprint("wex_profile_claim_territory")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/ClaimTerritory.md
@wex_profile_claim_territory.route("/<accountId>/ClaimTerritory", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def claim_territory(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to claim a territory when completing all 1/2/3/4 star missions in a zone
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    unlocked_territories = await request.ctx.profile.find_item_by_template_id("WorldUnlock:Territory",
                                                                              ProfileType.LEVELS)
    for territory in unlocked_territories:
        if territory["attributes"]["territoryId"] == request.json.get("territoryId"):
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage=f"Territory {request.json.get('zoneId')} is already unlocked.")
    await request.ctx.profile.add_item({
        "templateId": "WorldUnlock:Territory",
        "attributes": {
            "territoryId": request.json.get("territoryId")
        },
        "quantity": 1
    }, profile_id=ProfileType.LEVELS)
    await request.ctx.profile.modify_stat("num_territories_claimed",
                                          (await request.ctx.profile.get_stat("num_territories_claimed")) + 1)
    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
    await request.ctx.profile.add_notifications({
        "type": "WExpTerritoryClaim",
        "primary": True,
        "territoryId": request.json.get("territoryId"),
        "lootResult": {
            "tierGroupName": "LTG.FC.Territory.Claim",  # claiming territories always has the same loot tier group
            "items": [
                {
                    "itemType": "Currency:MtxGiveaway",
                    "itemGuid": mtx_item_id,
                    "itemProfile": "profile0",
                    "quantity": 100
                }
            ]
        }
    }, ProfileType.LEVELS)
    await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 100)
    # TODO: friend activity
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
