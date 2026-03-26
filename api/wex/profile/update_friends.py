"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles updating friends
"""
import datetime

import sanic
import sanic_ext

from utils import types
from utils.friend_system import PlayerFriends
from utils.profile_system import PlayerProfile
from utils.enums import ProfileType, FriendStatus
from utils.utils import authorized as auth, format_time, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_update_friends = sanic.Blueprint("wex_profile_update_friends")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpdateFriends.md
@wex_profile_update_friends.route("/<accountId>/UpdateFriends", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpdateFriends, query=MCPQueryValidation.MCPFriends)
@compress.compress()
async def update_friends(request: types.BBProfileRequest, accountId: str,
                         body: MCPValidation.UpdateFriends,
                         query: MCPQueryValidation.MCPFriends) -> sanic.response.JSONResponse:
    """
    This endpoint is used to update the friends list details
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    friend_instances = await request.ctx.profile.find_item_by_template_id("Friend:Instance", request.ctx.profile_id)
    pending_changes = request.ctx.profile.friends_changes
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    friends_list = (await request.app.ctx.friends[accountId].get_summary())["friends"]
    incoming_list = (await request.app.ctx.friends[accountId].get_summary())["incoming"]
    outgoing_list = (await request.app.ctx.friends[accountId].get_summary())["outgoing"]
    result = {}
    async for account in request.app.ctx.db["accounts"].find({"_id": {"$in": friends_list}}, {"_id": 1}):
        result[account["_id"]] = FriendStatus.FRIEND
    async for account in request.app.ctx.db["accounts"].find({"_id": {"$in": incoming_list}}, {"_id": 1}):
        result[account["_id"]] = FriendStatus.INVITED
    async for account in request.app.ctx.db["accounts"].find({"_id": {"$in": outgoing_list}}, {"_id": 1}):
        result[account["_id"]] = FriendStatus.REQUESTED
    for pending_change in pending_changes:
        if pending_change.get("changeType") == "itemAdded" and pending_change.get("item", {}).get(
                "templateId") == "Friend:Instance" and await request.app.ctx.db["accounts"].find_one(
            {"_id": pending_change.get("item", {}).get("attributes", {}).get("accountId")}, {"_id": 1}) is not None:
            result.pop(pending_change.get("item", {}).get("attributes", {}).get("accountId"), None)
    for itemId in friend_instances:
        friend_instance = await request.ctx.profile.get_item_by_guid(itemId, request.ctx.profile_id)
        if friend_instance["attributes"]["accountId"] in result:
            result.pop(friend_instance["attributes"]["accountId"])
        if datetime.datetime.strptime(friend_instance["attributes"]["snapshot_expires"],
                                      "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.UTC) <= datetime.datetime.now(
            datetime.UTC):
            account_data: dict = await request.app.ctx.db["accounts"].find_one(
                {"_id": friend_instance["attributes"]["accountId"]}, {"displayName": 1, "_id": 0})
            if account_data is None:
                # This friend isn't on the private server / was deleted
                # In this case, we preserve their snapshot and entry by marking them as a legacy friend
                # SuggestedLegacy was originally intended for friends on the old (1.0-1.71) friends system,
                # suggesting players to add them back using the Epic friends system
                # Note: Doing this means that clients older than 1.80 cannot parse the friend instance, and will
                # not show the friend in the friends list
                await request.ctx.profile.change_item_attribute(itemId, "status", "SuggestedLegacy",
                                                                request.ctx.profile_id)
                await request.ctx.profile.change_item_attribute(itemId, "snapshot_expires",
                                                                await format_time(
                                                                    datetime.datetime.now(
                                                                        datetime.UTC) + datetime.timedelta(hours=3)),
                                                                request.ctx.profile_id)
                continue
            if friend_instance["attributes"]["accountId"] not in request.app.ctx.profiles:
                request.app.ctx.profiles[friend_instance["attributes"]["accountId"]] = await PlayerProfile.init_profile(
                    friend_instance["attributes"]["accountId"])
            wex_data = await request.app.ctx.profiles[friend_instance["attributes"]["accountId"]].get_profile(
                ProfileType.PROFILE0)
            rep_heroes = []
            account_perks = []
            for account_perk in ["MaxHitPoints", "RegenStat", "PetStrength", "BasicAttack", "Attack", "SpecialAttack",
                                 "DamageReduction", "MaxMana"]:
                account_perks.append(wex_data["stats"]["attributes"].get("account_perks").get(account_perk, 0))
            for hero_id in wex_data["stats"]["attributes"].get("rep_hero_ids", []):
                hero_data = await request.app.ctx.profiles[friend_instance["attributes"]["accountId"]].get_item_by_guid(
                    hero_id)
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
            await request.ctx.profile.change_item_attribute(itemId, "snapshot", {
                "displayName": account_data["displayName"],
                "avatarUrl": "wex-temp-avatar.png",
                "repHeroes": rep_heroes,
                "lastPlayTime": wex_data["updated"],
                "numLevelsCompleted": wex_data["stats"]["attributes"].get("num_levels_completed", 0),
                "numTerritoriesClaimed": wex_data["stats"]["attributes"].get("num_territories_claimed", 0),
                "accountLevel": wex_data["stats"]["attributes"].get("level", 0),
                "numRepHeroes": len(wex_data["stats"]["attributes"].get("rep_hero_ids", [])),
                "isPvPUnlocked": wex_data["stats"]["attributes"].get("is_pvp_unlocked", False)
            }, request.ctx.profile_id)
            await request.ctx.profile.change_item_attribute(itemId, "canBeSparred",
                                                            wex_data["stats"]["attributes"].get("is_pvp_unlocked",
                                                                                                False),
                                                            request.ctx.profile_id)
            await request.ctx.profile.change_item_attribute(itemId, "status", "Friend", request.ctx.profile_id)
            await request.ctx.profile.change_item_attribute(itemId, "snapshot_expires",
                                                            await format_time(
                                                                datetime.datetime.now(
                                                                    datetime.UTC) + datetime.timedelta(hours=3)),
                                                            request.ctx.profile_id)
    for friend in result:
        await request.ctx.profile.add_friend_instance(request, friend, result[friend])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
