"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles MongoDB database migration.
"""

import pymongo
import asyncio
import orjson


async def migrate_to_mongodb():
    """
    Migrates the database to MongoDB.
    """
    client = pymongo.AsyncMongoClient("mongodb://localhost:27017")
    database = client["dippy_battle_breakers"]
    collection = database["profile_friends"]

    for files in os.listdir("C:/Users/dippy/PycharmProjects/battle-breakers-private-server/res/wex/api/receipts/v1/account"):
        with open(f"C:/Users/dippy/PycharmProjects/battle-breakers-private-server/res/wex/api/game/v2/profile/{files.split('.')[0]}/QueryProfile/friends.json", "rb") as file:
            data = orjson.loads(file.read())

        # replace id with _id
        # data["_id"] = data["id"]
        # del data["id"]
        # for entitlement in data:
        #     entitlement["_id"] = entitlement["id"]
        #     del entitlement["id"]

        data["_id"] = files.split(".")[0]
        del data["accountId"]

        # insert into database
        try:
            # await collection.insert_one({"_id": files.split(".")[0], "receipts": data})
            await collection.insert_one(data)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    asyncio.run(migrate_to_mongodb())
