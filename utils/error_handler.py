"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Error handler module for the server
"""
from .exceptions import EpicException
from .error_details import error_details

import uuid
import sanic
from sanic.handlers import ErrorHandler


class CustomErrorHandler(ErrorHandler):
    """
    Custom error handler to handle all exceptions
    """

    def default(self, request: sanic.request.Request,
                exception: sanic.exceptions.SanicException | EpicException | Exception) -> sanic.response.JSONResponse:
        """
        Handles all exceptions
        :param request: The request object
        :param exception: The exception object
        :return: The response
        """
        # TODO: clear profile changes on operation error
        if isinstance(exception, EpicException):
            exception_dict = exception.as_dict()
            status_code = getattr(exception, "statusCode", 500)
            headers = {
                "X-Epic-Error-Code": exception_dict["numericErrorCode"],
                "X-Epic-Error-Name": exception_dict["errorCode"],
            }
            ErrorHandler.log(request, exception)
            # if request.app.debug:
            #     exception_dict["errorMessage"] += f" ({exception.__class__.__name__})"
            return sanic.response.json(exception_dict, status=status_code, headers=headers)
        else:
            ErrorHandler.log(request, exception)
            status_code = getattr(exception, "status_code", 500)
            message_vars = []
            for var in getattr(exception, "args", []):
                message_vars.append(var)
            error = error_details.get(status_code, {
                "error_code": "errors.com.epicgames.unknown_error.v2",
                "error_message": "An unknown error has occurred, please report to admin. 🗿",
                "numeric_error_code": 0
            })
            error_code = error["error_code"]
            error_message = error["error_message"]
            numeric_error_code = error["numeric_error_code"]
            if getattr(exception, "context", None) is not None:
                error_code = exception.context.get("errorCode", error_code)
                error_message = exception.context.get("errorMessage", error_message)
                numeric_error_code = exception.context.get("numericErrorCode", numeric_error_code)
            if request.app.debug:
                if status_code == 500:
                    error_message = ""
                    for message in message_vars:
                        error_message += f"{message}"
                error_message += f" ({exception.__class__.__name__})"
            if isinstance(exception, Exception) and "pymongo" in exception.__class__.__module__:
                error_code = "errors.com.epicgames.common.mongo_execution_timeout_error"
                error_message = "Sorry, there was a timeout utilizing the database."
                numeric_error_code = 1045
                ErrorHandler.log(request, exception)
            # TODO: better pydantic validation error handling
            headers = {
                "X-Epic-Error-Code": numeric_error_code,
                "X-Epic-Error-Name": error_code,
            }
            return sanic.response.json({
                "errorCode": error_code,
                "errorMessage": error_message,
                "messageVars": message_vars,
                "numericErrorCode": numeric_error_code,
                "originatingService": "WEX",
                "intent": "prod",
                "trackingId": uuid.uuid4().__str__(),
                "errorDescription": error_message,
                "errorName": error_code.split(".")[-1],
            }, status_code, headers)
