"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the bulk offers for wex catalog
"""

import sanic

from utils import types
from utils.utils import authorized as auth, read_file_cached

from utils.sanic_gzip import Compress

compress = Compress()
bulk = sanic.Blueprint("catalog_bulk")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Catalog%20Service/catalog/api/shared/bulk/offers.md
@bulk.route("/api/shared/bulk/offers", methods=["GET"])
@auth(allow_basic=True)
@compress.compress()
async def offers(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Get offers
    :param request: The request object
    :return: The response object
    """
    # TODO: Support locale
    catalog_offers = await read_file_cached(f"res/catalog/api/shared/bulk/offers.json")
    catalog_ids = request.args.getlist("id")
    catalog = {}
    for catalog_id in catalog_ids:
        if catalog_id in catalog_offers:
            # TODO: support returnItemDetails
            catalog[catalog_id] = catalog_offers[catalog_id]
    return sanic.response.json(catalog)
