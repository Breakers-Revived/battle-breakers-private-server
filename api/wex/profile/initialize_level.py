"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles initializing a level for a profile.
"""
import uuid

import sanic

from utils import types
from utils.exceptions import errors
from utils.enums import ProfileType
from utils.utils import authorized as auth, load_datatable, format_time, room_generator

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_initialize_level = sanic.Blueprint("wex_profile_initialize_level")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/InitializeLevel.md
@wex_profile_initialize_level.route("/<accountId>/InitializeLevel", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def initialize_level(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to initialize a level for a profile.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    level_info = (await load_datatable("Content/World/Datatables/LevelInfo"))[0]["Rows"].get(
        request.json.get("levelId"))
    if level_info is None:
        raise errors.com.epicgames.world_explorers.level_not_found()
    level_item_id = str(uuid.uuid4())
    await request.ctx.profile.add_item({
        "templateId": "Level:InProgress",
        "attributes": {
            "debug_name": request.json.get("levelId", "")
        },
        "quantity": 1
    }, level_item_id, request.ctx.profile_id)
    energy_id = (await request.ctx.profile.find_item_by_template_id("Energy:PvE"))[0]
    energy_quantity = (await request.ctx.profile.get_item_by_guid(energy_id)).get("quantity", 300)
    energy_cost = level_info.get("EntranceEnergy", 0) + (
            level_info.get("EnergyPerRoom", 0) + level_info.get("NumExpectedRooms", 0))
    await request.ctx.profile.change_item_quantity(energy_id, energy_quantity - energy_cost)
    await request.ctx.profile.change_item_attribute(energy_id, "updated", await format_time())
    # TODO: activity energy spent
    level_notification = {
        "type": "WExpLevelCreated",
        "primary": False,
        "level": {
            "potentialBattlepassXp": 0,  # TODO: calculate battlepass xp
            "levelItemId": level_item_id,
            "rooms": [
                {
                    "roomName": "Room.Treasure.FullClear.R01",
                    "regionName": "Level.BurnyVolcano.Map1.D1",
                    "depth": 1,
                    "worldLevel": 50,
                    "discoveryGoldMult": 24.0,
                    "occupants": []
                },
                {
                    "roomName": "Room.Boss.FindKeyAndExit.R01",
                    "regionName": "Level.BurnyVolcano.Map1.D4",
                    "depth": 2,
                    "worldLevel": 231,
                    "discoveryGoldMult": 6.0,
                    "occupants": [
                        {
                            "isFriendly": False,
                            "characterTemplateId": "Character:Archer_UC1_Fire_ElementalBreath_T04",
                            "spawnGroup": [
                                {
                                    "isFriendly": False,
                                    "characterTemplateId": "Character:Archer_UC1_Fire_ElementalBreath_T03",
                                    "killXp": 120,
                                    "spawnClass": "BossMedium",
                                    "lootTemplateId": "Currency:HeroXp_Basic",
                                    "lootQuantity": 3076
                                },
                                {
                                    "isFriendly": False,
                                    "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T03",
                                    "killXp": 120,
                                    "spawnClass": "BossMedium",
                                    "lootTemplateId": "Currency:HeroXp_Basic",
                                    "lootQuantity": 2843
                                }
                            ],
                            "killXp": 160,
                            "spawnClass": "BossMedium",
                            "lootTemplateId": "Currency:HeroXp_Basic",
                            "lootQuantity": 3546
                        },
                        {
                            "isFriendly": False,
                            "characterTemplateId": "Character:Knight_UC1_Fire_Reconstruction_T03",
                            "spawnGroup": [
                                {
                                    "isFriendly": False,
                                    "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T02",
                                    "killXp": 20,
                                    "spawnClass": "Normal",
                                    "lootTemplateId": "Currency:Gold",
                                    "lootQuantity": 48
                                }
                            ],
                            "killXp": 30,
                            "spawnClass": "Normal",
                            "lootQuantity": 0
                        },
                        {
                            "isFriendly": False,
                            "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T03",
                            "spawnGroup": [],
                            "killXp": 30,
                            "spawnClass": "Normal",
                            "lootQuantity": 0
                        },
                        {
                            "isFriendly": False,
                            "characterTemplateId": "Character:Ninja_UC1_Fire_SwiftStrike_T03",
                            "spawnGroup": [
                                {
                                    "isFriendly": False,
                                    "characterTemplateId": "Character:MartialArtist_UC1_Fire_ChargedFist_T03",
                                    "killXp": 30,
                                    "spawnClass": "Normal",
                                    "lootQuantity": 0
                                }
                            ],
                            "killXp": 30,
                            "spawnClass": "Normal",
                            "lootQuantity": 0
                        },
                        {
                            "isFriendly": False,
                            "killXp": 0,
                            "lootTemplateId": "StandIn:AccountXp",
                            "lootQuantity": 30
                        },
                        {
                            "isFriendly": False,
                            "killXp": 0,
                            "lootTemplateId": "StandIn:AccountXp",
                            "lootQuantity": 30
                        },
                        {
                            "isFriendly": False,
                            "killXp": 0,
                            "lootTemplateId": "StandIn:AccountXp",
                            "lootQuantity": 50
                        },
                        {
                            "isFriendly": False,
                            "killXp": 0,
                            "lootTemplateId": "StandIn:AccountXp",
                            "lootQuantity": 50
                        },
                        {
                            "isFriendly": False,
                            "characterTemplateId": "Character:Shrine_Strength",
                            "killXp": 0,
                            "spawnClass": "Normal",
                            "lootQuantity": 0
                        }
                    ]
                }
            ],
            "levelId": request.json.get("levelId", "")
        },
        "heroInfo": []
    }
    for i in range(1, level_info.get("NumExpectedRooms", 1) + 1):
        level_notification["level"]["rooms"].append(await room_generator(
            request.json.get("levelId"), i, level_info))
    account_info = {
        "level": await request.ctx.profile.get_stat("level"),
        "perks": []
    }
    perks = await request.ctx.profile.get_stat("account_perks")
    for account_perk in ["MaxHitPoints", "RegenStat", "PetStrength", "BasicAttack", "Attack", "SpecialAttack",
                         "DamageReduction", "MaxMana"]:
        account_info["perks"].append(perks.get(account_perk, 0))
    if request.json.get("partyMembers") is not None:
        party_members = request.json.get("partyMembers")
    else:
        # Backwards compatability for old clients
        party_members = []
        party_instance = await request.ctx.profile.get_item_by_guid(request.json.get("partyId"))
        for character_id in party_instance.get("attributes").get("character_ids"):
            if party_instance.get("attributes").get("commander_index") == party_instance.get("attributes").get(
                    "character_ids").index(character_id):
                party_members.append({
                    "heroType": "LocalCommander",
                    "heroItemId": character_id
                })
            elif party_instance.get("attributes").get("friend_index") == party_instance.get("attributes").get(
                    "character_ids").index(character_id):
                if request.json.get("friendInstanceId") == "" and request.json.get("commanderId") == "":
                    party_members.append({
                        "heroType": "DefaultCommander",
                        "heroItemId": ""
                    })
                elif request.json.get("friendInstanceId") != "":
                    party_members.append({
                        "heroType": "FriendCommander",
                        "heroItemId": request.json.get("commanderId")
                    })
                elif request.json.get("commanderId") != "":
                    party_members.append({
                        "heroType": "LocalCommander",
                        "heroItemId": request.json.get("commanderId")
                    })
                else:
                    party_members.append({
                        "heroType": "DefaultCommander",
                        "heroItemId": ""
                    })
            else:
                party_members.append({
                    "heroType": "LocalHero",
                    "heroItemId": character_id
                })
    friend_instance_id = request.json.get("friendInstanceId")
    for party_member in party_members:
        if party_member.get("heroType") in ["FriendHero", "FriendCommander"]:
            friend_snapshot_data = await request.ctx.profile.get_item_by_guid(
                friend_instance_id, ProfileType.FRIENDS)
            if friend_snapshot_data is None:
                if str(level_info.get("DefaultFriendCommander", {}).get("AssetPathName")) != "None":
                    level_notification["heroInfo"].append({
                        "itemId": str(uuid.uuid4()),
                        "templateId": f"Character:{level_info.get('DefaultFriendCommander', {}).get('AssetPathName').split('.')[-1][3:]}",
                        "bIsCommander": True,
                        "level": level_info.get("DefaultFriendCommanderLevel"),
                        "skillLevel": 1,
                        "upgrades": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "accountInfo": {
                            "level": 0,
                            "perks": [0, 0, 0, 0, 0, 0, 0, 0]
                        },
                        "foilLevel": 0,
                        "gearTemplateId": "",
                    })
                else:
                    level_notification["heroInfo"].append({
                        "bIsCommander": False,
                        "level": 0,
                        "skillLevel": 0,
                        "foilLevel": 0
                    })
                continue
            else:
                for rep_hero in friend_snapshot_data.get("attributes").get("snapshot").get("repHeroes"):
                    if rep_hero.get("itemId") == party_member.get("heroItemId"):
                        level_notification["heroInfo"].append({
                            "itemId": party_member.get("heroItemId"),
                            "templateId": rep_hero["templateId"],
                            "bIsCommander": False if party_member.get("heroType") == "FriendHero" else True,
                            "level": rep_hero["level"],
                            "skillLevel": rep_hero["skillLevel"],
                            "upgrades": rep_hero["upgrades"],
                            "accountInfo": rep_hero["accountInfo"],
                            "foilLevel": rep_hero["foilLevel"],
                            "gearTemplateId": rep_hero["gearTemplateId"],
                        })
                        break
                else:
                    level_notification["heroInfo"].append({
                        "bIsCommander": False,
                        "level": 0,
                        "skillLevel": 0,
                        "foilLevel": 0
                    })
        elif party_member.get("heroType") in ["LocalHero", "LocalCommander"]:
            hero_data = await request.ctx.profile.get_item_by_guid(party_member.get("heroItemId"))
            if hero_data is not None:
                level_notification["heroInfo"].append({
                    "itemId": party_member.get("heroItemId"),
                    # "itemId": str(uuid.uuid4()),
                    "templateId": hero_data["templateId"],
                    # "templateId": "Character:MageKnight_VR2_Water_RegeneratingBarrier_T06",
                    "bIsCommander": False if party_member.get("heroType") == "LocalHero" else True,
                    "level": hero_data["attributes"]["level"],
                    "skillLevel": hero_data["attributes"]["skill_level"],
                    "upgrades": hero_data["attributes"]["upgrades"],
                    "accountInfo": account_info,
                    "foilLevel": hero_data["attributes"]["foil_lvl"],
                    "gearTemplateId": hero_data["attributes"]["sidekick_template_id"],
                })
            else:
                level_notification["heroInfo"].append({
                    "bIsCommander": False,
                    "level": 0,
                    "skillLevel": 0,
                    "foilLevel": 0
                })
        elif party_member.get("heroType") == "DefaultCommander":
            if str(level_info.get("DefaultFriendCommander", {}).get("AssetPathName")) != "None":
                level_notification["heroInfo"].append({
                    "itemId": str(uuid.uuid4()),
                    "templateId": f"Character:{level_info.get('DefaultFriendCommander', {}).get('AssetPathName').split('.')[-1][3:]}",
                    "bIsCommander": True,
                    "level": level_info.get("DefaultFriendCommanderLevel"),
                    "skillLevel": 1,
                    "upgrades": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "accountInfo": {
                        "level": 0,
                        "perks": [0, 0, 0, 0, 0, 0, 0, 0]
                    },
                    "foilLevel": 0,
                    "gearTemplateId": "",
                })
            else:
                level_notification["heroInfo"].append({
                    "bIsCommander": False,
                    "level": 0,
                    "skillLevel": 0,
                    "foilLevel": 0
                })
        else:
            level_notification["heroInfo"].append({
                "bIsCommander": False,
                "level": 0,
                "skillLevel": 0,
                "foilLevel": 0
            })
    await request.ctx.profile.clear_notifications(ProfileType.LEVELS)
    await request.ctx.profile.add_notifications(level_notification, ProfileType.LEVELS)
    # TODO: daily_friends if friend commander is used
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
    #     "notifications": [
    #         {
    #             "type": "WExpLevelCreated",
    #             "primary": False,
    #             "level": {
    #                 "potentialBattlepassXp": 450,
    #                 "levelItemId": "8f690514-530b-4075-83aa-bb1fac447650",
    #                 "rooms": [
    #                     {
    #                         "roomName": "Room.Treasure.FullClear.R01",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 1,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 24.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 30
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 768
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 936
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 60
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:HealthVial",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:LinkAttackScroll",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 8496
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Shrine_ResurrectionPool",
    #                                 "killXp": 0,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         "roomName": "Room.Boss.FindKeyAndExit.R01",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 2,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 6.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Archer_UC1_Fire_ElementalBreath_T04",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Archer_UC1_Fire_ElementalBreath_T03",
    #                                         "killXp": 120,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootTemplateId": "Currency:HeroXp_Basic",
    #                                         "lootQuantity": 3076
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T03",
    #                                         "killXp": 120,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootTemplateId": "Currency:HeroXp_Basic",
    #                                         "lootQuantity": 2843
    #                                     }
    #                                 ],
    #                                 "killXp": 160,
    #                                 "spawnClass": "BossMedium",
    #                                 "lootTemplateId": "Currency:HeroXp_Basic",
    #                                 "lootQuantity": 3546
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Knight_UC1_Fire_Reconstruction_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 48
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_UC1_Fire_SwiftStrike_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:MartialArtist_UC1_Fire_ChargedFist_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 30
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 30
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 50
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 50
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Shrine_Strength",
    #                                 "killXp": 0,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         "roomName": "Room.Boss.KillBosses.R02",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 3,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 6.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_UC1_Fire_SwiftStrike_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Ninja_Basic_Fire_Flurry_T02",
    #                                         "killXp": 80,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 48
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Knight_Basic_Fire_GuardianStance_T02",
    #                                         "killXp": 80,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 120,
    #                                 "spawnClass": "BossMedium",
    #                                 "lootTemplateId": "Currency:HeroXp_Basic",
    #                                 "lootQuantity": 3236
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Warrior_UC1_Light_Pummel_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootTemplateId": "Currency:HeroXp_Basic",
    #                                 "lootQuantity": 1860
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Knight_UC1_Fire_Reconstruction_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:MartialArtist_UC1_Fire_ChargedFist_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 198
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 96
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 20
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 30
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:HealthVial",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 264
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Assassin_C1_Fire_ImpStab_T01",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Assassin_C1_Fire_ImpStab_T01",
    #                                         "killXp": 10,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 48
    #                                     }
    #                                 ],
    #                                 "killXp": 10,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         "roomName": "Room.Standard.FullClear.Hard.R03",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 4,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 6.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Warrior_UC1_Fire_Pummel_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_Basic_Fire_Flurry_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 54
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Archer_UC1_Fire_ElementalBreath_T04",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:AI_PoisonTank_Fire_T04",
    #                                         "killXp": 60,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 264
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:HeroXp_Basic",
    #                                         "lootQuantity": 1989
    #                                     }
    #                                 ],
    #                                 "killXp": 40,
    #                                 "spawnClass": "Normal",
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 204
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_R2_Fire_TripleStab_T04",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Knight_Basic_Light_GuardianStance_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 54
    #                                     }
    #                                 ],
    #                                 "killXp": 40,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 20
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 10
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:ManaVial",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 40
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Assassin_C1_Fire_ImpStab_T01",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Assassin_C1_Fire_ImpStab_T01",
    #                                         "killXp": 10,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 10,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         "roomName": "Room.Treasure.FullClear.Side.R01",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 4,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 24.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Container:Chest_Fire_VeryHigh",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 1056
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 65
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 864
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 117
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:HealthVial",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Item:HealthVial",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 5328
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 2352
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         "roomName": "Room.Boss.Reveal.Duo.Mix.KillAllEnemies.R02",
    #                         "regionName": "Level.BurnyVolcano.Map1.D4",
    #                         "depth": 5,
    #                         "worldLevel": 231,
    #                         "discoveryGoldMult": 6.0,
    #                         "occupants": [
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Knight_UC1_Fire_Reconstruction_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 54
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Shadowknight_UC2_Fire_Ghoul_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T03",
    #                                         "killXp": 30,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Archer_UC1_Light_ElementalBreath_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Archer_Basic_Light_AimedShot_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 96
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Warrior_Basic_Fire_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Ninja_Basic_Light_Flurry_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Warrior_UC1_Fire_LesserDemon_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Ninja_Basic_Fire_Flurry_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Mage_UC1_Fire_ElementalPhantom_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Knight_Basic_Fire_GuardianStance_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_Basic_Fire_Flurry_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_UC1_Light_SwiftStrike_T03",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     },
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Mage_Basic_Fire_EnergyBlast_T02",
    #                                         "killXp": 20,
    #                                         "spawnClass": "Normal",
    #                                         "lootQuantity": 0
    #                                     }
    #                                 ],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:Ninja_Basic_Fire_Flurry_T03",
    #                                 "spawnGroup": [],
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:HolyKnight_VR1_Fire_FireSword_T05",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:Cleric_UC1_Light_Heal_T04",
    #                                         "killXp": 160,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootTemplateId": "Currency:Gold",
    #                                         "lootQuantity": 222
    #                                     }
    #                                 ],
    #                                 "killXp": 200,
    #                                 "spawnClass": "BossMedium",
    #                                 "lootTemplateId": "Currency:Gold",
    #                                 "lootQuantity": 480
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:AI_Summoner_Fire_T04",
    #                                 "spawnGroup": [
    #                                     {
    #                                         "isFriendly": False,
    #                                         "characterTemplateId": "Character:AI_Exploder_Fire_T04",
    #                                         "killXp": 160,
    #                                         "spawnClass": "BossMedium",
    #                                         "lootTemplateId": "Container:Chest_Fire_High",
    #                                         "lootQuantity": 1
    #                                     }
    #                                 ],
    #                                 "killXp": 160,
    #                                 "spawnClass": "BossMedium",
    #                                 "lootTemplateId": "Container:Chest_Fire_High",
    #                                 "lootQuantity": 1
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 30
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 20
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 50
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "killXp": 0,
    #                                 "lootTemplateId": "StandIn:AccountXp",
    #                                 "lootQuantity": 50
    #                             },
    #                             {
    #                                 "isFriendly": False,
    #                                 "characterTemplateId": "Character:AI_Tower_Fire_Buff_T03",
    #                                 "killXp": 30,
    #                                 "spawnClass": "Normal",
    #                                 "lootQuantity": 0
    #                             }
    #                         ]
    #                     }
    #                 ],
    #                 "levelId": "Level.BurnyVolcano.Map1.D4"
    #             },
    #             "heroInfo": [
    #                 {
    #                     "itemId": "e31f5085-b851-41ac-9eb6-317e76e3e98c",
    #                     "templateId": "Character:Shadowknight_VR2_Dark_SmasherSmash_T06",
    #                     "bIsCommander": True,
    #                     "level": 150,
    #                     "skillLevel": 20,
    #                     "upgrades": [
    #                         95,
    #                         95,
    #                         95,
    #                         95,
    #                         34,
    #                         150,
    #                         6,
    #                         46,
    #                         2
    #                     ],
    #                     "accountInfo": {
    #                         "level": 373,
    #                         "perks": [
    #                             6,
    #                             133,
    #                             209,
    #                             97,
    #                             6,
    #                             12,
    #                             12,
    #                             13
    #                         ]
    #                     },
    #                     "foilLevel": -1,
    #                     "gearTemplateId": ""
    #                 },
    #                 {
    #                     "bIsCommander": False,
    #                     "level": 0,
    #                     "skillLevel": 0,
    #                     "foilLevel": 0
    #                 },
    #                 {
    #                     "itemId": "dab75d65-7911-4f7b-8cc9-88790171650d",
    #                     "templateId": "Character:TreasureHunter_VR2_Fire_AntiMaterialCharge_T06",
    #                     "bIsCommander": False,
    #                     "level": 150,
    #                     "skillLevel": 20,
    #                     "upgrades": [
    #                         95,
    #                         95,
    #                         95,
    #                         95,
    #                         34,
    #                         129,
    #                         5,
    #                         55,
    #                         3
    #                     ],
    #                     "accountInfo": {
    #                         "level": 373,
    #                         "perks": [
    #                             6,
    #                             133,
    #                             209,
    #                             97,
    #                             6,
    #                             12,
    #                             12,
    #                             13
    #                         ]
    #                     },
    #                     "foilLevel": -1,
    #                     "gearTemplateId": "Character:TreasureHunter_R2_Fire_PowerEfflux_T03"
    #                 },
    #                 {
    #                     "itemId": "2dbc336a-554b-449c-ae84-b4697bb00119",
    #                     "templateId": "Character:Ninja_VR1_Light_CrystalDaggers_T06",
    #                     "bIsCommander": False,
    #                     "level": 150,
    #                     "skillLevel": 20,
    #                     "upgrades": [
    #                         95,
    #                         95,
    #                         95,
    #                         95,
    #                         34,
    #                         101,
    #                         4,
    #                         65,
    #                         3
    #                     ],
    #                     "accountInfo": {
    #                         "level": 373,
    #                         "perks": [
    #                             6,
    #                             133,
    #                             209,
    #                             97,
    #                             6,
    #                             12,
    #                             12,
    #                             13
    #                         ]
    #                     },
    #                     "foilLevel": 1,
    #                     "gearTemplateId": "Character:Mage_R2_Light_Cloudburst_T03"
    #                 },
    #                 {
    #                     "itemId": "f01dfe95-6a2c-4a18-a3d9-19709c5f7de1",
    #                     "templateId": "Character:Archer_VR2_Nature_GoinCommando_T06",
    #                     "bIsCommander": False,
    #                     "level": 150,
    #                     "skillLevel": 20,
    #                     "upgrades": [
    #                         95,
    #                         95,
    #                         95,
    #                         95,
    #                         34,
    #                         75,
    #                         3,
    #                         65,
    #                         3
    #                     ],
    #                     "accountInfo": {
    #                         "level": 373,
    #                         "perks": [
    #                             6,
    #                             133,
    #                             209,
    #                             97,
    #                             6,
    #                             12,
    #                             12,
    #                             13
    #                         ]
    #                     },
    #                     "foilLevel": -1,
    #                     "gearTemplateId": "Character:Archer_VR1_Dark_BarbedArrows_T04"
    #                 },
    #                 {
    #                     "itemId": "0cb63754-8755-47cd-96ad-c2d8df596735",
    #                     "templateId": "Character:TreasureHunter_VR1_Fire_TrailBlaze_T04",
    #                     "bIsCommander": False,
    #                     "level": 120,
    #                     "skillLevel": 1,
    #                     "upgrades": [
    #                         25,
    #                         25,
    #                         25,
    #                         25,
    #                         4,
    #                         10,
    #                         0,
    #                         0,
    #                         0
    #                     ],
    #                     "accountInfo": {
    #                         "level": 373,
    #                         "perks": [
    #                             6,
    #                             133,
    #                             209,
    #                             97,
    #                             6,
    #                             12,
    #                             12,
    #                             13
    #                         ]
    #                     },
    #                     "foilLevel": -1,
    #                     "gearTemplateId": ""
    #                 }
    #             ]
    #         }
    #     ],
    #     #"profileCommandRevision": orjson.loads(request.headers.get("X-EpicGames-ProfileRevisions"))[0]["clientCommandRevision"],
    #     "serverTime": "2022-12-29T05:54:05.833Z",
    #     "multiUpdate": [
    #         {
    #             "profileRevision": 40531,
    #             "profileId": "profile0",
    #             "profileChangesBaseRevision": 40455,
    #             "profileChanges": [
    #                 {
    #                     "changeType": "itemQuantityChanged",
    #                     "itemId": "492bb23f-74bf-42bb-a5b5-5ee27deb6169",
    #                     "quantity": 296
    #                 },
    #                 {
    #                     "changeType": "statModified",
    #                     "name": "activity",
    #                     "value": {
    #                         "a": {
    #                             "date": "2022-12-28T00:00:00.000Z",
    #                             "claimed": True,
    #                             "props": {
    #                                 "HeroAcquired": 137,
    #                                 "HeroPromote": 1,
    #                                 "HeroEvolve": 1,
    #                                 "MonsterPitLevelUp": 1,
    #                                 "HeroFoil": 1,
    #                                 "AccountLevelUp": 2,
    #                                 "BaseBonus": 10,
    #                                 "EnergySpent": 187
    #                             }
    #                         },
    #                         "b": {
    #                             "date": "2022-12-29T00:00:00.000Z",
    #                             "claimed": False,
    #                             "props": {
    #                                 "BaseBonus": 10,
    #                                 "EnergySpent": 4
    #                             }
    #                         },
    #                         "standardGift": 10
    #                     }
    #                 }
    #             ],
    #             #"profileCommandRevision": orjson.loads(request.headers.get("X-EpicGames-ProfileRevisions"))[0][
    #             #    "clientCommandRevision"],
    #         }
    #     ],
    #     "responseVersion": 1
    # })
