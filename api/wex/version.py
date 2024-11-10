"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the silly version info
"""
import platform
import re
import sys

import cpuinfo
import jwt
import orjson
import sanic
import git
import distro

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import format_time

compress = Compress()
wex_version = sanic.Blueprint("wex_ver")


# undocumented
@wex_version.route("/api/version", methods=["GET"])
@compress.compress()
async def wex_version_route(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Version information

    :param request: The request object
    :return: The response object
    """
    git_repo = git.Repo(search_parent_directories=True)
    try:
        build_date = git_repo.head.commit.committed_datetime.isoformat()
    except:
        build_date = "unknown"
    try:
        version_hash = git_repo.head.commit.hexsha
    except:
        version_hash = "unknown"
    try:
        branch = git_repo.head.reference.name
    except:
        branch = "unknown"
    try:
        cpu_info = re.sub(r'\(.\)|\(..\)| CPU |@ ....GHz', '', cpuinfo.get_cpu_info()['brand_raw'])
    except:
        cpu_info = "unknown"
    return sanic.response.json({
        "app": "WEX",
        "serverDate": await format_time(),
        "overridePropertiesVersion": "unknown",
        "cln": "19310354",
        "build": "107",
        "moduleName": "WorldExplorers-Live",
        "buildDate": build_date,
        "version": version_hash,
        "branch": branch,
        "modules": {
            "epic-common-core": {
                "cln": "14266600",
                "build": "2977",
                "buildDate": "2021-02-17T23:13:44.655Z",
                "version": "2.1",
                "branch": "TRUNK"
            },
            "Epic-LightSwitch-AccessControlCore": {
                "cln": "24565549",
                "build": "b2144",
                "buildDate": "2023-03-08T20:12:52.378Z",
                "version": "1.0.0",
                "branch": "trunk"
            },
        },
        "extra": {
            "About": "This is a Battle Breakers server 'emulator'. Not affiliated with Epic Games.",
            "Author": "Alexander Hanson",
            "GitHub": "https://github.com/dippyshere",
            "Repository": "https://github.com/dippyshere/battle-breakers-private-server",
            "Discord": ["dippy is not here#1332", "dippyshere#8105"],
            "Version": {
                "Python": sys.version,
                "Sanic": sanic.__version__,
                "GitPython": git.__version__,
                "PyJWT": jwt.__version__,
                "Orjson": orjson.__version__,
                "Platform": f"{platform.python_implementation()} {platform.python_version()}",
                "OS": f"{re.sub(r'-', ' ', platform.platform(aliased=True))}"
                      f" {platform.win32_edition() if platform.system() == 'Windows' else ''}",
                "Distribution": f"{distro.name() + ' ' + distro.version() if platform.system() == 'Linux' else ''}",
                "CPU": f"{cpu_info}",
                "Architecture": f"{platform.machine()}",
                "System": f"{platform.system()}",
                "Release": f"{platform.release()}",
                "Node": f"{platform.node()}",
                "Processor": f"{platform.processor()}",
                "Executable": f"{sys.executable}",
                "Flags": f"{sys.flags}"
            }
        }
    })
