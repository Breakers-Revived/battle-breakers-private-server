"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the enums
"""

import enum

from utils.exceptions import errors


class ProfileType(enum.Enum):
    """
    Enum for the profile types

    Attributes:
        PROFILE0: The profile ID for the profile0 profile
        LEVELS: The profile ID for the levels profile
        FRIENDS: The profile ID for the friends profile
        MONSTERPIT: The profile ID for the monsterpit profile
        MULTIPLAYER: The profile ID for the multiplayer profile

    Methods:
        from_string(cls, s: str) -> "ProfileType":
            Get the profile ID from the string
    """
    PROFILE0: str = "profile0"
    LEVELS: str = "levels"
    FRIENDS: str = "friends"
    MONSTERPIT: str = "monsterpit"
    MULTIPLAYER: str = "multiplayer"

    @classmethod
    def from_string(cls, s: str) -> "ProfileType":
        """
        Get the profile ID from the string
        :param s: The string to get the profile ID from
        :return: The profile ID
        :raises: errors.com.epicgames.modules.profile.invalid_profile_id_param: Raised if the profile ID is invalid
        """
        try:
            return cls[s.upper()]
        except KeyError:
            raise errors.com.epicgames.modules.profile.invalid_profile_id_param()


class FriendStatus(enum.Enum):
    """
    Enum for the different friend statuses in a WEX Profile

    Attributes:
        NONE: No friend status
        SUGGESTED: Suggested friend
        REQUESTED: Outgoing friend request
        INVITED: Incoming friend request
        FRIEND: Normal friend
        EPICFRIEND: Epic friend (1.80+)
        EPICNONPLATFORMFRIEND: Epic friend on a different platform
        PLATFORMONLYFRIEND: Friend on a different platform
        SUGGESTEDREQUEST: Suggested friend request sent
        SUGGESTEDLEGACY: Suggested friend from legacy
        NOTPLAYING: Not playing
        PLATFORMNOTPLAYING: Not playing on a different platform
        MAXNONE: Max friends reached

    Methods:
        from_string(cls, s: str) -> "FriendStatus":
            Get the friend status from a string
    """
    NONE: str = "None"
    SUGGESTED: str = "Suggested"
    REQUESTED: str = "Requested"
    INVITED: str = "Invited"
    FRIEND: str = "Friend"
    EPICFRIEND: str = "EpicFriend"
    EPICNONPLATFORMFRIEND: str = "EpicNonPlatformFriend"
    PLATFORMONLYFRIEND: str = "PlatformOnlyFriend"
    SUGGESTEDREQUEST: str = "SuggestedRequest"
    SUGGESTEDLEGACY: str = "SuggestedLegacy"
    NOTPLAYING: str = "NotPlaying"
    PLATFORMNOTPLAYING: str = "PlatformNotPlaying"
    MAXNONE: str = "Max_None"

    @classmethod
    def from_string(cls, s: str) -> "FriendStatus":
        """
        Get the friend status from a string
        :param s: The string to get the friend status from
        :return: The friend status
        """
        return cls[s.upper()]


class Permission(enum.Enum):
    """
    Enum for the different account permissions

    Attributes:
        NONE: No permissions
        CREATE: Create permissions
        READ: Read permissions
        CREATE_READ: Create and read permissions
        UPDATE: Update permissions
        CREATE_DELETE: Create and delete permissions
        READ_UPDATE: Read and update permissions
        CREATE_READ_UPDATE: Create, read, and update permissions
        DELETE: Delete permissions
        CREATE_DELETE_READ: Create, delete, and read permissions
        CREATE_DELETE_UPDATE: Create, delete, and update permissions
        CREATE_READ_DELETE: Create, read, and delete permissions
        CREATE_READ_UPDATE_DELETE: Create, read, update, and delete permissions
        READ_DELETE: Read and delete permissions
        READ_UPDATE_DELETE: Read, update, and delete permissions
        ALL: All permissions
        DENY: Deny permissions

    Methods:
        from_int(cls, i: int) -> "Permission":
            Get the permission from the integer
    """
    NONE = 0
    CREATE = 1
    READ = 2
    CREATE_READ = 3
    UPDATE = 4
    CREATE_DELETE = 5
    READ_UPDATE = 6
    CREATE_READ_UPDATE = 7
    DELETE = 8
    CREATE_DELETE_READ = 9  #
    CREATE_DELETE_UPDATE = 10  #
    CREATE_READ_DELETE = 11
    CREATE_READ_UPDATE_DELETE = 12  #
    READ_DELETE = 13  #
    READ_UPDATE_DELETE = 14
    ALL = 15
    DENY = 16

    @classmethod
    def from_int(cls, i: int) -> "Permission":
        """
        Get the permission from the integer
        :param i: The integer to get the permission from
        :return: The permission
        """
        return cls(i)


class AuthClient(enum.Enum):
    """
    Enum for the different authentication clients

    Attributes:
        wexPCGameClient: The Battle Breakers PC game client
        wexPCGameClient_GameDev: The Battle Breakers PC game client for GameDev environment
        wexAndroidGameClient: The Battle Breakers Android game client
        wexAndroidGameClient_GameDev: The Battle Breakers Android game client for GameDev environment
        wexIOSGameClient: The Battle Breakers iOS game client
        wexpClient: The Battle Breakers old mobile client
        wexpClient_GameDev: The Battle Breakers old mobile client for GameDev environment
        battlebreakers_web: The Battle Breakers website
        launcherAppClient2: The Epic Games Launcher
        googleClientId: The Google client ID
        googleClientId_new: The new reversed Google client ID

    Methods:
        from_string(cls, s: str) -> "AuthClient":
            Get the authentication client from a string
    """
    wexPCGameClient = ["3cf78cd3b00b439a8755a878b160c7ad", "b383e0f4-f0cc-4d14-99e3-813c33fc1e9d"]
    wexPCGameClient_GameDev = ["84cd036b576541e9ad1634c1448c0c30", "6b2a4df2-20f5-4297-953c-6bb3e01a9700"]
    wexAndroidGameClient = ["e645e4b96298419cbffbfa353ebf8b82", "d03089fd-628a-448a-ac39-0e8c5b022a11"]
    wexAndroidGameClient_GameDev = ["66e03bfeb7db44adaca611dae2674094", "6870a624-efdb-404b-8927-383fb92b5d08"]
    wexIOSGameClient = ["ec813099a59f48d4a338f1901c1609db", "72f6db62-0e3e-4439-97df-ee21f7b0ae94"]
    wexIOSGameClient_GameDev = ["016a103319b34d258c0e7d4d2760c985", "63f3acc5-7698-45a1-a6c4-4e7c99703b43"]
    wexpClient = ["f8eac541a1c241939f76d26cf2a673a6", "80f5551f151840ca9f52e2e14581a742"]
    wexpClient_GameDev = ["f8eac541a1c241939f76d26cf2a673a6", "cc545e608de846a18e75a36acc1cf3d0"]
    battlebreakers_web = ["8e873617d81d4caf89bae28a4b74bbfe", "d1d8b2a0-4b0a-4f4e-9f4a-3b3b7b0b0b0b"]
    launcherAppClient2 = ["34a02cf8f4414e29b15921876da36f9a", "daafbccc737745039dffe53d94fc76cf"]
    googleClientId = ["26523943714-k0ekuoist4nb0br1ngq0erv4eaq11u10.apps.googleusercontent.com",
                      "QSzqBOVSk_OA5zNk6XjIdj6Q"]
    googleClientId_new = ["com.googleusercontent.apps.26523943714-vcoht7h19fr69impmedkl8996scv78i0",
                          "QSzqBOVSk_OA5zNk6XjIdj6Q"]

    @classmethod
    def from_string(cls, s: str) -> list["AuthClient"]:
        """
        Get the authentication client secret pair from a client string
        :param s: The string to get the authentication client from
        :return: The authentication client secret pair
        """
        clients = []
        for client in cls:
            if s in client.value[0]:
                clients.append(client)
        if clients:
            return clients
        else:
            raise errors.com.epicgames.common.oauth.invalid_client()


class AccountPerk(enum.Enum):
    """
    Enum for the different account perks

    Attributes:
        MaxMana: The max mana perk
        MaxHitPoints: The max hit points perk
        Attack: The attack perk
        DamageReduction: The damage reduction perk
        RegenStat: The regen stat perk
        PetStrength: The pet strength perk
        BasicAttack: The basic attack perk
        SpecialAttack: The special attack perk

    Methods:
        from_string(cls, s: str) -> "AccountPerk":
            Get the account perk from a string
    """
    MaxMana = "MaxMana"
    MaxHitPoints = "MaxHitPoints"
    Attack = "Attack"
    DamageReduction = "DamageReduction"
    RegenStat = "RegenStat"
    PetStrength = "PetStrength"
    BasicAttack = "BasicAttack"
    SpecialAttack = "SpecialAttack"

    @classmethod
    def from_string(cls, s: str) -> "AccountPerk":
        """
        Get the account perk from a string
        :param s: The string to get the account perk from
        :return: The account perk
        """
        return cls[s.split("::")[1]]
