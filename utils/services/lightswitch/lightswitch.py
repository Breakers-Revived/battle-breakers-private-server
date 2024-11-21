"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based system to handle the lightswitch service
"""
import datetime

import motor.core
import sanic
from typing_extensions import Any, Optional, Self

from utils.enums import ServerStatus


class LightswitchService:
    """
    Class based system to handle the lightswitch service
    """

    def __init__(self) -> None:
        """
        Initialise the lightswitch class.
        This will setup the variables for the lightswitch service
        """
        self.status: ServerStatus = ServerStatus.UP
        self.message: str = "Battle Breakers is back :D"
        self.maintenance_uri: Optional[str] = None
        self.downtime_start: Optional[datetime.datetime] = None
        self.downtime_end: Optional[datetime.datetime] = None

    def __repr__(self) -> str:
        """
        Get the representation of the lightswitch class
        :return: The representation of the lightswitch class
        """
        return f"<LightswitchService status={self.status} message={self.message} downtime_start={self.downtime_start} downtime_end={self.downtime_end}>"

    def __str__(self) -> str:
        """
        Get the string of the lightswitch class
        :return: The string of the lightswitch class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the lightswitch class
        :return: The dictionary of the lightswitch class
        """
        time_to_shutdown_in_ms = -1
        if self.downtime_start is not None:
            time_to_shutdown_in_ms = (self.downtime_start - datetime.datetime.now(datetime.UTC)).total_seconds() * 1000
            if self.downtime_end is not None and datetime.datetime.now(datetime.UTC) > self.downtime_end:
                time_to_shutdown_in_ms = -1
        return {
            "status": self.status.value,
            "message": self.message,
            "maintenance_uri": self.maintenance_uri,
            "timeToShutdownInMs": time_to_shutdown_in_ms
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the lightswitch class
        :param key: The key to get the value of
        :return: The value of the key in the lightswitch class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the lightswitch class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the lightswitch class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the lightswitch class
        :param key: The key to delete
        :return: The value of the key in the lightswitch class
        """
        delattr(self, key)

    @classmethod
    async def init_lightswitch(cls, database: motor.core.AgnosticDatabase) -> Self:
        """
        Initialise the lightswitch class
        :return: The initialised lightswitch class
        """
        self: LightswitchService = cls()
        lightswitch_db = await database["admin"].find_one({"_id": "lightswitch"})
        if lightswitch_db is not None:
            self.status = ServerStatus(lightswitch_db["status"])
            self.message = lightswitch_db["message"]
            self.maintenance_uri = lightswitch_db.get("maintenance_uri")
            self.downtime_start = lightswitch_db.get("downtime_start")
            self.downtime_end = lightswitch_db.get("downtime_end")
        return self

    async def refresh_status(self) -> dict[str, Any]:
        """
        Update the lightswitch server status based on downtime start and end if applicable
        :return: The lightswitch status, message, and time to shutdown in milliseconds
        """
        if self.downtime_start is not None:
            if self.downtime_start > datetime.datetime.now(datetime.UTC):
                self.status = ServerStatus.UP
                self.message = "Battle Breakers is back :D"
            else:
                self.status = ServerStatus.DOWN
                self.message = "Battle Breakers is down for maintenance :("
        if self.downtime_end is not None:
            if self.downtime_end < datetime.datetime.now(datetime.UTC):
                self.status = ServerStatus.UP
                self.message = "Battle Breakers is back :D"
            else:
                self.status = ServerStatus.DOWN
                self.message = "Battle Breakers is down for maintenance :("
        return self.__dict__()

    async def save_lightswitch(self) -> None:
        """
        Save the lightswitch server status into the db
        :return: None
        """
        collection = sanic.Sanic.get_app().ctx.db["admin"]
        await collection.update_one({"_id": "lightswitch"}, {"$set": self.__dict__()}, upsert=True)
