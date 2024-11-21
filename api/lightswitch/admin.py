"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the admin operations for lightswitch control
"""
import datetime

import sanic

from utils import types
from utils.utils import authorized as auth, admin_auth

from utils.sanic_gzip import Compress

compress = Compress()
admin = sanic.Blueprint("lightswitch_admin")


@admin.route("/api/admin/update_status", methods=["POST"])
@auth()
@admin_auth()
@compress.compress()
async def lightswitch_admin_update(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Handles updating the lightswitch downtime and status
    :param request: The request object
    :return: The response object
    """
    lightswitch = request.app.ctx.lightswitch
    downtime_start = request.json.get("downtime_start")
    if downtime_start:
        lightswitch.downtime_start = datetime.datetime.fromtimestamp(downtime_start, datetime.UTC)
    else:
        lightswitch.downtime_start = None
    downtime_end = request.json.get("downtime_end")
    if downtime_end:
        lightswitch.downtime_end = datetime.datetime.fromtimestamp(downtime_end, datetime.UTC)
    else:
        lightswitch.downtime_end = None
    return sanic.response.json(await lightswitch.refresh_status())
