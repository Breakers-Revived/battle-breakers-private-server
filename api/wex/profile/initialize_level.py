"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles initializing a level for a profile.
"""
import random
import re
import uuid

import sanic

from utils import types
from utils.exceptions import errors
from utils.enums import ProfileType
from utils.utils import authorized as auth, load_datatable, format_time, room_generator, read_file, process_choices

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
    level_id = request.json.get("levelId")
    level_info = (await load_datatable("Content/World/Datatables/LevelInfo"))[0]["Rows"].get(
        request.json.get("levelId"))
    if level_info is None:
        raise errors.com.epicgames.world_explorers.level_not_found()
    level_item_id = str(uuid.uuid4())
    await request.ctx.profile.add_item({
        "templateId": "Level:InProgress",
        "attributes": {
            "debug_name": level_id
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
            "potentialBattlepassXp": 0,
            "levelItemId": level_item_id,
            "rooms": [],
            "levelId": level_id
        },
        "heroInfo": []
    }
    level_data = None
    if re.match(r".*\.D\d", level_id):
        target_difficulty = int(level_id.split(".")[-1][1:])
        for difficulty in range(target_difficulty, 0, -1):
            try:
                level_data = await read_file(f"res/wex/api/game/v2/level_data/{level_id[:-3]}.D{difficulty}.json")
            except FileNotFoundError:
                pass
            if level_data is not None:
                break
        else:
            try:
                level_data = await read_file(f"res/wex/api/game/v2/level_data/{level_id[:-3]}.json")
            except FileNotFoundError:
                pass
    else:
        try:
            level_data = await read_file(f"res/wex/api/game/v2/level_data/{level_id}.json")
        except FileNotFoundError:
            pass
    if level_data is not None:
        level_notification["level"]["potentialBattlepassXp"] = await process_choices(level_data["level"].get("potentialBattlepassXp", 0))
        level_notification["level"]["rooms"] = []
        depth = 1
        for room_data in level_data["level"].get("rooms", []):
            room_name = await process_choices(room_data.get("roomName", ""))
            room_info = (await load_datatable("Content/World/Datatables/LevelRooms"))[0]["Rows"].get(room_name, {})
            room = {
                "roomName": room_name,
                "regionName": await process_choices(room_data.get("regionName", level_id)),
                "depth": depth,
                "worldLevel": int(random.randint(
                    int(level_info["BaseWorldLevel"] * 0.92),
                    int(level_info["BaseWorldLevel"] * 1.09)
                )),
                "discoveryGoldMult": await process_choices(room_data.get("discoveryGoldMult", 1.0)) * room_info.get("GoldDropMult", 1.0),
                "occupants": []
            }
            for occupant_data in room_data.get("occupants", []):
                if random.randint(1, 100) > await process_choices(occupant_data.get("spawnChance", 100)):
                    continue
                occupant = {
                    "isFriendly": occupant_data.get("isFriendly", False),
                    "killXp": await process_choices(occupant_data.get("killXp", 0)),
                }
                if occupant_data.get("characterTemplateId", None):
                    occupant["characterTemplateId"] = await process_choices(occupant_data.get("characterTemplateId", ""))
                    occupant["spawnClass"] = await process_choices(occupant_data.get("spawnClass", "Normal"))
                occupant_data_loot = occupant_data.get("lootTemplateId", [])
                if occupant_data_loot:
                    if isinstance(occupant_data_loot, dict):
                        if occupant_data_loot.get("templateId", "") == "":
                            occupant["lootQuantity"] = 0
                        else:
                            occupant["lootTemplateId"] = await process_choices(occupant_data_loot.get("templateId", ""))
                            occupant["lootQuantity"] = await process_choices(occupant_data_loot.get("quantity", 1))
                    elif isinstance(occupant_data_loot, list):
                        picked_loot = random.choice(occupant_data_loot)
                        if picked_loot:
                            occupant["lootTemplateId"] = await process_choices(picked_loot.get("templateId", ""))
                            occupant["lootQuantity"] = await process_choices(picked_loot.get("quantity", 1))
                        else:
                            occupant["lootQuantity"] = 0
                    elif isinstance(occupant_data_loot, str) and occupant_data_loot != "":
                        occupant["lootTemplateId"] = occupant_data_loot
                        occupant["lootQuantity"] = await process_choices(occupant_data.get("quantity", 1))
                    else:
                        occupant["lootQuantity"] = 0
                else:
                    occupant["lootQuantity"] = 0
                spawn_group_data = occupant_data.get("spawnGroup", [])
                occupant["spawnGroup"] = []
                for spawn_data in spawn_group_data:
                    if random.randint(1, 100) > await process_choices(spawn_data.get("spawnChance", 100)):
                        continue
                    spawn = {
                        "isFriendly": spawn_data.get("isFriendly", False),
                        "characterTemplateId": await process_choices(spawn_data.get("characterTemplateId", "")),
                        "killXp": await process_choices(spawn_data.get("killXp", 0)),
                        "spawnClass": await process_choices(spawn_data.get("spawnClass", "Normal")),
                    }
                    spawn_loot_data = spawn_data.get("lootTemplateId", [])
                    if spawn_loot_data:
                        if isinstance(spawn_loot_data, dict):
                            if spawn_loot_data.get("templateId", "") == "":
                                spawn["lootQuantity"] = 0
                            else:
                                spawn["lootTemplateId"] = await process_choices(spawn_loot_data.get("templateId", ""))
                                spawn["lootQuantity"] = await process_choices(spawn_loot_data.get("quantity", 1))
                        elif isinstance(spawn_loot_data, list):
                            picked_loot = random.choice(spawn_loot_data)
                            if picked_loot:
                                spawn["lootTemplateId"] = await process_choices(picked_loot.get("templateId", ""))
                                spawn["lootQuantity"] = await process_choices(picked_loot.get("quantity", 1))
                            else:
                                spawn["lootQuantity"] = 0
                        elif isinstance(spawn_loot_data, str) and spawn_loot_data != "":
                            spawn["lootTemplateId"] = spawn_loot_data
                            spawn["lootQuantity"] = await process_choices(spawn_data.get("quantity", 1))
                        else:
                            spawn["lootQuantity"] = 0
                    else:
                        spawn["lootQuantity"] = 0
                    occupant["spawnGroup"].append(spawn)
                room["occupants"].append(occupant)
            level_notification["level"]["rooms"].append(room)
            depth += 1
    else:
        level_notification["level"]["rooms"] = await room_generator(level_id, level_info)
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
