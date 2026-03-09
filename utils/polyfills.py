"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles polyfills to improve compatibility with older clients by altering the response without needing to alter server sided profile data handling
"""
import sanic.log

async def profile_polyfill(response_data: dict, client_version: int) -> dict:
    """
    This function is used to alter the final response data on an mcp profile request for older clients

    :param response_data: The original response data
    :param client_version: The version of the client making the request
    :return: The modified response data
    """
    # for client < 1.1, the onboarding level counts as a completed level, and the game cant be played further without this level counting
    if client_version < 3296093:
        if response_data.get("profileId") == "profile0":
            if response_data["profileChanges"].get("profile", {}).get("stats", {}).get("num_levels_completed"):
                response_data["profileChanges"]["profile"]["stats"]["num_levels_completed"] = min(
                    response_data["profileChanges"]["profile"]["stats"]["num_levels_completed"] + 1, 999)
                sanic.log.logger.debug(f"Applied onboarding level polyfill for client version {client_version}")
    return response_data
