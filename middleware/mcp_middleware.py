"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

This file contains the middleware for the mcp related endpoints
"""

import datetime
import uuid

from utils.utils import sanitise_header

import sanic.request


async def add_mcp_headers(request: sanic.request.Request, response: sanic.response.JSONResponse) -> None:
    """
    Adds the standard MCP headers to the response

    :param request: The request object
    :param response: The response object
    :return: None
    """
    content_version = request.headers.get('X-EpicGames-WEX-BuildVersion')
    if content_version is None:
        try:
            content_version = request.headers.get('User-Agent').split('build=')[1]
        except (AttributeError, IndexError, TypeError):
            try:
                content_version = f'{request.headers.get("User-Agent").split("version=")[1].split(",")[0].split("-")[-1]}.0-r{request.headers.get("User-Agent").split("version=")[1].split(",")[0].split("-")[1].split("+")[0]}'
            except (AttributeError, IndexError, TypeError):
                content_version = "1.88.244-r17036752"
    corrid = request.headers.get('X-Epic-Correlation-ID')
    if corrid is None:
        try:
            corrid = str(request.id)
        except (AttributeError, TypeError):
            corrid = str(uuid.uuid4())
    try:
        if request.ctx.dvid is not None:
            response.headers["X-Epic-Device-ID"] = sanitise_header(request.ctx.dvid)
    except AttributeError:
        pass
    response.headers["Date"] = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["X-EpicGames-McpVersion"] = "prod Release-1.88-1.88 build 107 cl 19310354"
    response.headers["X-EpicGames-ContentVersion"] = sanitise_header(content_version)
    response.headers["X-EpicGames-MinBuild"] = "-1"
    response.headers["X-Epic-Correlation-ID"] = sanitise_header(corrid)
