"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the manifest
"""
import hashlib

import aiofiles
import sanic

from utils import types
from utils.exceptions import errors
from utils.sanic_gzip import Compress

compress = Compress()
wex_manifest = sanic.Blueprint("wex_manifest")


# undocumented
@wex_manifest.route("/api/game/v2/manifests/<manifest>", methods=['GET'])
@compress.compress()
async def wex_cloudv3_manifests(request: types.BBRequest, manifest: str) -> sanic.response.HTTPResponse:
    """
    Handles the manifest request for builds before build manifest (i.e. v1.5 and older)
    :param request: The request object
    :param manifest: The manifest
    :return: The response object
    """
    # yes, this is more ugly than the regex in utils, however its roughly 2-8x faster
    try:
        changelist = request.headers.get("User-Agent").split('version=')[1].split(",")[0].split("-")[1].split("+")[0]
    except:
        changelist = None
    if changelist is None:
        changelist = "3891207"

    # ~ 2ms
    # try:
    #     with open(f"res/wex/api/game/v2/manifests/CL_{changelist}/{manifest.lower()}", "rb") as f:
    #         manifest = orjson.dumps(orjson.loads(f.read())).decode("utf-8")
    # except:
    #     raise sanic.exceptions.FileNotFound("Manifest not found")
    # return sanic.response.text(manifest, content_type="text/text")

    # ~ 150ms
    # try:
    #     return await sanic.response.file(f"res/wex/api/game/v2/manifests/CL_{changelist}/{manifest.lower()}",
    #                                      mime_type="text/plain")
    # except:
    #     raise sanic.exceptions.FileNotFound("Manifest not found")

    # ~ 1.5ms
    try:
        manifest_file: bytes = await (
            await aiofiles.open(f"res/wex/api/game/v2/manifests/CL_{changelist}/{manifest.lower()}", "rb")).read()
        md5_hash: str = hashlib.md5(manifest_file).hexdigest().upper()
        if request.headers.get("If-None-Match") == f'"{md5_hash}"':
            return sanic.response.text("", status=304, headers={"ETag": f'"{md5_hash}"'})
        return sanic.response.text(manifest_file.decode(), content_type="text/text",
                                   headers={"ETag": f'"{md5_hash}"'})
    except:
        raise errors.com.epicgames.common.not_found()
