"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based system to handle the friends service management
"""
import random
from typing_extensions import Optional, Self

from pymongo.asynchronous.database import AsyncDatabase
import sanic
import sanic.log

from utils.enums import FriendStatus
from utils.exceptions import errors
from utils.profile_system import PlayerProfile
from utils.utils import format_time


class PlayerFriends:
    """
    Class based system to handle the friends service management
    """

    def __init__(self, account_id: str) -> None:
        """
        Initialise the friends class.
        This will load the profile from the res folder and set up the variables
        :param account_id: The account ID of the profile
        """
        self.account_id: str = account_id
        self.friends: Optional[dict] = None

    def __str__(self) -> str:
        """
        Return the account ID of the profile
        :return: The account ID of the profile
        """
        return self.account_id

    def __repr__(self) -> str:
        """
        Return the account ID of the profile
        :return: The account ID of the profile
        """
        return self.account_id

    @classmethod
    async def init_friends(cls, account_id: str) -> Self:
        """
        Initialise the friends class.

        :param account_id: The account ID of the profile
        :return: The friends class
        """
        self: PlayerFriends = cls(account_id)
        await self.load_friends(sanic.Sanic.get_app().ctx.db)
        return self

    async def load_friends(self, database: AsyncDatabase) -> None:
        """
        Load the profile based on the account ID and set up the variables
        :return: None
        """
        self.friends = await database["friends"].find_one({"_id": self.account_id})
        self.friends["limitsReached"] = {
            "incoming": False,
            "outgoing": False,
            "accepted": False
        }
        if len(self.friends["friends"]) > 1000:
            self.friends["limitsReached"]["accepted"] = True
        if len(self.friends["incoming"]) > 250:
            self.friends["limitsReached"]["incoming"] = True
        if len(self.friends["outgoing"]) > 250:
            self.friends["limitsReached"]["outgoing"] = True

    async def get_friends(self) -> dict:
        """
        Get the friends data
        :return: The friend data
        """
        return self.friends

    async def get_summary(self) -> dict:
        """
        Get the friends data summary
        :return: The friend data
        """
        # TODO: mutuals calculation if bothered
        return self.friends

    async def get_legacy_summary(self) -> list[dict]:
        """
        Get the legacy friends data for old clients
        :return: The friend data
        """
        friends: list = []
        for friend in self.friends["friends"]:
            friends.append({
                "accountId": friend["accountId"],
                "status": "ACCEPTED",
                "direction": friend.get("direction", "INBOUND"),
                "created": friend["created"],
                "favorite": friend["favorite"]
            })
        for friend in self.friends["incoming"]:
            friends.append({
                "accountId": friend["accountId"],
                "status": "PENDING",
                "direction": "INBOUND",
                "created": friend["created"],
                "favorite": False
            })
        for friend in self.friends["outgoing"]:
            friends.append({
                "accountId": friend["accountId"],
                "status": "PENDING",
                "direction": "OUTBOUND",
                "created": friend["created"],
                "favorite": False
            })
        return friends

    async def send_friend_request(self, request: sanic.request.Request, friendId: str) -> None | dict:
        """
        Send a friend request to a player
        :param request: The request object
        :param friendId: The account ID of the player to send the request to
        :return: The response of the request
        """
        for friend in self.friends["friends"]:
            if friend["accountId"] == friendId:
                raise errors.com.epicgames.friends.duplicate_friendship()
        for friend in self.friends["outgoing"]:
            if friend["accountId"] == friendId:
                raise errors.com.epicgames.friends.friend_request_already_sent()
        if friendId not in request.app.ctx.friends:
            request.app.ctx.friends[friendId]: PlayerFriends = await PlayerFriends.init_friends(friendId)
        other_friend: PlayerFriends = request.app.ctx.friends[friendId]
        for friend in self.friends["incoming"]:
            if friend["accountId"] == friendId:
                await other_friend.add_friend(request, self.account_id)
                await self.add_friend(request, friendId)
                return
        if other_friend.friends["settings"]["acceptInvites"] != "public":
            raise errors.com.epicgames.friends.cannot_friend_due_to_target_settings()
        for blocked in other_friend.friends["blocklist"]:
            if blocked["accountId"] == self.account_id:
                raise errors.com.epicgames.friends.cannot_friend_due_to_target_settings()
        for blocked in self.friends["blocklist"]:
            if blocked["accountId"] == friendId:
                raise errors.com.epicgames.friends.cannot_friend_due_to_target_settings()
        if self.account_id not in request.app.ctx.profiles:
            request.app.ctx.profiles[self.account_id]: PlayerProfile = await PlayerProfile.init_profile(self.account_id)
        await request.app.ctx.profiles[self.account_id].add_friend_instance(request, friendId, FriendStatus.REQUESTED)
        self.friends["outgoing"].append({
            "accountId": friendId,
            "mutual": 0,
            "favorite": False,
            "created": await format_time()
        })
        await self.save_friends()
        if friendId not in request.app.ctx.profiles:
            request.app.ctx.profiles[friendId]: PlayerProfile = await PlayerProfile.init_profile(friendId)
        await request.app.ctx.profiles[friendId].add_friend_instance(request, self.account_id, FriendStatus.INVITED)
        other_friend.friends["incoming"].append({
            "accountId": self.account_id,
            "mutual": 0,
            "favorite": False,
            "created": await format_time()
        })
        await other_friend.save_friends()

    async def add_friend(self, request: sanic.request.Request, friendId: str) -> None:
        """
        Add a friend to the profile
        :param request: The request object
        :param friendId: The account ID of the player to add
        :return: None
        """
        for friend in self.friends["friends"]:
            if friend["accountId"] == friendId:
                return
        if friendId not in request.app.ctx.profiles:
            request.app.ctx.profiles[friendId]: PlayerProfile = await PlayerProfile.init_profile(friendId)
        await request.app.ctx.profiles[friendId].add_friend_instance(request, self.account_id,
                                                                     FriendStatus.FRIEND)
        for friend in self.friends["incoming"]:
            if friend["accountId"] == friendId:
                self.friends["friends"].append({
                    "accountId": friendId,
                    "groups": [],
                    "mutual": 0,
                    "alias": "",
                    "note": "",
                    "favorite": False,
                    "created": await format_time(),
                    "direction": "INBOUND"
                })
                self.friends["incoming"].remove(friend)
                await self.save_friends()
                return
        for friend in self.friends["outgoing"]:
            if friend["accountId"] == friendId:
                self.friends["friends"].append({
                    "accountId": friendId,
                    "groups": [],
                    "mutual": 0,
                    "alias": "",
                    "note": "",
                    "favorite": False,
                    "created": await format_time(),
                    "direction": "OUTBOUND"
                })
                self.friends["outgoing"].remove(friend)
                await self.save_friends()
                return
        self.friends["friends"].append({
            "accountId": friendId,
            "groups": [],
            "mutual": 0,
            "alias": "",
            "note": "",
            "favorite": False,
            "created": await format_time(),
            "direction": "INBOUND"
        })
        await self.save_friends()

    async def remove_friend(self, request: sanic.request.Request, friendId: str) -> None:
        """
        Cancel/decline a friend request / remove a friend
        :param request: The request object
        :param friendId: The account ID of the player to cancel the request to
        :return: The response of the request
        """
        for friend in self.friends["friends"]:
            if friend["accountId"] == friendId:
                self.friends["friends"].remove(friend)
                break
        for friend in self.friends["incoming"]:
            if friend["accountId"] == friendId:
                self.friends["incoming"].remove(friend)
                break
        for friend in self.friends["outgoing"]:
            if friend["accountId"] == friendId:
                self.friends["outgoing"].remove(friend)
                break
        if self.account_id not in request.app.ctx.profiles:
            request.app.ctx.profiles[self.account_id]: PlayerProfile = await PlayerProfile.init_profile(self.account_id)
        await request.app.ctx.profiles[self.account_id].remove_friend_instance(friendId)
        await self.save_friends()
        try:
            if friendId not in request.app.ctx.friends:
                request.app.ctx.friends[friendId]: PlayerFriends = await PlayerFriends.init_friends(friendId)
            other_friend: PlayerFriends = request.app.ctx.friends[friendId]
            for friend in other_friend.friends["friends"]:
                if friend["accountId"] == self.account_id:
                    other_friend.friends["friends"].remove(friend)
                    break
            for friend in other_friend.friends["incoming"]:
                if friend["accountId"] == self.account_id:
                    other_friend.friends["incoming"].remove(friend)
                    break
            for friend in other_friend.friends["outgoing"]:
                if friend["accountId"] == self.account_id:
                    other_friend.friends["outgoing"].remove(friend)
                    break
            if friendId not in request.app.ctx.profiles:
                request.app.ctx.profiles[friendId]: PlayerProfile = await PlayerProfile.init_profile(friendId)
            await request.app.ctx.profiles[friendId].remove_friend_instance(self.account_id)
            await other_friend.save_friends()
        except Exception as e:
            sanic.log.logger.warning(f"Error removing friend on other side: {e}")

    async def update_friends(self, friends: dict) -> None:
        """
        Update the friends data
        :param friends: The new friends data
        :return: None
        """
        self.friends: dict = friends
        await self.save_friends()

    async def save_friends(self) -> None:
        """
        Save the new friends data to the res folder
        :return: None
        """
        collection = sanic.Sanic.get_app().ctx.db["friends"]
        await collection.replace_one({"_id": self.account_id}, self.friends, upsert=True)

    async def suggest_friends(self, request: sanic.request.Request) -> list[str]:
        """
        Suggest friends for the player
        :param request: The request object
        :return: The response of the request
        """
        # TODO: calculate mutual friends and rank suggestions by mutuals
        matching_account_ids = [doc["_id"] async for doc in request.app.ctx.db["friends"].find({
            "_id": {"$ne": self.account_id},
            "friends.friends": {"$ne": {"accountId": self.account_id}},
            "friends.incoming": {"$not": {"$elemMatch": {"accountId": self.account_id}}},
            "friends.outgoing": {"$not": {"$elemMatch": {"accountId": self.account_id}}},
            "friends.settings.acceptInvites": "public"
        }, projection=["_id"])]
        random.shuffle(matching_account_ids)
        suggested_accounts = matching_account_ids[:10]
        self.friends["suggested"] = []
        for suggestion in suggested_accounts:
            self.friends["suggested"].append({
                "accountId": suggestion,
                "mutual": 0,
            })
        await self.save_friends()
        return suggested_accounts
