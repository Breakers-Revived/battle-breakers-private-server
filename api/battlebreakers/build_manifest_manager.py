"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the manifest cdn downloads
"""
import aiofiles
import sanic

from utils import types, utils
from utils.exceptions import errors
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
        safe_file = await utils.safe_path_join("res/wex/api/game/v2/manifests", f"{file.replace('.txt', '')} {version}.txt")
        async with aiofiles.open(safe_file,"rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise errors.com.epicgames.bad_request(errorMessage="This Build Manifest does not exist, or Build Manifests are unavailable on this server.")


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
    if request.app.config.CONTENT['EXTERNAL-PAK-URL'] and isinstance(request.app.config.CONTENT['EXTERNAL-PAK-URL'], str):
        return sanic.response.redirect(f"{request.app.config.CONTENT['EXTERNAL-PAK-URL']}/{version}/{platform}/{pak}")
    try:
        safe_file = await utils.safe_path_join(request.app.config.CONTENT['BUILD-MANIFEST'], f"{version}/{platform}/{pak}")
        async with aiofiles.open(safe_file, "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise errors.com.epicgames.not_found(errorMessage="Build Manifest PAKs are unavailable on this server.")
