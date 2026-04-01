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
    # TODO: hide/replace final level loot that only exists in newer versions to prevent crashes
    # for client <= 1.2, the onboarding level counts as a completed level, and the game cant be played further without this level counting
    if client_version < 3571999:
        if response_data.get("profileId") == "profile0" and response_data.get("profileChanges", [])[0].get("changeType") == "fullProfileUpdate":
            if response_data["profileChanges"][0].get("profile", {}).get("stats", {}).get("attributes", {}).get("num_levels_completed") is not None:
                response_data["profileChanges"][0]["profile"]["stats"]["attributes"]["num_levels_completed"] = min(
                    response_data["profileChanges"][0]["profile"]["stats"]["attributes"]["num_levels_completed"] + 1, 999)
                sanic.log.logger.debug(f"Applied onboarding level polyfill for client version {client_version}")
    return response_data
