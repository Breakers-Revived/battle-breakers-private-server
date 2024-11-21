"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the service status for Battle Breakers
"""

import sanic

from utils import types
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
status = sanic.Blueprint("lightswitch_status")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Lightswitch%20Service/lightswitch/api/service/bulk/status.md
@status.route("/api/service/bulk/status", methods=["GET"])
@auth(allow_basic=True)
@compress.compress()
async def lightswitch_bulk(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Handles the lightswitch bulk status request
    :param request: The request object
    :return: The response object
    """
    lightswitch = await request.app.ctx.lightswitch.refresh_status()
    service_id = request.args.getlist("serviceId")
    services = []
    if not service_id:
        service_id = ["WorldExplorersLive"]
    for service in service_id:
        services.append({
            "serviceInstanceId": service.lower(),
            "status": lightswitch["status"],
            "message": lightswitch["message"],
            "maintenanceUri": lightswitch["maintenance_uri"],
            "overrideCatalogIds": ["ae402a2cb61b4c5fa199ce5311cca724"],
            "allowedActions": ["PLAY", "DOWNLOAD"],
            "banned": False,
            "launcherInfoDTO": {
                "appName": service,
                # not bothered / required to fix this for other services
                "catalogItemId": "a53e821fbdc24181877243a8dbb63463",
                "namespace": "wex"
            },
            "timeToShutdownInMs": lightswitch["timeToShutdownInMs"]
        })
    return sanic.response.json(services)


# undocumented
@status.route("/api/service/<serviceId>/status", methods=["GET"])
@compress.compress()
async def lightswitch_service(request: types.BBRequest, serviceId: str) -> sanic.response.JSONResponse:
    """
    Handles the lightswitch status request
    :param request: The request object
    :param serviceId: The service id
    :return: The response object
    """
    lightswitch = await request.app.ctx.lightswitch.refresh_status()
    return sanic.response.json([{
        "serviceInstanceId": serviceId.lower(),
        "status": lightswitch["status"],
        "message": lightswitch["message"],
        "maintenanceUri": lightswitch["maintenance_uri"],
        "overrideCatalogIds": ["ae402a2cb61b4c5fa199ce5311cca724"],
        "allowedActions": ["PLAY", "DOWNLOAD"],
        "banned": False,
        "launcherInfoDTO": {
            "appName": serviceId,
            "catalogItemId": "a53e821fbdc24181877243a8dbb63463",
            "namespace": "wex"
        },
        "timeToShutdownInMs": lightswitch["timeToShutdownInMs"]
    }])
