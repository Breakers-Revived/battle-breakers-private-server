"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based system to handle the profile management for wex mcp service
"""
import ast
import datetime
import uuid
from types import UnionType
from typing_extensions import Any, Optional, Self

import motor.core
import motor.motor_asyncio
import sanic

from utils.enums import ProfileType, FriendStatus
from utils.utils import format_time

MCPTypes: UnionType = str | int | float | list | dict | bool


class MCPItem:
    """
    Class to handle the MCP item

    :var _guid: The GUID of the item
    :var templateId: The template ID of the item
    :var attributes: The attributes of the item
    :var quantity: The quantity of the item

    Methods:
        __init__(self, guid: str, template_id: str, attributes: dict[str, MCPTypes] = None, quantity: int = 1) -> None:
            Initialise the MCP item
        __repr__(self) -> str:
            Get the representation of the MCP item
        __str__(self) -> str:
            Get the string of the MCP item
        __eq__(self, other: object) -> bool:
            Check if the MCP item is equal to another object
        __ne__(self, other: object) -> bool:
            Check if the MCP item is not equal to another object
        __dict__(self) -> dict[str, Any]:
            Get the dictionary of the MCP item
        __getitem__(self, item: str) -> MCPTypes:
            Get the attribute of the MCP item
        __setitem__(self, key: str, value: MCPTypes) -> None:
            Set the attribute of the MCP item
        __delitem__(self, key: str) -> None:
            Delete the attribute of the MCP item
        __contains__(self, item: str) -> bool:
            Check if the MCP item contains an attribute
        __len__(self) -> int:
            Get the length of the MCP item
        __iter__(self) -> iter:
            Get the iterator of the MCP item
        __reversed__(self) -> reversed:
            Get the reversed iterator of the MCP item
        __copy__(self) -> MCPItem:
            Get a copy of the MCP item

    Static Methods:
        get(self, key: str, default: Any = None) -> Any:
            Get the attribute of the MCP item

    Properties:
        guid: Get the GUID of the MCP item
        item: Get the dictionary of the MCP item
    """

    def __init__(self, guid: str, template_id: str, attributes: dict[str, MCPTypes] = None,
                 quantity: int = 1) -> None:
        """
        Initialise the MCP item
        :param guid: The GUID of the item
        :param template_id: The template ID of the item
        :param attributes: The attributes of the item
        :param quantity: The quantity of the item
        """
        if attributes is None:
            attributes = {}
        self._guid: str = guid
        self.templateId: str = template_id
        self.attributes: dict[str, MCPTypes] = attributes
        self.quantity: int = quantity

    def __repr__(self) -> str:
        """
        Get the representation of the MCP item
        :return: The representation of the MCP item
        """
        return f"<MCPItem guid={self._guid} templateId={self.templateId} attributes={self.attributes} " \
               f"quantity={self.quantity}>"

    def __str__(self) -> str:
        """
        Get the string of the MCP item
        :return: The string of the MCP item
        """
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        """
        Check if the MCP item is equal to another object
        :param other: The other object to check
        :return: Whether the MCP item is equal to the other object
        """
        if not isinstance(other, MCPItem):
            return NotImplemented
        return self._guid == other.guid

    def __ne__(self, other: object) -> bool:
        """
        Check if the MCP item is not equal to another object
        :param other: The other object to check
        :return: Whether the MCP item is not equal to the other object
        """
        if not isinstance(other, MCPItem):
            return NotImplemented
        return self._guid != other.guid

    def __dict__(self) -> dict[str, str | dict[str, MCPTypes] | int]:
        """
        Get the dictionary of the MCP item
        :return: The dictionary of the MCP item
        """
        return self.item

    def __getitem__(self, key: str) -> MCPTypes:
        """
        Get the item value from the MCP item
        :param key: The attribute to get
        :return: The item from the MCP item
        """
        return self.item[key]

    def __setitem__(self, key: str, value: MCPTypes) -> None:
        """
        Set the item value in the MCP item
        :param key: The item to set
        :param value: The value to set
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete an item from the MCP item
        :param key: The item to delete
        """
        delattr(self, key)

    def __contains__(self, key: str) -> bool:
        """
        Check if the MCP item contains the attribute
        :param key: The attribute to check
        :return: Whether the MCP item contains the attribute
        """
        return key in self.attributes

    def __len__(self) -> int:
        """
        Get the length of the MCP item
        :return: The length of the MCP item
        """
        return len(self.attributes)

    def __iter__(self) -> iter:
        """
        Get the iterator of the MCP item
        :return: The iterator of the MCP item
        """
        return iter(self.attributes)

    def __reversed__(self) -> reversed:
        """
        Get the reversed iterator of the MCP item
        :return: The reversed iterator of the MCP item
        """
        return reversed(self.attributes)

    def __copy__(self) -> "MCPItem":
        """
        Copy the MCP item
        :return: The copied MCP item
        """
        return MCPItem(self._guid, self.templateId, self.attributes, self.quantity)

    @property
    def guid(self) -> str:
        """
        Get the GUID of the item
        :return: The GUID of the item
        """
        return self._guid

    @guid.setter
    def guid(self, value: str) -> None:
        """
        Set the GUID of the item
        :param value: The value to set the GUID to
        """
        self._guid = value

    @property
    def item(self) -> dict[str, str | dict[str, MCPTypes] | int]:
        """
        Get the item
        :return: The item
        """
        return {
            "templateId": self.templateId,
            "attributes": self.attributes,
            "quantity": self.quantity
        }

    def get(self, key: str, default: Optional[MCPTypes] = None) -> MCPTypes:
        """
        Get the item value from the MCP item
        :param key: The attribute to get
        :param default: The default value to return if the attribute is not found
        :return: The item from the MCP item
        """
        return self.item.get(key, default)


class MCPProfile:
    """
    A class to represent an MCP profile

    :var accountId: The account ID of the profile
    :var created: The date and time the profile was created
    :var updated: The date and time the profile was last updated
    :var rvn: The revision number of the profile
    :var wipeNumber: The wipe number of the profile
    :var version: The version of the profile
    :var items: The items in the profile
    :var stats: The stats in the profile
    :var commandRevision: The command revision of the profile

    Methods:
        __init__(account_id, profile_type): Initialise the MCP profile
        __repr__(): Get the representation of the MCP profile
        __str__(): Get the string of the MCP profile
        __eq__(other): Check if the MCP profile is equal to another object
        __ne__(other): Check if the MCP profile is not equal to another object
        __dict__(): Get the dictionary of the MCP profile
        __getitem__(key): Get the item value from the MCP profile
        __setitem__(key, value): Set the item value in the MCP profile
        __delitem__(key): Delete an item from the MCP profile
        __contains__(key): Check if the MCP profile contains the attribute
        __len__(): Get the length of the MCP profile

    Properties:
        id: The ID of the profile
        profile_type: The type of the profile
        profile: The profile

    Static Methods:
        get(self, key: str, default: Any = None) -> Any:
            Get the item value from the MCP profile
    """

    def __init__(self, account_id: str, profile_type: ProfileType) -> None:
        """
        Initialise the MCP profile
        :param account_id: The account ID of the profile
        :param profile_type: The type of the profile

        Attributes:
            accountId: The account ID of the profile
            created: The date and time the profile was created
            updated: The date and time the profile was last updated
            rvn: The revision number of the profile
            wipeNumber: The wipe number of the profile
            version: The version of the profile
            items: The items in the profile
            stats: The stats in the profile
            commandRevision: The command revision of the profile
        """
        self._id: Optional[str] = None
        self._profile_type: ProfileType = profile_type
        self.accountId: str = account_id
        self.created: Optional[str] = None
        self.updated: Optional[str] = None
        self.rvn: Optional[int] = None
        self.wipeNumber: Optional[int] = None
        self.version: Optional[str] = None
        self.items: Optional[dict[str, MCPItem]] = None
        self.stats: Optional[dict[str, dict[str, MCPTypes]]] = None
        self.commandRevision: Optional[int] = None

    def __repr__(self) -> str:
        """
        Get the representation of the MCP profile
        :return: The representation of the MCP profile
        """
        return f"<McpProfile account_id={self.accountId} profile_type={self.profile_type} rvn={self.rvn} " \
               f"items={len(self.items)}>"

    def __str__(self) -> str:
        """
        Get the string of the MCP profile
        :return: The string of the MCP profile
        """
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        """
        Check if the MCP profile is equal to another object
        :param other: The other object to check
        :return: Whether the MCP profile is equal to the other object
        """
        if not isinstance(other, MCPProfile):
            return NotImplemented
        return self.accountId == other.accountId and self.profile_type == other.profile_type

    def __ne__(self, other: object) -> bool:
        """
        Check if the MCP profile is not equal to another object
        :param other: The other object to check
        :return: Whether the MCP profile is not equal to the other object
        """
        if not isinstance(other, MCPProfile):
            return NotImplemented
        return self.accountId != other.accountId or self.profile_type != other.profile_type

    def __bool__(self) -> bool:
        """
        Check if the MCP profile is valid
        :return: Whether the MCP profile is valid
        """
        return self.accountId is not None and self.profile_type is not None

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the MCP profile
        :return: The dictionary of the MCP profile
        """
        return self.profile

    def __getitem__(self, key: str) -> MCPTypes:
        """
        Get the value of the key in the MCP profile
        :param key: The key to get the value of
        :return: The value of the key in the MCP profile
        """
        return self.profile[key]

    def __setitem__(self, key: str, value: MCPTypes) -> None:
        """
        Set the value of the key in the MCP profile
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the MCP profile
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the MCP profile
        :param key: The key to delete
        :return: The value of the key in the MCP profile
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the MCP profile
        :return: The length of the MCP profile
        """
        return len(self.profile)

    @property
    def id(self) -> str:
        """
        Get the ID of the profile
        :return: The ID of the profile
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """
        Set the ID of the profile
        :param value: The value to set the ID to
        """
        self._id = value

    @property
    def profile_type(self) -> str:
        """
        Get the profile type
        :return: The profile type
        """
        return self._profile_type.value

    @property
    def profile(self) -> dict[str, Any]:
        """
        Get the profile
        :return: The profile
        """
        return {
            "_id": self._id,
            "created": self.created,
            "updated": self.updated,
            "rvn": self.rvn,
            "wipeNumber": self.wipeNumber,
            "accountId": self.accountId,
            "profileType": self.profile_type,
            "version": self.version,
            "items": self.items,
            "stats": self.stats,
            "commandRevision": self.commandRevision
        }

    @profile.setter
    def profile(self, value: dict[str, Any]) -> None:
        """
        Set the profile
        :param value: The value to set the profile to
        """
        self.updated = value.get("updated", self.updated)
        self.rvn = value.get("rvn", self.rvn)
        self.items = value.get("items", self.items)
        self.stats = value.get("stats", self.stats)
        self.commandRevision = value.get("commandRevision", self.commandRevision)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the profile
        :param key: The key to get the value from
        :param default: The default value to return if the key doesn't exist
        :return: The value from the profile
        """
        return self.profile.get(key, default)

    @classmethod
    async def init_profile(cls, account_id: str, profile_type: ProfileType,
                           database: motor.core.AgnosticDatabase) -> Self:
        """
        Initialise the profile

        :param account_id: The account ID of the profile to initialise
        :param profile_type: The profile type of the profile to initialise
        :param database: The database to use
        :return:
        """
        self: MCPProfile = cls(account_id, profile_type)
        await self.load_profile(database)
        return self

    async def load_profile(self, database: motor.core.AgnosticDatabase) -> None:
        """
        Load the profile

        :param database: The database to use
        """
        collection = database[f"profile_{self.profile_type}"]
        profile = await collection.find_one({"_id": self.accountId})
        self._id: str = profile.get("_id")
        self.created: str = profile.get("created")
        self.updated: str = profile.get("updated")
        self.rvn: int = profile.get("rvn")
        self.wipeNumber: int = profile.get("wipeNumber")
        self.version: str = profile.get("version")
        if self.items is None:
            self.items: dict[str, MCPItem] = {}
        for item, item_data in profile.get("items").items():
            self.items[item]: MCPItem = MCPItem(item, item_data["templateId"], item_data["attributes"],
                                                item_data["quantity"])
        self.stats: dict[str, dict[str, MCPTypes]] = profile.get("stats")
        self.commandRevision: int = profile.get("commandRevision")

    async def save_profile(self, database: motor.core.AgnosticDatabase) -> None:
        """
        Save the profile

        :param database: The database to use
        """
        collection = database[f"profile_{self.profile_type}"]
        await collection.replace_one({"_id": self.accountId}, self.profile, upsert=True)


class PlayerProfile:
    # noinspection PyUnresolvedReferences
    """
        Class based system to handle the profile management for WEX MCP service

        :param account_id: The account ID of the profile

        :var account_id: The account ID of the profile
        :var profile_revisions: The profile revisions of the profiles
        :var profile0: The profile 0 of the profile
        :var profile0_changes: The profile 0 changes of the profile
        :var profile0_notifications: The profile 0 notifications of the profile
        :var levels: The levels of the profile
        :var levels_changes: The levels changes of the profile
        :var levels_notifications: The levels notifications of the profile
        :var friends: The friends of the profile
        :var friends_changes: The friends changes of the profile
        :var friends_notifications: The friends notifications of the profile
        :var monsterpit: The monsterpit of the profile
        :var monsterpit_changes: The monsterpit changes of the profile
        :var monsterpit_notifications: The monsterpit notifications of the profile
        :var multiplayer: The multiplayer of the profile
        :var multiplayer_changes: The multiplayer changes of the profile
        :var multiplayer_notifications: The multiplayer notifications of the profile
        """

    def __init__(self, account_id: str) -> None:
        """
        Initialise the profile.
        This will load the profile from the res folder and setup the variables
        :param account_id: The account ID of the profile
        """
        self.account_id: str = account_id
        self.profile_revisions: list[
            dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[
                str, str | int]] = []

    def __repr__(self) -> str:
        """
        Return the account ID of the profile
        :return: The account ID of the profile
        """
        return f"<PlayerProfile account_id={self.account_id}>"

    def __str__(self) -> str:
        """
        Return the account ID of the profile
        :return: The account ID of the profile
        """
        return self.__repr__()

    @classmethod
    async def init_profile(cls, account_id: str) -> Self:
        """
        Initialise the profile

        :param account_id: The account ID of the profile to initialise
        :return: The initialised profile
        """
        self: PlayerProfile = cls(account_id)
        await self.load_profiles(account_id)
        return self

    async def load_profiles(self, account_id: str) -> None:
        """
        Load the profiles

        :param account_id: The account ID of the profile to load
        :return: None
        """
        sanic_app = sanic.Sanic.get_app()
        for profile_type in ProfileType:
            mcp_profile: MCPProfile = await MCPProfile.init_profile(account_id, profile_type, sanic_app.ctx.db)
            setattr(self, f"_{profile_type.value}", mcp_profile)
            setattr(self, f"{profile_type.value}_changes", [])
            setattr(self, f"{profile_type.value}_notifications", [])
            self.profile_revisions.append(
                {"profileId": profile_type.value, "clientCommandRevision": mcp_profile.commandRevision})

    async def get_profile(self, profile_id: ProfileType = ProfileType.PROFILE0) -> MCPProfile:
        """
        Get the profile data
        :param profile_id: The profile ID to get
        :return: The profile data
        """
        return getattr(self, f"_{profile_id.value}")

    async def get_item_by_guid(self, guid: str, profile_id: ProfileType = ProfileType.PROFILE0) -> dict:
        """
        Get the item by the GUID
        :param profile_id: The profile ID to get
        :param guid: The GUID of the item
        :return: The item
        """
        if isinstance(guid, list):
            guid: str = guid[0]
        return (await self.get_profile(profile_id)).get("items").get(guid)

    async def find_item_by_template_id(self, template_id: str, profile_id: ProfileType = ProfileType.PROFILE0) -> list:
        """
        Find all items with the specified template ID
        :param template_id: The template ID to search for
        :param profile_id: The profile ID to get
        :return: A list of GUIDs of the items with the specified template ID
        """
        guids: list = []
        for guid, item in (await self.get_profile(profile_id)).get("items").items():
            if item["templateId"] == template_id:
                guids.append(guid)
        return guids

    async def fuzzy_find_item_by_template_id(self, template_id: str,
                                             profile_id: ProfileType = ProfileType.PROFILE0) -> list:
        """
        Find all items with the specified template ID. Not actually fuzzy search, just searches for tID after :
        :param template_id: The template ID to search for
        :param profile_id: The profile ID to get
        :return: A list of GUIDs of the items with the specified template ID
        """
        guids: list = []
        for guid, item in (await self.get_profile(profile_id)).get("items").items():
            if item["templateId"].split(":")[-1] == template_id:
                guids.append(guid)
        return guids

    async def find_items_by_type(self, template_id: str, profile_id: ProfileType = ProfileType.PROFILE0) -> list:
        """
        Find all items with the specified type.
        :param template_id: The template ID to search for
        :param profile_id: The profile ID to get
        :return: A list of GUIDs of the items with the specified template ID
        """
        guids: list = []
        for guid, item in (await self.get_profile(profile_id)).get("items").items():
            if item["templateId"].split(":")[0] == template_id:
                guids.append(guid)
        return guids

    async def get_stat(self, stat_name: str, profile_id: ProfileType = ProfileType.PROFILE0) -> MCPTypes:
        """
        Get the specified stat from the profile
        :param stat_name: The name of the stat to get
        :param profile_id: The profile ID to get
        :return: The value of the stat
        """
        return (await self.get_profile(profile_id)).get("stats").get("attributes").get(stat_name)

    async def modify_stat(self, stat_name: str, new_value: MCPTypes,
                          profile_id: ProfileType = ProfileType.PROFILE0) -> None:
        """
        Modify the specified stat to the new value
        :param stat_name: The name of the stat to modify
        :param new_value: The new value of the stat
        :param profile_id: The ID of the profile to modify
        :raise AttributeError: If the profile ID is invalid
        :return: None
        """
        profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
        profile_changes.append({"changeType": "statModified", "name": stat_name, "value": new_value})
        setattr(self, f"{profile_id.value}_changes", profile_changes)

    async def remove_item(self, item_id: str, profile_id: ProfileType = ProfileType.PROFILE0) -> None:
        """
        Remove the specified item from the profile
        :param item_id: The GUID of the item to remove
        :param profile_id: The ID of the profile to modify
        :raise AttributeError: If the profile ID is invalid
        :return: None
        """
        profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
        profile_changes.append({"changeType": "itemRemoved", "itemId": item_id})
        setattr(self, f"{profile_id.value}_changes", profile_changes)

    async def change_item_attribute(self, item_id: str, attribute_name: str, new_value: MCPTypes,
                                    profile_id: ProfileType = ProfileType.PROFILE0) -> None:
        """
        Change the specified attribute of the specified item to the new value
        :param item_id: The GUID of the item to modify
        :param attribute_name: The name of the attribute to modify
        :param new_value: The new value of the attribute
        :param profile_id: The ID of the profile to modify
        :raise AttributeError: If the profile ID is invalid
        :return: None
        """
        profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
        if new_value is None:
            profile_changes.append({"changeType": "itemAttrChanged", "itemId": item_id, "attributeName": attribute_name})
        else:
            profile_changes.append({"changeType": "itemAttrChanged", "itemId": item_id, "attributeName": attribute_name,
                                    "attributeValue": new_value})
        setattr(self, f"{profile_id.value}_changes", profile_changes)

    async def add_item(self, item_data: dict, item_id: Optional[str] = None,
                       profile_id: ProfileType = ProfileType.PROFILE0) -> str:
        """
        Add the specified item to the profile
        :param item_data: The data of the item to add
        :param item_id: The GUID of the item to add
        :param profile_id: The ID of the profile to modify
        :raise AttributeError: If the profile ID is invalid
        :return: The GUID of the item added
        """
        if item_id is None:
            item_id: str = str(uuid.uuid4())
        profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
        profile_changes.append({"changeType": "itemAdded", "itemId": item_id, "item": item_data})
        setattr(self, f"{profile_id.value}_changes", profile_changes)
        return item_id

    async def change_item_quantity(self, item_id: str, new_quantity: int | float,
                                   profile_id: ProfileType = ProfileType.PROFILE0) -> None:
        """
        Change the quantity of the specified item to the new value
        :param item_id: The GUID of the item to modify
        :param new_quantity: The new quantity of the item
        :param profile_id: The ID of the profile to modify
        :raise AttributeError: If the profile ID is invalid
        :return: None
        """
        profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
        profile_changes.append({"changeType": "itemQuantityChanged", "itemId": item_id, "quantity": new_quantity})
        setattr(self, f"{profile_id.value}_changes", profile_changes)

    async def grant_item(self, template_id: str, quantity: int = 1,
                         attributes: Optional[dict[str, MCPTypes]] = None, unique = False, profile_id: ProfileType = ProfileType.PROFILE0) -> str:
        """
        Grant the specified item to the profile
        :param template_id: The template ID of the item to grant
        :param quantity: The quantity of the item to grant
        :param attributes: The default attributes of the item to grant
        :param unique: Whether a new item should be created if the item already exists
        :param profile_id: The type of profile to modify
        :return: The GUID of the item granted
        """
        # search for the item
        item_guids: list = await self.find_item_by_template_id(template_id, profile_id)
        if item_guids and not unique:
            item_guid: str = item_guids[0]
            item: dict = await self.get_item_by_guid(item_guid, profile_id)
            item["quantity"]: MCPTypes = item["quantity"] + quantity
            await self.change_item_quantity(item_guid, item["quantity"], profile_id)
            return item_guid
        else:
            item_data: dict = {
                "templateId": template_id,
                "attributes": attributes if attributes is not None else {},
                "quantity": quantity
            }
            return await self.add_item(item_data, profile_id=profile_id)

    async def grant_hero(self, template_id: str, gear_weapon_item_id: str = "", weapon_unlocked: bool = False,
                         sidekick_template_id: str = "", level: int = 1, is_new: bool = True, num_sold: int = 0,
                         skill_level: int = 1, sidekick_unlocked: bool = False, upgrades: Optional[list[int]] = None,
                         used_as_sidekick: bool = False, gear_armor_item_id: str = "", skill_xp: int = 0, armor_unlocked: bool = False,
                         foil_lvl: int = -1, xp: int = 0, rank: int = 0, sidekick_item_id: str = "", profile_id: ProfileType = ProfileType.PROFILE0) -> str:
            """
            Grant the specified hero to the profile
            :param template_id: The template ID of the hero to grant
            :param gear_weapon_item_id: The item ID of the weapon to grant
            :param weapon_unlocked: Whether the weapon is unlocked
            :param sidekick_template_id: The template ID of the sidekick to grant
            :param level: The level of the hero
            :param is_new: Whether the hero is new
            :param num_sold: The number of heroes sold
            :param skill_level: The skill level of the hero
            :param sidekick_unlocked: Whether the sidekick is unlocked
            :param upgrades: The upgrades of the hero
            :param used_as_sidekick: Whether the hero is used as a sidekick
            :param gear_armor_item_id: The item ID of the armor to grant
            :param skill_xp: The skill XP of the hero
            :param armor_unlocked: Whether the armor is unlocked
            :param foil_lvl: The foil level of the hero
            :param xp: The XP of the hero
            :param rank: The rank of the hero
            :param sidekick_item_id: The item ID of the sidekick to grant
            :param profile_id: The type of profile to add the hero to
            :return: The GUID of the hero granted
            """
            if upgrades is None:
                upgrades = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            return await self.grant_item(template_id, 1, {
                "gear_weapon_item_id": gear_weapon_item_id,
                "weapon_unlocked": weapon_unlocked,
                "sidekick_template_id": sidekick_template_id,
                "level": level,
                "is_new": is_new,
                "num_sold": num_sold,
                "skill_level": skill_level,
                "sidekick_unlocked": sidekick_unlocked,
                "upgrades": upgrades,
                "used_as_sidekick": used_as_sidekick,
                "gear_armor_item_id": gear_armor_item_id,
                "skill_xp": skill_xp,
                "armor_unlocked": armor_unlocked,
                "foil_lvl": foil_lvl,
                "xp": xp,
                "rank": rank,
                "sidekick_item_id": sidekick_item_id
            }, True, profile_id)

    async def get_notifications(self, profile_id: ProfileType = ProfileType.PROFILE0) -> list[dict]:
        """
        Get the notifications for the current account and profile
        :param profile_id: The ID of the profile to get
        :return: The notifications
        """
        return getattr(self, f"{profile_id.value}_notifications", [])

    async def add_notifications(self, notification: dict, profile_id: ProfileType = ProfileType.PROFILE0) -> list[dict]:
        """
        Adds notifications for the current account and profile
        :param notification: The notification to add to
        :param profile_id: The ID of the profile to add to
        :return: The notifications
        """
        profile_notifications: list = getattr(self, f"{profile_id.value}_notifications", [])
        profile_notifications.append(notification)
        setattr(self, f"{profile_id.value}_notifications", profile_notifications)
        return profile_notifications

    async def clear_notifications(self, profile_id: Optional[ProfileType] = None) -> None:
        """
        Clears notifications for the current account and profile
        :param profile_id: The ID of the profile to clear
        :return: The notifications
        """
        profile_types: "ProfileType" | list[ProfileType] = ProfileType if profile_id is None else [profile_id]

        for p_type in profile_types:
            setattr(self, f"{p_type.value}_notifications", [])

    async def flush_changes(self, profile_type: Optional[ProfileType] = None) -> None:
        """
        Apply all changes to the original profiles.

        :param profile_type: (Optional) Enum of the profile to flush. If None, all profiles will be flushed.
        """
        profile_types: "ProfileType" | list[ProfileType] = ProfileType if profile_type is None else [profile_type]

        for p_type in profile_types:
            profile = await self.get_profile(p_type)
            for change in getattr(self, f"{p_type.value}_changes"):
                change_type = change["changeType"]
                match change_type:
                    case "statModified":
                        profile["stats"]["attributes"][change["name"]]: MCPTypes = change["value"]
                    case "itemRemoved":
                        try:
                            del profile["items"][change["itemId"]]
                        except KeyError:
                            pass
                    case "itemAttrChanged":
                        if change.get("attributeValue") is None:
                            del profile["items"][change["itemId"]]["attributes"][change["attributeName"]]
                        else:
                            profile["items"][change["itemId"]]["attributes"][change["attributeName"]]: \
                                MCPTypes = change["attributeValue"]
                    case "itemAdded":
                        profile["items"][change["itemId"]]: MCPTypes = change["item"]
                    case "itemQuantityChanged":
                        profile["items"][change["itemId"]]["quantity"]: MCPTypes = change["quantity"]
            setattr(self, f"_{p_type.value}", profile)

            # Clear the changes list for this profile
            setattr(self, f"{p_type.value}_changes", [])

    async def add_friend_instance(self, request: sanic.request.Request, friendId: str,
                                  friendStatus: FriendStatus = FriendStatus.FRIEND) -> None:
        """
        Adds / Updates a friend instance for the provided account ID to the current profile
        :param request: The request to add the friend instance to
        :param friendId: The ID of the friend to add
        :param friendStatus: The status of the friend to add
        :return: None
        """
        if friendId not in request.app.ctx.profiles:
            request.app.ctx.profiles[friendId]: PlayerProfile = await PlayerProfile.init_profile(friendId)
        wex_data: dict = await request.app.ctx.profiles[friendId].get_profile(ProfileType.PROFILE0)
        rep_heroes: list = []
        account_perks: list = []
        # TODO: Move to database
        account_data: dict = await request.app.ctx.db["accounts"].find_one({"_id": friendId}, {
            "displayName": 1,
        })
        for account_perk in ["MaxHitPoints", "RegenStat", "PetStrength", "BasicAttack", "Attack", "SpecialAttack",
                             "DamageReduction", "MaxMana"]:
            account_perks.append(wex_data["stats"]["attributes"].get("account_perks").get(account_perk, 0))
        for hero_id in wex_data["stats"]["attributes"].get("rep_hero_ids", []):
            hero_data: dict = await request.app.ctx.profiles[friendId].get_item_by_guid(hero_id)
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
        friend_instance_guids: list[str] = await self.find_item_by_template_id("Friend:Instance", ProfileType.FRIENDS)
        for friend_instance_guid in friend_instance_guids:
            friend_instance: dict[str, MCPTypes] = await self.get_item_by_guid(friend_instance_guid,
                                                                               ProfileType.FRIENDS)
            if friend_instance["attributes"]["accountId"] == account_data["_id"]:
                if friend_instance["attributes"]["status"] == "Suggested" and friendStatus == FriendStatus.REQUESTED:
                    # noinspection PyPep8Naming
                    friendStatus: FriendStatus = FriendStatus.SUGGESTEDREQUEST
                await self.change_item_attribute(friend_instance_guid, "status", friendStatus.value,
                                                 ProfileType.FRIENDS)
                await self.change_item_attribute(friend_instance_guid, "snapshot_expires",
                                                 await format_time(
                                                     datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3)),
                                                 ProfileType.FRIENDS)
                await self.change_item_attribute(friend_instance_guid, "canBeSparred",
                                                 wex_data["stats"]["attributes"].get("is_pvp_unlocked",
                                                                                     False), ProfileType.FRIENDS)
                await self.change_item_attribute(friend_instance_guid, "snapshot", {
                    "displayName": account_data["displayName"],
                    "avatarUrl": "wex-temp-avatar.png",
                    "repHeroes": rep_heroes,
                    "lastPlayTime": wex_data["updated"],
                    "numLevelsCompleted": wex_data["stats"]["attributes"].get("num_levels_completed", 0),
                    "numTerritoriesClaimed": wex_data["stats"]["attributes"].get("num_territories_claimed", 0),
                    "accountLevel": wex_data["stats"]["attributes"].get("level", 0),
                    "numRepHeroes": len(wex_data["stats"]["attributes"].get("rep_hero_ids", [])),
                    "isPvPUnlocked": wex_data["stats"]["attributes"].get("is_pvp_unlocked", False)
                }, ProfileType.FRIENDS)
                return
        await self.add_item({
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
                "remoteFriendId": "",  # TODO: figure out what the hell remotefrendid is supposed to be
                "status": friendStatus.value,
                "gifts": {}
            },
            "quantity": 1
        }, profile_id=ProfileType.FRIENDS)

    async def remove_friend_instance(self, friendId: str) -> None:
        """
        Remove a friend instance from the profile
        :param friendId: The friend ID
        """
        friend_instance_guids: list[str] = await self.find_item_by_template_id("Friend:Instance", ProfileType.FRIENDS)
        for friend_instance_guid in friend_instance_guids:
            friend_instance: dict[str, MCPTypes] = await self.get_item_by_guid(friend_instance_guid,
                                                                               ProfileType.FRIENDS)
            if friend_instance["attributes"]["accountId"] == friendId:
                await self.remove_item(friend_instance_guid, ProfileType.FRIENDS)

    async def construct_response(self, profile_id: ProfileType = ProfileType.PROFILE0, rvn: int = -1,
                                 client_command_revision: Optional[str] = None,
                                 clear_notification: bool = False, clear_all: bool = False) -> dict:
        """
        Construct a response for the specified profile
        :param profile_id: The profile to construct a response for
        :param rvn: The revision number of the profile
        :param client_command_revision: The revision number of the client command
        :param clear_notification: Whether to clear the notifications after constructing the response
        :param clear_all: Whether to clear all notifications
        :return: The response
        """
        from utils.utils import format_time
        if client_command_revision is None:
            client_command_revision: list[
                dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[
                    str, str | int]] = self.profile_revisions
        else:
            client_command_revision: list[
                dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[
                    str, str | int]] = ast.literal_eval(client_command_revision)
        for item in client_command_revision:
            if item["profileId"] == profile_id.value:
                client_revision: int = item["clientCommandRevision"]
                break
        else:
            client_revision: int = -1
        if client_revision <= 0:
            client_revision: int = (await self.get_profile(profile_id))["commandRevision"]
        response: dict[str, int | list | str | list[dict[str, int | list | str | Any]] | Any] = {
            "profileRevision": (await self.get_profile(profile_id))["rvn"],
            "profileId": profile_id.value,
            "profileChangesBaseRevision": (await self.get_profile(profile_id))["rvn"],
            "profileChanges": [],
            "profileCommandRevision": client_revision,
            "serverTime": await format_time(),
            "responseVersion": 1
        }

        if rvn != (await self.get_profile(profile_id))["rvn"]:
            # Full profile update requested
            await self.flush_changes(profile_id)
            response['profileChanges']: list[dict[str, str | dict | int]] = [
                {
                    "changeType": "fullProfileUpdate",
                    "profile": await self.get_profile(profile_id)
                }
            ]
        else:
            # Partial profile update requested
            profile_changes: list = getattr(self, f"{profile_id.value}_changes", [])
            if profile_changes:
                response['profileChanges']: list = profile_changes
                await self.bump_revision(profile_id, response)

        # Check for other profiles with changes
        other_changes: list = []
        for profile in ProfileType:
            if profile == profile_id:
                continue
            profile_changes: list = getattr(self, f"{profile.value}_changes", [])
            if profile_changes:
                profile_notifications: list = getattr(self, f"{profile.value}_notifications", [])
                for item in client_command_revision:
                    if item["profileId"] == profile.value:
                        client_revision: int = item["clientCommandRevision"]
                        break
                else:
                    client_revision: int = -1
                if client_revision <= 0:
                    client_revision: int = (await self.get_profile(profile))["commandRevision"]
                base_rvn: int = (await self.get_profile(profile))["rvn"]
                await self.bump_revision(profile)
                other_changes.append({
                    "profileRevision": (await self.get_profile(profile))["rvn"],
                    "profileId": profile.value,
                    "profileChangesBaseRevision": base_rvn,
                    "profileChanges": profile_changes,
                    "profileCommandRevision": client_revision,
                })
                if profile_notifications:
                    other_changes[-1]["notifications"]: list = profile_notifications

        if other_changes:
            response['multiUpdate']: list = other_changes
        notifications = getattr(self, f"{profile_id.value}_notifications", [])
        if notifications:
            response["notifications"]: list = notifications

        if clear_notification:
            if clear_all:
                for profile in ProfileType:
                    await self.clear_notifications(profile)
            else:
                await self.clear_notifications(profile_id)

        await self.flush_changes()
        await self.save_profile()

        return response

    async def bump_revision(self, profile_id: ProfileType = ProfileType.PROFILE0,
                            response: Optional[dict] = None) -> None:
        """
        Bump the revision of the specified profile
        :param profile_id: The profile to bump the revision of
        :param response: The response to add the revision to
        :return: None
        """
        from utils.utils import format_time
        (await self.get_profile(profile_id))["rvn"] += 1
        (await self.get_profile(profile_id))["updated"] = await format_time()
        (await self.get_profile(profile_id))["commandRevision"] += 1
        if response is not None:
            response["profileRevision"] = (await self.get_profile(profile_id))["rvn"]
            response["profileChangesBaseRevision"] = (await self.get_profile(profile_id))["rvn"] - 1
            response["profileCommandRevision"] = (await self.get_profile(profile_id))["commandRevision"]
        for i, client_revision in enumerate(self.profile_revisions):
            if client_revision["profileId"] == profile_id.value:
                self.profile_revisions[i]["clientCommandRevision"] += 1
                break

    async def save_profile(self) -> None:
        """
        Save the modified profiles to disk
        :return: None
        """
        save_profile: bool = False
        if save_profile:
            for profile_type in ProfileType:
                profile = await self.get_profile(profile_type)
                await profile.save_profile(sanic.Sanic.get_app().ctx.db)
