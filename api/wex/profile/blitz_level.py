"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles level blitz for burny mines
"""
import random
import re
import uuid

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_blitz_level = sanic.Blueprint("wex_profile_blitz_level")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/BlitzLevel.md
@wex_profile_blitz_level.route("/<accountId>/BlitzLevel", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def blitz_level(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to blitz a level
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    # TODO: modify activity chest
    # TODO: proper blitz mine streakbreaker for magicite drops
    if not any(member.get("heroType") == "LocalCommander" for member in request.json.get("partyMembers")):
        raise errors.com.epicgames.world_explorers.bad_request("SingleCommander", "0", "0", "1", errorMessage="Invalid SingleCommander configuration f=0, d=0, l=1")
    treasure_hunter_count = 0
    for member in request.json.get("partyMembers"):
        if member.get("heroType") in ["LocalHero", "LocalCommander"]:
            hero_item = await request.ctx.profile.get_item_by_guid(member.get("heroItemId"))
            if hero_item is None:
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
            if not hero_item.get("templateId").startswith("Character:"):
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
            if "TreasureHunter" in hero_item.get("templateId"):
                treasure_hunter_count += 1
    if not re.match(r"Level\.Mine\.Map[1-4]\.D[1-4]", request.json.get("levelId")):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid level id")
    level_id = request.json.get("levelId")
    gold_item = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))
    if not gold_item:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid gold item")
    gold_id = gold_item[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    silver_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Silver")
    current_silver = 0
    if not silver_id:
        silver_id = str(uuid.uuid4())
    else:
        silver_id = silver_id[0]
        current_silver = (await request.ctx.profile.get_item_by_guid(silver_id))["quantity"]
    magicite_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Magicite")
    current_magicite = 0
    if not magicite_id:
        magicite_id = str(uuid.uuid4())
    else:
        magicite_id = magicite_id[0]
        current_magicite = (await request.ctx.profile.get_item_by_guid(magicite_id))["quantity"]
    iron_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Iron")
    current_iron = 0
    if not iron_id:
        iron_id = str(uuid.uuid4())
    else:
        iron_id = iron_id[0]
        current_iron = (await request.ctx.profile.get_item_by_guid(iron_id))["quantity"]
    loot_items = []
    rolled_items = []
    streakbreaker_id = (await request.ctx.profile.find_item_by_template_id("Currency:SB_Mine"))[0]
    current_streakbreaker = (await request.ctx.profile.get_item_by_guid(streakbreaker_id))["quantity"]
    match level_id.split(".")[2]:
        case "Map1":
            match level_id.split(".")[3]:
                case "D1":
                    if current_gold < 10000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 10000)
                    current_gold -= 10000
                    current_streakbreaker += 10000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(3, 6)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(35, 55)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(35, 55)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D2":
                    if current_gold < 20000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 20000)
                    current_gold -= 20000
                    current_streakbreaker += 20000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(6, 12)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(70, 110)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(70, 110)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D3":
                    if current_gold < 30000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 30000)
                    current_gold -= 30000
                    current_streakbreaker += 30000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(9, 18)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(105, 165)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(105, 165)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D4":
                    if current_gold < 40000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 40000)
                    current_gold -= 40000
                    current_streakbreaker += 40000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(12, 24)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
        case "Map2":
            match level_id.split(".")[3]:
                case "D1":
                    if current_gold < 20000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 20000)
                    current_gold -= 20000
                    current_streakbreaker += 20000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(6, 12)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(70, 110)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(70, 110)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D2":
                    if current_gold < 40000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 40000)
                    current_gold -= 40000
                    current_streakbreaker += 40000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(12, 24)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D3":
                    if current_gold < 60000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 60000)
                    current_gold -= 60000
                    current_streakbreaker += 60000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(18, 36)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(210, 330)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(210, 330)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D4":
                    if current_gold < 80000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 80000)
                    current_gold -= 80000
                    current_streakbreaker += 80000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(24, 48)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(280, 440)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(280, 440)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
        case "Map3":
            match level_id.split(".")[3]:
                case "D1":
                    if current_gold < 30000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 30000)
                    current_gold -= 30000
                    current_streakbreaker += 30000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(9, 18)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(105, 165)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(105, 165)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D2":
                    if current_gold < 60000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 60000)
                    current_gold -= 60000
                    current_streakbreaker += 60000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(18, 36)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(210, 330)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(210, 330)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D3":
                    if current_gold < 90000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 90000)
                    current_gold -= 90000
                    current_streakbreaker += 90000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(27, 56)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(315, 495)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(315, 495)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D4":
                    if current_gold < 120000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 120000)
                    current_gold -= 120000
                    current_streakbreaker += 120000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(36, 72)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(420, 660)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(420, 660)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
        case "Map4":
            match level_id.split(".")[3]:
                case "D1":
                    if current_gold < 40000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 40000)
                    current_gold -= 40000
                    current_streakbreaker += 40000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(12, 24)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(140, 220)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D2":
                    if current_gold < 80000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 80000)
                    current_gold -= 80000
                    current_streakbreaker += 80000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(24, 48)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(280, 440)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(280, 440)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D3":
                    if current_gold < 120000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 120000)
                    current_gold -= 120000
                    current_streakbreaker += 120000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(36, 72)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(420, 660)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(420, 660)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
                case "D4":
                    if current_gold < 160000:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough gold")
                    await request.ctx.profile.change_item_quantity(gold_id, current_gold - 160000)
                    current_gold -= 160000
                    current_streakbreaker += 160000
                    if random.randint(1, 100) <= 25:
                        magicite_instance = random.randint(48, 96)
                        rolled_items.append({
                                    "itemType": "Ore:Ore_Magicite",
                                    "itemGuid": magicite_id,
                                    "itemProfile": "profile0",
                                    "quantity": magicite_instance
                                })
                        if current_magicite > 0:
                            await request.ctx.profile.change_item_quantity(magicite_id, current_magicite + magicite_instance)
                        else:
                            await request.ctx.profile.add_item({
                                "templateId": "Ore:Ore_Magicite",
                                "attributes": {},
                                "quantity": magicite_instance
                            }, magicite_id)
                        current_magicite += magicite_instance
                    silver_instance = random.randint(560, 880)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Silver",
                                "itemGuid": silver_id,
                                "itemProfile": "profile0",
                                "quantity": silver_instance
                            })
                    if current_silver > 0:
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver + silver_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Silver",
                            "attributes": {},
                            "quantity": silver_instance
                        }, silver_id)
                    current_silver += silver_instance
                    iron_instance = random.randint(560, 880)
                    rolled_items.append({
                                "itemType": "Ore:Ore_Iron",
                                "itemGuid": iron_id,
                                "itemProfile": "profile0",
                                "quantity": iron_instance
                            })
                    if current_iron > 0:
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
                    else:
                        await request.ctx.profile.add_item({
                            "templateId": "Ore:Ore_Iron",
                            "attributes": {},
                            "quantity": iron_instance
                        }, iron_id)
                    current_iron += iron_instance
    stars = await request.ctx.profile.get_stat("num_levels_completed")
    try:
        difficulty = int(level_id[-1])
    except ValueError:
        difficulty = 1
    await request.ctx.profile.remove_item(request.json.get("levelItemId"), request.ctx.profile_id)
    mtx_item_id = (await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway"))[0]
    mtx_quantity = (await request.ctx.profile.get_item_by_guid(mtx_item_id))["quantity"]
    for unlocked_level_guids in (await request.ctx.profile.find_item_by_template_id("WorldUnlock:Level",
                                                                                    request.ctx.profile_id)):
        level_item = await request.ctx.profile.get_item_by_guid(unlocked_level_guids, request.ctx.profile_id)
        if level_item["attributes"]["levelId"] == level_id:
            break
    else:
        await request.ctx.profile.add_item({
            "templateId": "WorldUnlock:Level",
            "attributes": {
                "levelId": level_id
            },
            "quantity": 1
        }, profile_id=request.ctx.profile_id)
        await request.ctx.profile.modify_stat("num_levels_completed", stars + difficulty)
        loot_items.append({
            "tierGroupName": "Level.FirstInstance",
            "items": [{
                "itemType": "Currency:MtxGiveaway",
                "itemGuid": mtx_item_id,
                "itemProfile": "profile0",
                "quantity": 20
            }]
        })
        await request.ctx.profile.change_item_quantity(mtx_item_id, mtx_quantity + 20)
    await request.ctx.profile.modify_stat("last_played_level", level_id, profile_id=request.ctx.profile_id)
    await request.ctx.profile.modify_stat("last_used_friend_id", request.json.get("friendInstanceId"), profile_id=request.ctx.profile_id)
    iron_instance = random.randint(1, 10)
    loot_items.append({
        "tierGroupName": "Level.Instance",
        "items": [
            {
                "itemType": "Ore:Ore_Iron",
                "itemGuid": iron_id,
                "itemProfile": "profile0",
                "quantity": iron_instance
            }
        ]
    })
    if current_iron > 0:
        await request.ctx.profile.change_item_quantity(iron_id, current_iron + iron_instance)
    else:
        await request.ctx.profile.add_item({
            "templateId": "Ore:Ore_Iron",
            "attributes": {},
            "quantity": iron_instance
        })
    loot_items.append({
        "tierGroupName": "Level.EventsLoot",
        "items": [
            {
                "itemType": "Currency:Gold",
                "itemGuid": gold_id,
                "itemProfile": "profile0",
                "quantity": 1
            }
        ]
    })
    if current_streakbreaker > 68000000:
        voucher_id = await request.ctx.profile.find_item_by_template_id("Voucher:Voucher_Hero_Mine")
        if not voucher_id:
            voucher_id = await request.ctx.profile.add_item({
                "templateId": "Voucher:Voucher_Hero_Mine",
                "attributes": {},
                "quantity": 1
            })
        else:
            voucher = await request.ctx.profile.get_item_by_guid(voucher_id[0])
            await request.ctx.profile.change_item_quantity(voucher_id[0], voucher["quantity"] + 1)
        rolled_items.insert(0, {
            "itemType": "Voucher:Voucher_Hero_Mine",
            "itemGuid": voucher_id,
            "itemProfile": "profile0",
            "quantity": 1
        })
        await request.ctx.profile.change_item_quantity(streakbreaker_id, 18000000)
    else:
        await request.ctx.profile.change_item_quantity(streakbreaker_id, current_streakbreaker)
    rolled_loot = {
        "tierGroupName": "",
        "items": []
    }
    for item in rolled_items:
        rolled_loot["items"].append(item)
    loot_items.insert(0, rolled_loot)
    blitz_notification = {
        "type": "WExpLevelCompleted",
        "primary": False,
        "accountXp": 0,
        "bonusAccountXp": 0,
        "levelId": level_id,
        "completed": True,
        "loot": loot_items
    }
    await request.ctx.profile.change_item_quantity(gold_id, current_gold + 1)
    await request.ctx.profile.add_notifications(blitz_notification, ProfileType.LEVELS)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions, True)
    )
