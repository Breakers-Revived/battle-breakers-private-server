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
lightswitch_version = sanic.Blueprint("lightswitch_ver")


# undocumented
@lightswitch_version.route("/api/version", methods=["GET"])
@compress.compress()
async def lightswitch_version_route(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Version information

    :param request: The request object
    :return: The response object
    """
    return sanic.response.json({
        "app": "lightswitch",
        "serverDate": await format_time(),
        "overridePropertiesVersion": "unknown",
        "cln": "unknown",
        "build": "unknown",
        "moduleName": "unknown",
        "buildDate": "2023-04-14T06:55:25.238Z",
        "version": "unknown",
        "branch": "unknown",
        "modules": {
            "Epic-LightSwitch-AccessControlCore": {
                "cln": "24565549",
                "build": "b2144",
                "buildDate": "2023-03-08T20:12:52.378Z",
                "version": "1.0.0",
                "branch": "trunk"
            },
            "epic-common-core": {
                "cln": "a2be7743a57e32be7adac6d23287eb8be91bc87c",
                "build": "b1191",
                "buildDate": "2023-03-02T19:14:18.251Z",
                "version": "4.0.23.20230302191242",
                "branch": "master"
            }
        }
    })
