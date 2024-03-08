"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the manifest cdn downloads
"""
import aiofiles
import sanic

from utils import types
from utils.sanic_gzip import Compress

compress = Compress()
build_manifest = sanic.Blueprint("cdn_build_manifest")


# undocumented
@build_manifest.route(r"/<version:(\d\.\d*\.\d*-r\d*)>/<file:(BuildManifest-\w*\.txt)>", methods=["GET"])
@compress.compress()
async def build_manifest_request(request: types.BBRequest, version: str,
                                 file: str) -> sanic.response.HTTPResponse:
    """
    Handles the build manifest txt request
    :param request: The request object
    :param version: The game content version
    :param file: The manifest file to download
    :return: The response object (204)
    """
    try:
        async with aiofiles.open(f"res/wex/api/game/v2/manifests/{file.replace('.txt', '')} {version}.txt",
                                 "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        # raise sanic.exceptions.FileNotFound("BuildManifest not found")
        raise sanic.exceptions.BadRequest("BuildManifest not found")


# undocumented
@build_manifest.route(r"/<version:(\d\.\d*\.\d*-r\d*)>/<platform>/<pak:(\w*chunk\d*[-_]pak\d*\.pak)>", methods=["GET"])
@compress.compress()
async def build_manifest_pak(request: types.BBRequest, version: str, platform: str,
                             pak: str) -> sanic.response.HTTPResponse:
    """
    Handles the pak chunk downloads
    :param request: The request object
    :param version: The game content version
    :param platform: The platform and texture format
    :param pak: The pak chunk to download
    :return: The response object (204)
    """
    try:
        async with aiofiles.open(f"D:/Battle Breakers/{version}/{platform}/{pak}", "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise sanic.exceptions.FileNotFound("chunk was not found")
