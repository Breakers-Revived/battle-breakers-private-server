"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles verifying real money mtx mcp
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_verify_realmoney = sanic.Blueprint("wex_verify_realmoney")


# undocumented
@wex_verify_realmoney.route("/<accountId>/VerifyRealMoneyPurchase", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def verify_rmt(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to verify if receipts are legit or fake!! Checks for profile changes after a purchase.
    :param request: The request object
    :param accountId: The account id
    :return: The response object containing the profile changes
    """
    receipts = (await request.app.ctx.db["receipts"].find_one({"_id": accountId})).get("receipts", [])
    for receipt in receipts:
        if receipt["receiptId"] == request.json.get("receiptId") and \
                receipt["appStore"] == request.json.get("appStore") and \
                receipt["appStoreId"] == request.json.get("appStoreId") and \
                receipt["receiptInfo"] == request.json.get("receiptInfo"):
            break
    else:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid receipt")
    iap = await request.ctx.profile.get_stat("in_app_purchases")
    match request.json.get("appStore"):
        case "EpicPurchasingService":
            if f"EPIC:{request.json.get('receiptId')}" not in iap["receipts"] and f"EPIC:{request.json.get('receiptId')}" not in iap["ignoredReceipts"]:
                iap["receipts"].append(f"EPIC:{request.json.get('receiptId')}")
                await request.ctx.profile.modify_stat("in_app_purchases", iap)
                # TODO: fulfill the purchase
                await request.ctx.profile.add_notifications({
                    "type": "CatalogPurchase",
                    "primary": True,
                    "lootResult": {
                        "tierGroupName": f"Fulfillment:/{request.json.get('receiptInfo')}",
                        "items": []
                    }
                }, request.ctx.profile_id)
        case _:
            pass
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
