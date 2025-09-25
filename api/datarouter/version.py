"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the silly version info
"""

import sanic

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import format_time

compress = Compress()
datarouter_version = sanic.Blueprint("datarouter_ver")


# undocumented
@datarouter_version.route("/api/version", methods=["GET"])
@compress.compress()
async def datarouter_version_route(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Version information

    :param request: The request object
    :return: The response object
    """
    return sanic.response.json({
        "app": "datarouter",
        "serverDate": await format_time(),
        "overridePropertiesVersion": "unknown",
        "cln": "04e1eec103849796502f0c58b08075c5d254f09f",
        "build": "b1290",
        "moduleName": "main",
        "buildDate": "2023-01-27T08:44:42.837Z",
        "version": "1.0.0",
        "branch": "trunk",
        "modules": {
            "epic-common-core": {
                "cln": "14266600",
                "build": "2977",
                "buildDate": "2021-02-17T23:13:44.655Z",
                "version": "2.1",
                "branch": "TRUNK"
            }
        }
    })
