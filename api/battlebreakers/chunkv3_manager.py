"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the chunkv3 manifest cdn downloads
"""
import aiofiles
import sanic

from utils import types, utils
from utils.exceptions import errors
from utils.sanic_gzip import Compress

compress = Compress()
chunk_manifest = sanic.Blueprint("cdn_chunkv3_manifest")


# undocumented
@chunk_manifest.route(
    r"/<environment:(WorldExplorers\w*)>/<changelist:(CL_\d*)>/<platform>/<file:(WorldExplorers_pakchunk\d*CL_\d*\.manifest)>",
    methods=["GET"])
@compress.compress()
async def chunk_manifest_request(request: types.BBRequest, environment: str, changelist: str, platform: str,
                                 file: str) -> sanic.response.HTTPResponse:
    """
    Handles the chunkv3 individual pak manifest request
    :param request: The request object
    :param environment: The environment (WorldExplorersLive/WorldExplorersDevTesting/etc)
    :param changelist: The changelist (CL_1234567)
    :param platform: The platform (WindowsNoEditor/Android_ETC2/Android_ASTC/etc)
    :param file: The manifest file to download (WorldExplorers_pakchunk1CL_1234567.manifest)
    :return: The response object (204)
    """
    try:
        safe_file = await utils.safe_path_join("res/wex/api/game/v2/manifests", 
                                               f"{changelist}/{platform}/{file}")
        async with aiofiles.open(safe_file, "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise errors.com.epicgames.not_found(errorMessage="This ChunkV3 PAK manifest does not exist, or ChunkV3 PAK manifests are unavailable on this server.")


# undocumented
@chunk_manifest.route(
    r"/<environment:(WorldExplorers\w*)>/<changelist:(CL_\d*)>/<platform>/ChunksV3/<DataGroupList:(\d{2})>/<ChunkHashGUID:([0-9A-F]*_[0-9A-F]*\.chunk)>",
    methods=["GET"])
@compress.compress()
async def chunk_manifest_serve_chunks(request: types.BBRequest, environment: str, changelist: str, platform: str,
                                      DataGroupList: str, ChunkHashGUID: str) -> sanic.response.HTTPResponse:
    """
    Handles the chunked cloudv3 downloads
    :param request: The request object
    :param environment: The environment (WorldExplorersLive/WorldExplorersDevTesting/etc)
    :param changelist: The changelist (CL_1234567)
    :param platform: The platform (WindowsNoEditor/Android_ETC2/Android_ASTC/etc)
    :param DataGroupList: The datagrouplist (43)
    :param ChunkHashGUID: The chunk hash guid (34254574B8C46AC9_DF511A404ABE748CE527B6A264B5389A.chunk); theres a more specific regex i could write for this but im not bothered
    :return: The response object (204)
    """
    try:
        safe_file = await utils.safe_path_join(request.app.config.CONTENT['CHUNK-V3'], 
                                               f"{changelist}/{platform}/ChunksV3/{DataGroupList}/{ChunkHashGUID}")
        async with aiofiles.open(safe_file, "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise errors.com.epicgames.not_found(errorMessage="ChunkV3 PAK chunks are unavailable on this server.")
