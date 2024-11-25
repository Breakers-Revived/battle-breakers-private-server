"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles all the item ratings requests
"""
import urllib.parse

import sanic

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, load_character_data, load_datatable, read_file

compress = Compress()
wex_item_ratings = sanic.Blueprint("wex_item_ratings")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/item_ratings/accountId/templateId.md
@wex_item_ratings.route("/api/game/v2/item_ratings/<accountId>/<templateId>", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def item_ratings(request: types.BBRequest, accountId: str, templateId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to get item ratings from the server
    :param request: The request object
    :param accountId: The account id
    :param templateId: The template id
    :return: The response object (204)
    """
    my_rating = {
        "gameplayRating": 0,
        "appearanceRating": 0
    }
    template_id = urllib.parse.unquote(templateId)
    character_datatable = await load_datatable("Content/Characters/Datatables/CharacterStats")
    # TODO: rating key compatability for older versions
    rating_key = (character_datatable[0]["Rows"].get(
        (await load_character_data(template_id))[0]["Properties"]["CharacterStatsHandle"]["RowName"],
        {}).get("RatingsKey", f"CD.{template_id.split(':')[1].replace('_', '.')}")).replace(".", "_")
    data = await request.app.ctx.db["item_ratings"].find_one({"_id": accountId}, {rating_key: 1, "_id": 0})
    if data and rating_key in data:
        my_rating = data[rating_key]
    base_ratings = await read_file("res/wex/api/game/v2/item_ratings/base_ratings.json")
    user_ratings = request.app.ctx.db["item_ratings"].find({rating_key: {'$ne': None}},
                                                           {rating_key: 1, "_id": 0})
    ratings = [{
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }]
    if rating_key in base_ratings:
        i = 0
        for rating in base_ratings[rating_key]:
            ratings[i] = {
                "gameplayRating": rating[0],
                "appearanceRating": rating[1]
            }
            i += 1
    async for rating in user_ratings:
        if rating_key in rating:
            if rating[rating_key]["gameplayRating"] != 0:
                ratings[rating[rating_key]["gameplayRating"] - 1]["gameplayRating"] += 1
            if rating[rating_key]["appearanceRating"] != 0:
                ratings[rating[rating_key]["appearanceRating"] - 1]["appearanceRating"] += 1
    return sanic.response.json({
        "myRating": my_rating,
        "overallRatings": {
            "ratingsKey": rating_key.replace("_", "."),
            "discussUrl": "https://discord.gg/stw-dailies-757765475823517851",
            "ratings": ratings
        }
    })


# undocumented
@wex_item_ratings.route("/api/game/v2/item_ratings/<accountId>/<templateId>", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def set_item_rating(request: types.BBRequest, accountId: str, templateId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to rate an item
    :param request: The request object
    :param accountId: The account id
    :param templateId: The template id
    :return: The response object (204)
    """
    template_id = urllib.parse.unquote(templateId)
    character_datatable = await load_datatable("Content/Characters/Datatables/CharacterStats")
    # TODO: rating key compatability for older versions
    rating_key = (character_datatable[0]["Rows"].get(
        (await load_character_data(template_id))[0]["Properties"]["CharacterStatsHandle"]["RowName"],
        {}).get("RatingsKey", f"CD.{template_id.split(':')[1].replace('_', '.')}")).replace(".", "_")
    rating_data = {
        "gameplayRating": request.json["gameplayRating"],
        "appearanceRating": request.json["appearanceRating"]
    }
    if rating_data["gameplayRating"] > 5:
        rating_data["gameplayRating"] = 5
    elif rating_data["gameplayRating"] < 0:
        rating_data["gameplayRating"] = 0
    if rating_data["appearanceRating"] > 5:
        rating_data["appearanceRating"] = 5
    elif rating_data["appearanceRating"] < 0:
        rating_data["appearanceRating"] = 0
    await request.app.ctx.db["item_ratings"].update_one({"_id": accountId}, {"$set": {rating_key: rating_data}},
                                                        upsert=True)
    base_ratings = await read_file("res/wex/api/game/v2/item_ratings/base_ratings.json")
    user_ratings = request.app.ctx.db["item_ratings"].find({rating_key: {'$ne': None}},
                                                           {rating_key: 1, "_id": 0})
    ratings = [{
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }, {
        "gameplayRating": 0,
        "appearanceRating": 0
    }]
    if rating_key in base_ratings:
        i = 0
        for rating in base_ratings[rating_key]:
            ratings[i] = {
                "gameplayRating": rating[0],
                "appearanceRating": rating[1]
            }
            i += 1
    async for rating in user_ratings:
        if rating_key in rating:
            if rating[rating_key]["gameplayRating"] != 0:
                ratings[rating[rating_key]["gameplayRating"] - 1]["gameplayRating"] += 1
            if rating[rating_key]["appearanceRating"] != 0:
                ratings[rating[rating_key]["appearanceRating"] - 1]["appearanceRating"] += 1
    return sanic.response.json({
        "myRating": rating_data,
        "overallRatings": {
            "ratingsKey": rating_key.replace("_", "."),
            "discussUrl": "https://discord.gg/stw-dailies-757765475823517851",
            "ratings": ratings
        }
    })


# undocumented
@wex_item_ratings.route("/api/game/v2/item_ratings/<accountId>/", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def get_all_item_ratings(request: types.BBRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to get all item ratings from the server
    :param request: The request object
    :param accountId: The account id
    :return: The response object (204)
    """
    data = await request.app.ctx.db["item_ratings"].find_one({"_id": accountId}, {"_id": 0})
    return sanic.response.json(data)
