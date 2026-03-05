"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the tax calculation
"""

import sanic

from utils import types
from utils.utils import authorized as auth, read_file_cached

from utils.sanic_gzip import Compress

compress = Compress()
price = sanic.Blueprint("priceengine_price")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Price%20Engine%20Service/priceengine/api/shared/offers/price.md
@price.route("/api/shared/offers/price", methods=["POST"])
@auth(allow_basic=True)
@compress.compress()
async def price_request(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Get price information
    :param request: The request object
    :return: The response object
    """
    # TODO: Support bad input
    # TODO: Support other currencies/countries
    offers = await read_file_cached("res/priceengine/api/shared/offers/price.json")
    line_offers = []
    line_id = 0
    totals = {
        "currencyCode": "AUD",
        "discountPrice": 0,
        "originalPrice": 0,
        "discountPercentage": 100,
        "discount": 0,
        "voucherDiscount": 0,
        "sellerVat": 0,
        "vat": 0,
        "vatRate": 0.1,
        "convenienceFee": 0,
        "basePayoutPrice": 0,
        "basePayoutCurrencyCode": "USD",
        "revenueWithoutTax": 0,
        "revenueWithoutTaxCurrencyCode": "USD",
        "payoutCurrencyExchangeRate": 0.674685939256375
    }
    for offer in request.json["lineOffers"]:
        line_id += 1
        line_offers.append({
            "lineId": str(line_id),
            "quantity": offer["quantity"],
            "taxSkuId": "FR_Game",
            "price": {
                "currencyCode": offers[offer["offerId"]]["currencyCode"],
                "discountPrice": offers[offer["offerId"]]["discountPrice"],
                "unitPrice": offers[offer["offerId"]]["unitPrice"],
                "originalPrice": offers[offer["offerId"]]["originalPrice"],
                "originalUnitPrice": offers[offer["offerId"]]["originalUnitPrice"],
                "discountPercentage": offers[offer["offerId"]]["discountPercentage"],
                "discount": offers[offer["offerId"]]["discount"],
                "voucherDiscount": offers[offer["offerId"]]["voucherDiscount"],
                "sellerVat": offers[offer["offerId"]]["sellerVat"],
                "vat": offers[offer["offerId"]]["vat"],
                "vatRate": offers[offer["offerId"]]["vatRate"],
                "convenienceFee": offers[offer["offerId"]]["convenienceFee"],
                "basePayoutPrice": offers[offer["offerId"]]["basePayoutPrice"],
                "basePayoutCurrencyCode": offers[offer["offerId"]]["basePayoutCurrencyCode"],
                "revenueWithoutTax": offers[offer["offerId"]]["revenueWithoutTax"],
                "revenueWithoutTaxCurrencyCode": offers[offer["offerId"]]["revenueWithoutTaxCurrencyCode"],
                "payoutCurrencyExchangeRate": offers[offer["offerId"]]["payoutCurrencyExchangeRate"],
            },
            # TODO: Price details entry
            "offerId": offer["offerId"],
            "appliedRules": [],
            "ref": offer["offerId"]
        })
        totals["discountPrice"] += offers[offer["offerId"]]["discountPrice"]
        totals["originalPrice"] += offers[offer["offerId"]]["originalPrice"]
        totals["discount"] += offers[offer["offerId"]]["discount"]
        totals["voucherDiscount"] += offers[offer["offerId"]]["voucherDiscount"]
        totals["sellerVat"] += offers[offer["offerId"]]["sellerVat"]
        totals["vat"] += offers[offer["offerId"]]["vat"]
        totals["convenienceFee"] += offers[offer["offerId"]]["convenienceFee"]
        totals["basePayoutPrice"] += offers[offer["offerId"]]["basePayoutPrice"]
        totals["revenueWithoutTax"] += offers[offer["offerId"]]["revenueWithoutTax"]
    return sanic.response.json({
        "accountId": request.json["accountId"],
        "identityId": request.json["accountId"],
        "namespace": "wex",
        "country": request.json["country"],
        "taxType": "Tax",
        "taxCalculationStatus": "SUCCEEDED",
        "totalPrice": totals,
        "totalPaymentPrice": {
            "paymentCurrencyExchangeRate": 1.0,
            "paymentCurrencyCode": "AUD",
            "paymentCurrencySymbol": "$",
            "paymentCurrencyAmount": totals["discountPrice"],
            "paymentCurrencyDecimal": 2
        },
        "coupons": [],
        "lineOffers": line_offers,
        "isB2bVatReverseCharge": True,
        "vatEnabled": True
    })
