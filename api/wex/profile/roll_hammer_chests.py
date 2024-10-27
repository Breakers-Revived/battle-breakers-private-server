"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles rolling for new hammer chests
"""
import random

import aiofiles.os
import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, calculate_streakbreaker, load_datatable

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_roll_hammer_chests = sanic.Blueprint("wex_profile_roll_hammer_chests")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/RollHammerChests.md
@wex_profile_roll_hammer_chests.route("/<accountId>/RollHammerChests", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def roll_hammer_chests(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to roll for new hammer chests
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if (await request.ctx.profile.get_stat("active_hammer_chest")) != "":
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage="Unable to roll hammer chests while a chest is active")
    hammer_chest_pool = await aiofiles.os.listdir("res/battle-breakers-data/WorldExplorers/Content/Loot/AccountItems/HammerChests")
    hammer_chest_pool.remove("HC_Tutorial.json")
    hammer_chest_pool = [chest[:-5] for chest in hammer_chest_pool]
    streakbreaker_id = await request.ctx.profile.find_item_by_template_id("Currency:SB_Hammer")
    if streakbreaker_id:
        current_streakbreaker = (await request.ctx.profile.get_item_by_guid(streakbreaker_id[0])).get("quantity")
    else:
        current_streakbreaker = 0
    streakbreaker_roll = await calculate_streakbreaker(current_streakbreaker, base_chance=8)
    # TODO: implement more faithful and accurate streakbreaker (battle breakers bad luck protection)
    if streakbreaker_roll[0]:
        hammer_chest_pool = [chest for chest in hammer_chest_pool if "Rare" in chest]
    else:
        hammer_chest_pool = [chest for chest in hammer_chest_pool if "Rare" not in chest]
    if streakbreaker_id:
        await request.ctx.profile.change_item_quantity(streakbreaker_id[0], streakbreaker_roll[1] + 1)
    else:
        await request.ctx.profile.add_item({
            "templateId": "Currency:SB_Hammer",
            "attributes": {},
            "quantity": streakbreaker_roll[1] + 1
        })
    for selected_chest in random.sample(hammer_chest_pool, 3):
        chest_data = await load_datatable(f"Content/Loot/AccountItems/HammerChests/{selected_chest}")
        await request.ctx.profile.add_item({
            "templateId": f"HammerChest:{selected_chest}",
            "attributes": {
                "taps_applied": 0,
                "taps_remaining": chest_data[0]["Properties"]["TapsToBreak"]
            },
            "quantity": 1
        })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
