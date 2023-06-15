"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the silly version info
"""

import sanic

from utils.sanic_gzip import Compress

compress = Compress()
catalog_version = sanic.Blueprint("catalog_ver")


# undocumented
@catalog_version.route("/api/version", methods=["GET"])
@compress.compress()
async def catalog_version_route(request: sanic.request.Request) -> sanic.response.JSONResponse:
    """
    Version information

    :param request: The request object
    :return: The response object
    """
    return sanic.response.json({
        "app": "com.epicgames.catalog.public",
        "serverDate": await request.app.ctx.format_time(),
        "overridePropertiesVersion": "unknown",
        "cln": "605b456849d4a0de36d7d75c0514ba345905921f",
        "build": "b11675",
        "moduleName": "Epic-Catalog-PublicService",
        "buildDate": "2023-04-24T09:35:00.369Z",
        "version": "4.2.9",
        "branch": "TRUNK",
        "modules": {
            "epic-common-core": {
                "cln": "01b0a30780e8d1b4b4327fda403299fd635c6559",
                "build": "b1096",
                "buildDate": "2022-09-21T13:55:01.514Z",
                "version": "3.2.35.20220921145409",
                "branch": "master"
            }
        }
    })