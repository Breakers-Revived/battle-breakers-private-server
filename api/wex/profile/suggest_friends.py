"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the friend suggestion request
"""
import datetime

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.friend_system import PlayerFriends
from utils.profile_system import PlayerProfile
from utils.utils import authorized as auth, format_time, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_suggest_friends = sanic.Blueprint("wex_profile_suggest_friends")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateFriends.md
@wex_profile_suggest_friends.route("/<accountId>/SuggestFriends", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.SuggestFriends, query=MCPQueryValidation.MCPFriends)
@compress.compress()
async def suggest_friends(request: types.BBProfileRequest, accountId: str,
                          body: MCPValidation.SuggestFriends,
                          query: MCPQueryValidation.MCPFriends) -> sanic.response.JSONResponse:
    """
    This endpoint is used to request friend suggestions (on legacy clients/friend system)
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    suggested_accounts = await request.app.ctx.friends[accountId].suggest_friends(request)
    for account in suggested_accounts:
        account_data: dict = await request.app.ctx.db["accounts"].find_one({"_id": account}, {
            "displayName": 1,
        })
        if account not in request.app.ctx.profiles:
            request.app.ctx.profiles[account] = await PlayerProfile.init_profile(account)
        wex_data = await request.app.ctx.profiles[account].get_profile(ProfileType.PROFILE0)
        rep_heroes = []
        account_perks = []
        for account_perk in ["MaxHitPoints", "RegenStat", "PetStrength", "BasicAttack", "Attack", "SpecialAttack",
                             "DamageReduction", "MaxMana"]:
            account_perks.append(wex_data["stats"]["attributes"].get("account_perks").get(account_perk, 0))
        for hero_id in wex_data["stats"]["attributes"].get("rep_hero_ids", []):
            hero_data = await request.app.ctx.profiles[account].get_item_by_guid(hero_id)
            rep_heroes.append({
                "itemId": hero_id,
                "templateId": hero_data.get("templateId"),
                "bIsCommander": True,
                "level": hero_data.get("attributes").get("level"),
                "skillLevel": hero_data.get("attributes").get("skill_level"),
                "upgrades": hero_data.get("attributes").get("upgrades"),
                "accountInfo": {
                    "level": wex_data["stats"]["attributes"].get("level", 0),
                    "perks": account_perks
                },
                "foilLevel": hero_data.get("attributes").get("foil_lvl", -1),
                "gearTemplateId": hero_data.get("attributes").get("sidekick_template_id", ""),
            })
        await request.ctx.profile.add_item({
            "templateId": "Friend:Instance",
            "attributes": {
                "lifetime_claimed": 0,
                "accountId": account_data["_id"],
                "canBeSparred": False,
                "snapshot_expires": await format_time(
                    datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3)),
                "best_gift": 0,  # These stats are unique to the friend instance on the profile, not the friend
                "lifetime_gifted": 0,
                "snapshot": {
                    "displayName": account_data["displayName"],
                    "avatarUrl": "wex-temp-avatar.png",
                    "repHeroes": rep_heroes,
                    "lastPlayTime": wex_data["updated"],
                    "numLevelsCompleted": wex_data["stats"]["attributes"].get("num_levels_completed", 0),
                    "numTerritoriesClaimed": wex_data["stats"]["attributes"].get("num_territories_claimed", 0),
                    "accountLevel": wex_data["stats"]["attributes"].get("level", 0),
                    "numRepHeroes": len(wex_data["stats"]["attributes"].get("rep_hero_ids", [])),
                    "isPvPUnlocked": wex_data["stats"]["attributes"].get("is_pvp_unlocked", False)
                },
                "remoteFriendId": "",
                "status": "Suggested",
                "gifts": {}
            },
            "quantity": 1
        }, profile_id=ProfileType.FRIENDS)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
