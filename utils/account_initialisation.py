"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

This file creates the base version of all necessary files for an account.
"""
import datetime
import os
import uuid

import motor.core
import motor.motor_asyncio

from utils.services.calendar.calendar import ScheduledEvents
from utils.utils import normalise_string, format_time, uuid_generator


async def initialise_account(database: motor.core.AgnosticDatabase, account_id: str = None, display_name: str = None,
                             password: bytes = None, email: str = None, calendar: ScheduledEvents = None) -> str:
    """
    Initialises an account with the given account ID. If no account ID is given, one will be generated.
    :param database: The database to use
    :param account_id: The account ID to initialise
    :param display_name: The display name to use
    :param password: The password to use
    :param email: The email to use
    :param calendar: The calendar class to fetch events from
    :return: account_id
    """
    if account_id is None:
        account_id = await uuid_generator()
    # initialise the account services
    await database["accounts"].insert_one({
        "_id": account_id,
        "displayName": display_name,
        "minorVerified": False,
        "minorStatus": "NOT_MINOR",
        "cabinedMode": False,
        "name": None,
        "email": email,
        "failedLoginAttempts": 0,
        "lastLogin": None,
        "numberOfDisplayNameChanges": 0,
        "dateOfBirth": None,
        "ageGroup": "ADULT",
        "headless": True if display_name is None else False,
        "country": None,
        "lastName": None,
        "phoneNumber": None,
        "preferredLanguage": "en",
        "lastDisplayNameChange": None,
        "canUpdateDisplayName": True,
        "tfaEnabled": False,
        "emailVerified": False,
        "minorExpected": False,
        "hasHashedEmail": False,
        "externalAuths": {},
        "extra": {
            "pwhash": password.decode() if password is not None else None,
            "deviceAuths": []
        },
        "metadata": {
            "FGOnboarded": "true"
        }
    })
    # initialise entitlement service
    await database["entitlements"].insert_one({
        "_id": account_id,
        "entitlements": []
    })
    # initialise friends service
    await database["friends"].insert_one({
        "_id": account_id,
        "friends": [],
        "incoming": [],
        "outgoing": [],
        "suggested": [],
        "blocklist": [],
        "settings": {
            "acceptInvites": "public",
            "mutualPrivacy": "ALL"
        },
        "limitsReached": {
            "incoming": False,
            "outgoing": False,
            "accepted": False
        }
    })
    # initialise wex services
    await database["profile_friends"].insert_one({
        "_id": account_id,
        "created": await format_time(),
        "updated": await format_time(),
        "rvn": 1,
        "wipeNumber": 4,
        "profileId": "friends",
        "version": "force_max_friends_to_100",
        "items": {},
        "stats": {
            "attributes": {
                "daily_friends": {},
                "max_friend_count": 100,
                "daily_friend_uses": 2
            }
        },
        "commandRevision": 0
    })
    await database["profile_levels"].insert_one({
        "_id": account_id,
        "created": await format_time(),
        "updated": await format_time(),
        "rvn": 1,
        "wipeNumber": 4,
        "profileId": "levels",
        "version": "grant_pvp_item",
        "items": {},
        "stats": {
            "attributes": {
                "last_played_level": "",
                "last_used_friend_id": "",
                "portal_level": "",
                "personal_events": [
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 5,
                        "zoneId": "Zone.Event.PE.MidgamePet.First.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "a7604ceb-768d-4e6a-ae99-50d4286038b8",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 4,
                        "zoneId": "Zone.Event.PE.MidgamePet.Second.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "a7604ceb-768d-4e6a-ae99-50d4286038b8",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 3,
                        "zoneId": "Zone.Event.PE.MidgamePet.Third.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "a7604ceb-768d-4e6a-ae99-50d4286038b8",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 2,
                        "zoneId": "Zone.Event.PE.MidgamePet.Fourth.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "a7604ceb-768d-4e6a-ae99-50d4286038b8",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 1,
                        "zoneId": "Zone.Event.PE.MidgamePet.Fifth.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "a7604ceb-768d-4e6a-ae99-50d4286038b8",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 5,
                        "zoneId": "Zone.Event.PE.MidgameChallenge.First.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "86ad5c0f-159d-4b9c-9383-07b3dd12cd74",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 4,
                        "zoneId": "Zone.Event.PE.MidgameChallenge.Second.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "86ad5c0f-159d-4b9c-9383-07b3dd12cd74",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 3,
                        "zoneId": "Zone.Event.PE.MidgameChallenge.Third.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "86ad5c0f-159d-4b9c-9383-07b3dd12cd74",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 2,
                        "zoneId": "Zone.Event.PE.MidgameChallenge.Fourth.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "86ad5c0f-159d-4b9c-9383-07b3dd12cd74",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    },
                    {
                        "expiresAt": "2999-12-31T23:59:59.999Z",
                        "sortPriority": 1,
                        "zoneId": "Zone.Event.PE.MidgameChallenge.Fifth.Map1",
                        "maxRuns": 1,
                        "resetCostMtx": 0,
                        "eventKey": "86ad5c0f-159d-4b9c-9383-07b3dd12cd74",
                        "flags": [],
                        "dynamicTier": -1,
                        "dynamicGoldTier": -1,
                        "dynamicWorldLevel": -1
                    }
                ],
                "portal_expires": "min",
                "last_forgiven_abandon": "min"
            }
        },
        "commandRevision": 0
    })
    await database["profile_monsterpit"].insert_one({
        "_id": account_id,
        "created": await format_time(),
        "updated": await format_time(),
        "rvn": 1,
        "wipeNumber": 4,
        "profileId": "monsterpit",
        "version": "remove_pet_upgrades",
        "items": {},
        "stats": {
            "attributes": {
                "highest_pit_power": 0,
                "pit_power_dirty": True,
                "pit_power": 0,
                "pit_level": 1
            }
        },
        "commandRevision": 0
    })
    await database["profile_multiplayer"].insert_one({
        "_id": account_id,
        "created": await format_time(),
        "updated": await format_time(),
        "rvn": 1,
        "wipeNumber": 5,
        "profileId": "multiplayer",
        "version": "initial",
        "items": {
            str(uuid.uuid4()): {
                "templateId": "MultiplayerMode:PvpDuel",
                "attributes": {
                    "lifetime_wins": 0,
                    "current_enemies_defeated": 0,
                    "defense_rating": 0,
                    "current_losses": 0,
                    "attack_rating": 0,
                    "match_roster": [],
                    "lifetime_enemies_defeated": 0,
                    "recent_matches": [],
                    "pvp_match_count": 0,
                    "match_refresh": {},
                    "current_wins": 0,
                    "recent_opponents": [],
                    "lifetime_losses": 0
                },
                "quantity": 1
            }
        },
        "stats": {
            "attributes": {
                "daily_pvp_wins": 0,
                "last_refresh": "0021-12-01T21:12:00.000Z",
                "current_pvp_win_date": "0021-12-01T21:12:00.000Z",
                "pvp_taunt": "",
                "default_parties": {},
                "matchmaking_id": "",
                "daily_pvp_reward_limit": 25
            }
        },
        "commandRevision": 0
    })
    if calendar is not None:
        await calendar.update_required_events()
        current_event = calendar.battlepass.states[0].state.get("seasonId", "2018_1")
    else:
        current_event = "2018_1"
    await database["profile_profile0"].insert_one({
        "_id": account_id,
        "created": await format_time(),
        "updated": await format_time(),
        "rvn": 1,
        "wipeNumber": 4,
        "profileId": "profile0",
        "version": "initialize_season_end_date",
        "items": {
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_Market",
                "attributes": {
                    "level": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_Silver",
                "attributes": {},
                "quantity": 40000
            },
            str(uuid.uuid4()): {
                "templateId": "Energy:PvP",
                "attributes": {
                    "fatigue": 0,
                    "updated": await format_time(),
                    "charge_rate": 1,
                    "max_value": 120
                },
                "quantity": 120
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_WS",
                "attributes": {},
                "quantity": 15000
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_SpiralTower",
                "attributes": {
                    "level": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_Bronze",
                "attributes": {},
                "quantity": 80000
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_HeroTower_Elemental",
                "attributes": {
                    "Normal_static_currency_amount": 100,
                    "Special_static_reward_template_id": "Reagent:Reagent_HeroMap_SuperRare",
                    "level": 0,
                    "chest_options": [
                        {
                            "heroChoicesDeprecated": [],
                            "itemChoices": [
                                "Character:Warrior_Starter_Fire_Berserking_T03",
                                "Character:Warrior_R2_Nature_Whirlwind_T03",
                                "Character:MartialArtist_R2_Water_Ironfist_T03"
                            ],
                            "itemQuantities": [
                                1,
                                1,
                                1
                            ],
                            "heroTrackId": "CoreBasic",
                            "foilLevel": 0
                        }
                    ],
                    "Special_static_currency_template_id": "Reagent:Reagent_HeroMap_Elemental",
                    "Special_static_currency_amount": 500,
                    "Normal_static_reward_amount": 1,
                    "Special_static_reward_amount": 5,
                    "Normal_static_currency_template_id": "Reagent:Reagent_HeroMap_Elemental",
                    "CoreBasic_progress": 0,
                    "chest_info_content_version": "",
                    "page_index": 0,
                    "foil_lvl": -1,
                    "Normal_static_reward_template_id": "Reagent:Reagent_HeroMap_SuperRare"
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Giftbox:GB_AccountLevel01",
                "attributes": {
                    "sealed_days": 0,
                    "params": {},
                    "min_level": 10
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Energy:PvE",
                "attributes": {
                    "fatigue": 0,
                    "updated": await format_time(),
                    "charge_rate": 30,
                    "max_value": 300
                },
                "quantity": 300
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_HeroTower_Bronze",
                "attributes": {
                    "Normal_static_currency_amount": 1,
                    "Normal_static_currency_template_id": "Reagent:Reagent_HeroMap_Bronze",
                    "chest_info_content_version": "",
                    "level": 0,
                    "chest_options": [
                        {
                            "heroChoicesDeprecated": [
                                "Character:Archer_UC1_Fire_ElementalBreath_T03",
                                "Character:MartialArtist_UC1_Nature_ChargedFist_T03",
                                "Character:Knight_UC2_Water_SpearThrust_T03"
                            ],
                            "itemChoices": [],
                            "itemQuantities": [],
                            "heroTrackId": "CoreBronze",
                            "foilLevel": 0
                        }
                    ],
                    "CoreBronze_progress": 0,
                    "page_index": -1,
                    "foil_lvl": -1,
                    "Normal_static_reward_template_id": "",
                    "Normal_static_reward_amount": 1
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_PlanarRifts",
                "attributes": {
                    "level": 1
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "MajorEventTracker:MajorEventTracker",
                "attributes": {
                    "level": 0,
                    "seasonId": "0",
                    "totalLevels": 0,
                    "xp": 0,
                    "totalRuns": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_CrystalForge",
                "attributes": {
                    "level": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_Gold",
                "attributes": {},
                "quantity": 25000
            },
            str(uuid.uuid4()): {
                "templateId": "MajorEventTracker:BattlepassSeason",
                "attributes": {
                    "seasonId": current_event,
                    "level": 0,
                    "totalLevels": 0,
                    "xp": 0,
                    "totalRuns": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_LevelCompletion",
                "attributes": {},
                "quantity": 125000
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_Mine",
                "attributes": {},
                "quantity": 18000000
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_HeroTower_SuperRare",
                "attributes": {
                    "Normal_static_currency_amount": 100,
                    "Normal_static_currency_template_id": "Reagent:Reagent_HeroMap_SuperRare",
                    "chest_info_content_version": "",
                    "level": 0,
                    "chest_options": [
                        {
                            "heroChoicesDeprecated": [
                                "Character:Warmage_SR2_Fire_Shadowflame_T05",
                                "Character:MartialArtist_SR1_Dark_ExplodingPalm_T05",
                                "Character:DragonKnight_SR1_Water_JumpStrike_T05"
                            ],
                            "itemChoices": [],
                            "itemQuantities": [],
                            "heroTrackId": "CoreSuperRare",
                            "foilLevel": 0
                        }
                    ],
                    "page_index": -1,
                    "foil_lvl": -1,
                    "Normal_static_reward_template_id": "",
                    "CoreSuperRare_progress": 0,
                    "Normal_static_reward_amount": 1
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "HqBuilding:HQ_AncientFactory",
                "attributes": {
                    "level": 0
                },
                "quantity": 1
            },
            str(uuid.uuid4()): {
                "templateId": "Currency:SB_Platinum",
                "attributes": {},
                "quantity": 15000
            }
        },
        "stats": {
            "attributes": {
                "active_hammer_chest": "",
                "labor_force": {},
                "labor_refill_cd": "min",
                "affiliate_id": "",
                "normalized_name": await normalise_string(display_name),
                "season_xp": 0,
                "mtx_purchase_history": {},
                "default_parties": {},
                "daily_purchases": {},
                "in_app_purchases": {
                    "receipts": [],
                    "packages": []
                },
                "current_battlepass": current_event,
                "hero_limit": 15,
                "is_pvp_unlocked": False,
                "days_since_started": 0,
                "mtx_level": 0,
                "level": 1,
                "battlepass_purchase_history": {},
                "current_major_event": "",
                "weekly_challenge_xp": 0,
                "starter_hero": "",
                "rep_hero_ids": [],
                "has_started": False,
                "display_name": display_name,
                "secret_shop_page": {
                    "unlock_time": None,
                    "page": 0
                },
                "store_level": 0,
                "market_page": {
                    "unlock_time": None,
                    "page": 0
                },
                "tracked_days_since_started": 0,
                "recent_party_id": "",
                "notification_optin_reward_claimed": False,
                "weapon_limit": 500,
                "starter_hero_template_id": "",
                "vip_level": 0,
                "event_purchases": {
                    "event_id": "",
                    "offers": {}
                },
                "account_perks": {},
                "hero_store_page": {
                    "unlock_time": None,
                    "page": 0
                },
                "activity": {
                    "a": {
                        "date": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT00:00:00.000Z"),
                        "claimed": False,
                        "props": {
                            "BaseBonus": 10
                        }
                    },
                    "standardGift": 10
                },
                "hammer_quest_energy": {
                    "energy_spent": 0,
                    "energy_required": 100,
                    "claim_count": 0
                },
                "standard_gift": 10,
                "num_territories_claimed": 0,
                "daily_quest_last_refresh": "0021-12-01T21:12:00.000Z",
                "debug_ltm": "",
                "recovery_code": str(int(os.urandom(3).hex(), 16)),
                "has_external_account": False,
                "hammer_quest_realtime": {
                    "next_claim": None,
                    "claim_count": 0
                },
                "is_headless": True if display_name is None else False,
                "current_season_end_date": "2022-12-28T00:00:00.000Z",
                "max_rep_heroes": 1,
                "armor_limit": 500,
                "season_regular_claim_level": -1,
                "rewards_claimed": {},
                "last_reported_account_level_milestone": 0,
                "rocket_unlock": 0,
                "last_battlepass_purchased": "",
                "inventory_limit_bonus": 0,
                "weekly_purchases": {},
                "num_levels_completed": 0,
                "avatar_url": "wex-temp-avatar.png",
                "weekly_challenge_level": 0,
                "monthly_purchases": {},
                "xp": 0,
                "event_next_level": 0,
                "login_reward": {
                    "last_claim_time": "0021-12-01T21:12:00.000Z",
                    "next_level": 1
                },
                "season_premium_claim_level": -1,
                "come_back_reward_claimed": False,
                "is_developer": False
            }
        },
        "commandRevision": 2
    })
    await database["receipts"].insert_one({"_id": account_id, "receipts": []})
    return account_id
