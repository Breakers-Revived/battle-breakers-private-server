"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles selecting a starter hero
"""
import datetime

import sanic

from utils.exceptions import errors
from utils.friend_system import PlayerFriends
from utils.profile_system import PlayerProfile
from utils.enums import ProfileType
from utils.utils import authorized as auth, normalise_string, format_time, read_file

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_select_start_options = sanic.Blueprint("wex_profile_select_start_options")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/SelectStartOptions.md
@wex_profile_select_start_options.route("/<accountId>/SelectStartOptions", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def select_start_options(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to choose a starter hero, and update the display name / support a creator code
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if await request.ctx.profile.get_stat("has_started"):
        raise errors.com.epicgames.world_explorers.service_not_required(errorMessage="Already started game")
    await request.ctx.profile.modify_stat("has_started", True)
    await request.ctx.profile.modify_stat("starter_hero",
                                          f"starter{request.json.get('characterTemplateId').split('_')[2]}")
    await request.ctx.profile.modify_stat("starter_hero_template_id", request.json.get('characterTemplateId'))
    starter_character_guid = await request.ctx.profile.add_item({
        "templateId": request.json.get("characterTemplateId"),
        "attributes": {
            "gear_weapon_item_id": "",
            "weapon_unlocked": False,
            "sidekick_template_id": "",
            "is_new": True,
            "level": 1,
            "num_sold": 0,
            "skill_level": 1,
            "sidekick_unlocked": False,
            "upgrades": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "used_as_sidekick": False,
            "gear_armor_item_id": "",
            "skill_xp": 0,
            "armor_unlocked": False,
            "foil_lvl": -1,
            "xp": 0,
            "rank": 0,
            "sidekick_item_id": ""
        },
        "quantity": 1
    })
    await request.ctx.profile.modify_stat("rep_hero_ids", [starter_character_guid])
    party_instance_guid = await request.ctx.profile.add_item({
        "templateId": "Party:Instance",
        "attributes": {
            "commander_index": 3,
            "date_created": await format_time(),
            "character_ids": [
                "",
                "",
                "",
                starter_character_guid,
                "",
                ""
            ],
            "friend_index": 5,
            "party_icon": "None"
        },
        "quantity": 1
    })
    await request.ctx.profile.modify_stat("default_parties", {"LastPvePartyUsed": party_instance_guid})
    for _ in range(3):
        await request.ctx.profile.add_item({
            "templateId": "Party:Instance",
            "attributes": {
                "commander_index": 0,
                "date_created": await format_time(),
                "character_ids": [],
                "friend_index": 5,
                "party_icon": "None"
            },
            "quantity": 1
        })
    await request.ctx.profile.add_item({
        "templateId": "Currency:MtxGiveaway",
        "attributes": {},
        "quantity": 40
    })
    await request.ctx.profile.add_item({
        "templateId": "Currency:Gold",
        "attributes": {},
        "quantity": 700
    })
    await request.ctx.profile.add_item({
        "templateId": "Currency:HeroXp_Basic",
        "attributes": {},
        "quantity": 1000
    })
    await request.ctx.profile.add_item({
        "templateId": "HammerChest:HC_Tutorial",
        "attributes": {
            "taps_applied": 0,
            "taps_remaining": 10
        },
        "quantity": 1
    })
    await request.ctx.profile.modify_stat("display_name", request.json.get("displayName"))
    await request.ctx.profile.modify_stat("normalized_name",
                                          await normalise_string(request.json.get("displayName")))
    await request.app.ctx.database["accounts"].update_one(
        {"_id": accountId},
        {"$set": {"displayName": request.json.get("displayName")}}
    )
    await request.ctx.profile.modify_stat("suggestion_timeout",
                                          await format_time(
                                              datetime.datetime.utcnow() + datetime.timedelta(hours=1)),
                                          ProfileType.FRIENDS)
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = await PlayerFriends.init_friends(accountId)
    suggested_accounts = await request.app.ctx.friends[accountId].suggest_friends(request)
    for account in suggested_accounts:
        account_data: dict = await request.app.ctx.database["accounts"].find_one({"_id": account}, {
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
                    datetime.datetime.utcnow() + datetime.timedelta(hours=3)),
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
    await request.ctx.profile.modify_stat("personal_events", [
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 5,
            "zoneId": "Zone.Event.PE.MidgamePet.First.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "ea2894c5-9f3d-490e-8895-69d869eea350",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 4,
            "zoneId": "Zone.Event.PE.MidgamePet.Second.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "ea2894c5-9f3d-490e-8895-69d869eea350",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 3,
            "zoneId": "Zone.Event.PE.MidgamePet.Third.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "ea2894c5-9f3d-490e-8895-69d869eea350",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 2,
            "zoneId": "Zone.Event.PE.MidgamePet.Fourth.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "ea2894c5-9f3d-490e-8895-69d869eea350",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 1,
            "zoneId": "Zone.Event.PE.MidgamePet.Fifth.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "ea2894c5-9f3d-490e-8895-69d869eea350",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 5,
            "zoneId": "Zone.Event.PE.MidgameChallenge.First.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "614f498f-e93b-47fb-8399-4a8ad35be995",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 4,
            "zoneId": "Zone.Event.PE.MidgameChallenge.Second.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "614f498f-e93b-47fb-8399-4a8ad35be995",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 3,
            "zoneId": "Zone.Event.PE.MidgameChallenge.Third.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "614f498f-e93b-47fb-8399-4a8ad35be995",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 2,
            "zoneId": "Zone.Event.PE.MidgameChallenge.Fourth.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "614f498f-e93b-47fb-8399-4a8ad35be995",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 1,
            "zoneId": "Zone.Event.PE.MidgameChallenge.Fifth.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "614f498f-e93b-47fb-8399-4a8ad35be995",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 8,
            "zoneId": "Zone.Event.NewPlayer.Map1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 7,
            "zoneId": "Zone.Event.NewPlayer.Map2",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 6,
            "zoneId": "Zone.Event.NewPlayer.Map3",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 5,
            "zoneId": "Zone.Event.NewPlayer.Map4",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 4,
            "zoneId": "Zone.Event.NewPlayer.Map5",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 3,
            "zoneId": "Zone.Event.NewPlayer.Map6",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 2,
            "zoneId": "Zone.Event.NewPlayer.Map7",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        },
        {
            "expiresAt": "2099-01-04T00:00:00.000Z",
            "sortPriority": 1,
            "zoneId": "Zone.Event.NewPlayer.Map8",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "eventKey": "4c08026d-88ea-416a-8477-340b9c2c73c6",
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1
        }
    ], ProfileType.LEVELS)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
