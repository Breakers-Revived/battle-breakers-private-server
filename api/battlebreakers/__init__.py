"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the cdn for battle breakers
"""
import sanic
from .build_manifest_manager import build_manifest
from .chunkv3_manager import chunk_manifest
from .motd import bb_motd

bb_cdn = sanic.Blueprint.group(build_manifest, chunk_manifest, bb_motd)
