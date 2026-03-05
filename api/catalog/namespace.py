"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the namespace offers for epic catalog
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, read_file_cached

from utils.sanic_gzip import Compress

compress = Compress()
catalog_namespace = sanic.Blueprint("catalog_namespace")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Catalog%20Service/catalog/api/shared/namespace/wex/bulk/items.md
@catalog_namespace.route("/api/shared/bulk/namespace/<namespace>/bulk/items", methods=["GET"])
@auth(allow_basic=True)
@compress.compress()
async def items(request: types.BBRequest, namespace: str) -> sanic.response.JSONResponse:
    """
    Get items
    :param request: The request object
    :param namespace: The namespace
    :return: The response object
    """
    if namespace != "wex":
        raise errors.com.epicgames.bad_request(errorMessage="Unsupported namespace")
    # Nothing changes for includemaingamedetails or includedlcdetails for bb
    catalog_items = await read_file_cached(
        f"res/catalog/api/shared/shared/namespace/{namespace}/bulk/items.json")
    catalog_ids = request.form.getlist("id")
    catalog = {}
    for catalog_id in catalog_ids:
        if catalog_id in catalog_items:
            catalog[catalog_id] = catalog_items[catalog_id]
    return sanic.response.json(catalog)
