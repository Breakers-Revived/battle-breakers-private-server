"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based system to handle the calendar services
"""
import datetime
from typing_extensions import Any, Optional, Self

import utils.services.calendar.channels as channels


class ScheduledEvents:
    """
    Class based system to handle the calendar services
    """

    def __init__(self) -> None:
        """
        Initialise the scheduled events class.
        This will set up the variables for the calendar
        """
        self.updated: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.news: Optional[channels.News] = None
        self.limited_time_mode: Optional[channels.LimitedTimeMode] = None
        self.marketing: Optional[channels.Marketing] = None
        self.rotational_content: Optional[channels.RotationalContent] = None
        self.featured_stores_mcp: Optional[channels.FeaturedStoresMcp] = None
        self.weekly_challenge: Optional[channels.WeeklyChallenge] = None
        self.battlepass: Optional[channels.BattlePass] = None

    def __repr__(self) -> str:
        """
        Get the representation of the ScheduledEvents class
        :return: The representation of the ScheduledEvents class
        """
        return f"<ScheduledEvents>"

    def __str__(self) -> str:
        """
        Get the string of the ScheduledEvents class
        :return: The string of the ScheduledEvents class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the ScheduledEvents class
        :return: The dictionary of the ScheduledEvents class
        """
        return {
            "news": self.news.__dict__(),
            "limited-time-mode": self.limited_time_mode.__dict__(),
            "marketing": self.marketing.__dict__(),
            "rotational-content": self.rotational_content.__dict__(),
            "featured-stores-mcp": self.featured_stores_mcp.__dict__(),
            "weekly-challenge": self.weekly_challenge.__dict__(),
            "battlepass": self.battlepass.__dict__()
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the ScheduledEvents class
        :param key: The key to get the value of
        :return: The value of the key in the ScheduledEvents class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the ScheduledEvents class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the ScheduledEvents class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the ScheduledEvents class
        :param key: The key to delete
        :return: The value of the key in the ScheduledEvents class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the ScheduledEvents
        :return: The length of the ScheduledEvents
        """
        return len(self.__dict__())

    @classmethod
    async def init_calendar(cls) -> Self:
        """
        Initialise the calendar
        :return: The initialised calendar class
        """
        self: ScheduledEvents = cls()
        await self.setup_calendar()
        return self

    async def setup_calendar(self) -> None:
        """
        Set up the calendar
        :return: None
        """
        self.news: channels.News = channels.News()
        self.limited_time_mode: channels.LimitedTimeMode = channels.LimitedTimeMode()
        self.marketing: channels.Marketing = channels.Marketing()
        self.rotational_content: channels.RotationalContent = channels.RotationalContent()
        self.featured_stores_mcp: channels.FeaturedStoresMcp = channels.FeaturedStoresMcp()
        self.weekly_challenge: channels.WeeklyChallenge = channels.WeeklyChallenge()
        self.battlepass: channels.BattlePass = channels.BattlePass()
        await self.update_all_events()

    async def update_all_events(self) -> None:
        """
        Update the events in the ScheduledEvents class
        :return: None
        """
        self.updated = datetime.datetime.now(datetime.UTC)
        await self.news.update_events()
        await self.limited_time_mode.update_events()
        await self.marketing.update_events()
        await self.rotational_content.update_events()
        await self.featured_stores_mcp.update_events()
        await self.weekly_challenge.update_events()
        await self.battlepass.update_events()

    async def update_required_events(self) -> dict[str, Any]:
        """
        Updates any events that have their cache expired
        :return: None
        """
        if self.news.cache_expired():
            await self.news.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.limited_time_mode.cache_expired():
            await self.limited_time_mode.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.marketing.cache_expired():
            await self.marketing.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.rotational_content.cache_expired():
            await self.rotational_content.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.featured_stores_mcp.cache_expired():
            await self.featured_stores_mcp.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.weekly_challenge.cache_expired():
            await self.weekly_challenge.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        if self.battlepass.cache_expired():
            await self.battlepass.update_events()
            self.updated = datetime.datetime.now(datetime.UTC)
        return self.__dict__()
