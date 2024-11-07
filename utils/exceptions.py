"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Error exceptions class for formatting error responses
"""
from typing_extensions import Any


class EpicException(Exception):
    """
    The base exception class for all Epic exceptions

    :param args: The arguments to format the error message with
    :param kwargs: The keyword arguments to set as attributes

    :ivar errorCode: The error code
    :ivar errorMessage: The error message
    :ivar messageVars: The message variables
    :ivar numericErrorCode: The numeric error code
    :ivar originatingService: The originating service
    :ivar intent: The intent
    :ivar trackingId: The tracking ID
    :ivar statusCode: The status code
    :ivar error_description: The error description
    :ivar error: The error
    :ivar validationFailures: The validation failures

    :ivar _quiet: Whether to log the exception or not

    :raises: None

    :return: The formatted error response
    """

    _quiet: bool = True

    errorCode: str = None
    errorMessage: str = None
    messageVars: list = []
    numericErrorCode: int = 0
    originatingService: str = None
    intent: str = "prod"
    trackingId: str = None
    statusCode: int = 400
    error_description: str = None
    error: str = None
    validationFailures: dict[str, dict[str, str | dict[str, str]]] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialises the EpicException class
        :param args: Arguments to format the error message with
        :param kwargs: Keyword arguments to set as attributes

        :ivar errorCode: The error code
        :ivar errorMessage: The error message
        :ivar messageVars: The message variables
        :ivar numericErrorCode: The numeric error code
        :ivar originatingService: The originating service
        :ivar intent: The intent
        :ivar trackingId: The tracking ID
        :ivar statusCode: The status code
        :ivar error_description: The error description
        :ivar error: The error
        :ivar validationFailures: The validation failures

        :raises: None

        :return: None
        """
        if self.errorCode is None:
            self.errorCode: str = self.__class__.__qualname__
        for key, value in kwargs.items():
            setattr(self, key, value)
        if args:
            self.errorMessage: str = self.errorMessage.format(*args)
        if self.errorMessage:
            self.messageVars: list = list(args)
        if self.error is None:
            self.error: str = type(self).__name__
        self.error_description: str = self.errorMessage
        super().__init__(self.errorMessage)

    # noinspection IncorrectFormatting
    def __dict__(self) -> dict[str, str | int | list | dict[str, str | dict[str, str]]]:
        """
        Returns the exception as a dictionary

        :raises: None

        :return: The exception as a dictionary
        """
        error: dict = {}
        for cls in reversed(self.__class__.__mro__):
            for attr, value in cls.__dict__.items():
                if not callable(getattr(self, attr)) and getattr(self, attr, None) is not None and not attr.startswith(
                        "_") and attr not in ["args", "quiet"]:
                    error[attr]: str | int | list | dict = getattr(self, attr)
        return error

    def __repr__(self) -> str:
        """
        Returns the exception as a string
        :return: <__class__.__name__ errorCode= errorMessage= numericErrorCode=>
        """
        return f"<{self.__class__.__name__} errorCode={self.errorCode} errorMessage={self.errorMessage} " \
               f"numericErrorCode={self.numericErrorCode}>"

    def __str__(self) -> str:
        """
        Returns the exception as a string
        :return: <__class__.__name__ errorCode= errorMessage= numericErrorCode=>
        """
        return self.__repr__()

    def as_dict(self) -> dict[str, str | int | list | dict[str, str | dict[str, str]]]:
        """
        Returns the exception as a dictionary

        :raises: None

        :return: The exception, formatted for an error json response
        """
        return self.__dict__()

    @property
    def quiet(self) -> bool:
        """
        Returns whether the exception should be quiet or not
        If the exception is quiet, it will not be logged to the console

        :return: Quiet exception or not
        """
        return self._quiet


# noinspection PyPep8Naming
class errors:
    """
    Parent class for all error classes
    """

    class com:
        """
        Parent class for all error classes
        """

        class epicgames(EpicException):
            """
            Parent class for all Epic Games error classes
            """
            errorCode: str = "errors.com.epicgames."
            errorMessage: str = "There was an error"

            class account:
                """
                Parent class for all account errors
                """

                class account_age_verification_incomplete(EpicException):
                    """
                    This error is thrown when the account needs to have the age verified, but it has not been completed
                    *errors.com.epicgames.account.account_age_verification_incomplete*
                    """
                    errorMessage: str = "Age verification incomplete"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_created_but_banned(EpicException):
                    """
                    This error is thrown when the account has been created, but it has been banned
                    *errors.com.epicgames.account.account_created_but_banned*
                    """
                    errorMessage: str = "Account created but banned"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_creation_disabled(EpicException):
                    """
                    This error is thrown when the account creation has been disabled
                    *errors.com.epicgames.account.account_creation_disabled*
                    """
                    errorMessage: str = "Account creation disabled"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_locked(EpicException):
                    """
                    This error is thrown when the account has been locked
                    *errors.com.epicgames.account.account_locked*
                    """
                    errorMessage: str = "Account locked"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_locked_for_update(EpicException):
                    """
                    This error is thrown when the account has been locked for update
                    *errors.com.epicgames.account.account_locked_for_update*
                    """
                    errorMessage: str = "Account locked for update"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_not_active(EpicException):
                    """
                    This error is thrown when the account is disabled
                    *errors.com.epicgames.account.account_not_active*
                    """
                    errorMessage: str = "Sorry the account you are using is not active."
                    numericErrorCode: int = 18006
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 401

                class account_not_found(EpicException):
                    """
                    This error is thrown when the account is not found
                    *errors.com.epicgames.account.account_not_found*

                    Message Vars:
                     - Display Name (Epic User)
                    """
                    errorMessage: str = "Sorry, we couldn't find an account for {0}. Have an account to import? " \
                                        "Get in touch with us on Discord!"
                    numericErrorCode: int = 18007
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 404

                class account_permission_not_found(EpicException):
                    """
                    This error is thrown when the account permission is not found
                    *errors.com.epicgames.account.account_permission_not_found*
                    """
                    errorMessage: str = "Account permission not found"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class account_updated_but_banned(EpicException):
                    """
                    This error is thrown when the account has been updated, but it has been banned
                    *errors.com.epicgames.account.account_updated_but_banned*
                    """
                    errorMessage: str = "Account updated but banned"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class address:
                    """
                    Parent class for all account address errors
                    """

                    class address_not_found(EpicException):
                        """
                        This error is thrown when the account address is not found
                        *errors.com.epicgames.account.address.address_not_found*
                        """
                        errorMessage: str = "Address not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class auth_app:
                    """
                    Parent class for all account authentication app errors
                    """

                    class bad_definition_format(EpicException):
                        """
                        This error is thrown when the account authentication app definition is bad
                        *errors.com.epicgames.account.auth_app.bad_definition_format*
                        """
                        errorMessage: str = "Bad definition format"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class internal_client_forbidden(EpicException):
                        """
                        This error is thrown when the account authentication app internal client is forbidden
                        *errors.com.epicgames.account.auth_app.internal_client_forbidden*
                        """
                        errorMessage: str = "Internal client forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class not_authorized_for_account(EpicException):
                        """
                        This error is thrown when the account authentication app is not authorized for the account
                        *errors.com.epicgames.account.auth_app.not_authorized_for_account*
                        """
                        errorMessage: str = "Not authorized for account"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class auth_token:
                    """
                    Parent class for all account authentication token errors
                    """

                    class invalid_access_token(EpicException):
                        """
                        This error is thrown when the account authentication token access is invalid
                        *errors.com.epicgames.account.auth_token.invalid_access_token*
                        """
                        errorMessage: str = "Invalid access token"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_platform_token(EpicException):
                        """
                        This error is thrown when the account authentication token platform is invalid
                        *errors.com.epicgames.account.auth_token.invalid_platform_token*
                        """
                        errorMessage: str = "Invalid platform token"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_refresh_token(EpicException):
                        """
                        This error is thrown when the account authentication token refresh is invalid
                        *errors.com.epicgames.account.auth_token.invalid_refresh_token*
                        """
                        errorMessage: str = "Sorry, your refresh token is invalid. Please log in again."
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 401

                    class not_own_session_removal(EpicException):
                        """
                        This error is thrown when the account authentication token session is not owned by the removal
                        *errors.com.epicgames.account.auth_token.not_own_session_removal*
                        """
                        errorMessage: str = "Not own session removal"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class unknown_oauth_session(EpicException):
                        """
                        This error is thrown when the account authentication token oauth session is unknown
                        *errors.com.epicgames.account.auth_token.unknown_oauth_session*
                        """
                        errorMessage: str = "Unknown oauth session"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class unknown_oauth_session_refresh(EpicException):
                        """
                        This error is thrown when the account authentication token oauth session refresh is unknown
                        *errors.com.epicgames.account.auth_token.unknown_oauth_session_refresh*
                        """
                        errorMessage: str = "Unknown oauth session refresh"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class banned_by_whitelist_entry(EpicException):
                    """
                    This error is thrown when the account has been banned by a whitelist entry
                    *errors.com.epicgames.account.banned_by_whitelist_entry*
                    """
                    errorMessage: str = "Banned by whitelist entry"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class bulk_pwd_max_items_limit(EpicException):
                    """
                    This error is thrown when the account bulk password max items limit is reached
                    *errors.com.epicgames.account.bulk_pwd_max_items_limit*
                    """
                    errorMessage: str = "Bulk password max items limit"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class cannot_change_account_status(EpicException):
                    """
                    This error is thrown when the account cannot change status
                    *errors.com.epicgames.account.cannot_change_account_status*
                    """
                    errorMessage: str = "Cannot change account status"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class client:
                    """
                    Parent class for all account client errors
                    """

                    class client_permission_not_found(EpicException):
                        """
                        This error is thrown when the account client permission is not found
                        """
                        errorMessage: str = "Client permission not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class client_secret_limit_exceeded(EpicException):
                        """
                        This error is thrown when the account client secret limit is exceeded
                        *errors.com.epicgames.account.client.client_secret_limit_exceeded*
                        """
                        errorMessage: str = "Client secret limit exceeded"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class client_secret_not_found(EpicException):
                        """
                        This error is thrown when the account client secret is not found
                        *errors.com.epicgames.account.client.client_secret_not_found*
                        """
                        errorMessage: str = "Client secret not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class duplicate_client(EpicException):
                        """
                        This error is thrown when the account client is a duplicate
                        *errors.com.epicgames.account.client.duplicate_client*
                        """
                        errorMessage: str = "Duplicate client"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class duplicate_client_permission(EpicException):
                        """
                        This error is thrown when the account client permission is a duplicate
                        *errors.com.epicgames.account.client.duplicate_client_permission*
                        """
                        errorMessage: str = "Duplicate client permission"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class duplicate_client_permissions(EpicException):
                        """
                        This error is thrown when the account client permissions are a duplicate
                        *errors.com.epicgames.account.client.duplicate_client_permissions*
                        """
                        errorMessage: str = "Duplicate client permissions"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class unknown_client(EpicException):
                        """
                        This error is thrown when the account client is unknown
                        *errors.com.epicgames.account.client.unknown_client*
                        """
                        errorMessage: str = "Unknown client"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class client_disabled(EpicException):
                    """
                    This error is thrown when the account client is disabled
                    *errors.com.epicgames.account.client_disabled*
                    """
                    errorMessage: str = "Sorry the client you are using has been disabled"
                    numericErrorCode: int = 18014
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class client_locked_for_update(EpicException):
                    """
                    This error is thrown when the account client is locked for update
                    *errors.com.epicgames.account.client_locked_for_update*
                    """
                    errorMessage: str = "Client locked for update"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class client_missing_redirect_url(EpicException):
                    """
                    This error is thrown when the account client is missing a redirect url
                    *errors.com.epicgames.account.client_missing_redirect_url*
                    """
                    errorMessage: str = "Client missing redirect url"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class country_unchanged(EpicException):
                    """
                    This error is thrown when the account country is unchanged
                    *errors.com.epicgames.account.country_unchanged*
                    """
                    errorMessage: str = "Country unchanged"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class device_auth:
                    """
                    Parent class for all account device auth errors
                    """

                    class disabled(EpicException):
                        """
                        This error is thrown when an account device auth is disabled
                        *errors.com.epicgames.account.device_auth.disabled*
                        """
                        errorMessage: str = "Device auth disabled"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_device_info(EpicException):
                        """
                        This error is thrown when an account device auth has invalid device info
                        *errors.com.epicgames.account.device_auth.invalid_device_info*
                        """
                        errorMessage: str = "Invalid device info JSON value"
                        numericErrorCode: int = 18130
                        originatingService: str = "com.epicgames.account.public"

                class display_name_already_set(EpicException):
                    """
                    This error is thrown when the account display name is already set
                    *errors.com.epicgames.account.display_name_already_set*
                    """
                    errorMessage: str = "Display name already set"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class display_name_change_timeframe(EpicException):
                    """
                    This error is thrown when the account display name change timeframe is invalid
                    *errors.com.epicgames.account.display_name_change_timeframe*
                    """
                    errorMessage: str = "Display name change timeframe invalid"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class display_name_was_used(EpicException):
                    """
                    This error is thrown when the account display name was used
                    *errors.com.epicgames.account.display_name_was_used*
                    """
                    errorMessage: str = "Display name was used"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class duplicate_account_permission(EpicException):
                    """
                    This error is thrown when the account permission is a duplicate
                    *errors.com.epicgames.account.duplicate_account_permission*
                    """
                    errorMessage: str = "Duplicate account permission"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class duplicate_display_name(EpicException):
                    """
                    This error is thrown when the account display name is a duplicate
                    *errors.com.epicgames.account.duplicate_display_name*
                    """
                    errorMessage: str = "This Name is already taken."
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class duplicate_email(EpicException):
                    """
                    This error is thrown when the account email is a duplicate
                    *errors.com.epicgames.account.duplicate_email*
                    """
                    errorMessage: str = "This email is already taken."
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class duplicate_external_auth_type(EpicException):
                    """
                    This error is thrown when the account external auth type is a duplicate
                    *errors.com.epicgames.account.duplicate_external_auth_type*
                    """
                    errorMessage: str = "Duplicate external auth type"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class duplicate_username(EpicException):
                    """
                    This error is thrown when the account username is a duplicate
                    *errors.com.epicgames.account.duplicate_username*
                    """
                    errorMessage: str = "This username is already taken."
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class email:
                    """
                    Parent class for all account email errors
                    """

                    class alternate_email_limit_exceeded(EpicException):
                        """
                        This error is thrown when an account email alternate email limit is exceeded
                        *errors.com.epicgames.account.email.alternate_email_limit_exceeded*
                        """
                        errorMessage: str = "Alternate email limit exceeded"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class email_already_on_account(EpicException):
                    """
                    This error is thrown when the account email is already on the account
                    """
                    errorMessage: str = "Email already on account"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class email_change_timeframe(EpicException):
                    """
                    This error is thrown when the account email change timeframe is invalid
                    *errors.com.epicgames.account.email_change_timeframe*
                    """
                    errorMessage: str = "Email change timeframe invalid"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class email_code:
                    """
                    Parent class for all account email code errors
                    """

                    class code_not_for_your_account(EpicException):
                        """
                        This error is thrown when an account email code is not for your account
                        *errors.com.epicgames.account.email_code.code_not_for_your_account*
                        """
                        errorMessage: str = "This code is not for your account."
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class code_not_found(EpicException):
                        """
                        This error is thrown when an account email code is not found
                        *errors.com.epicgames.account.email_code.code_not_found*
                        """
                        errorMessage: str = "Code not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class code_not_valid(EpicException):
                        """
                        This error is thrown when an account email code is not valid
                        *errors.com.epicgames.account.email_code.code_not_valid*
                        """
                        errorMessage: str = "Code not valid"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class email_code_expired(EpicException):
                        """
                        This error is thrown when an account email code is expired
                        """
                        errorMessage: str = "Code expired"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class validation_code_not_found(EpicException):
                        """
                        This error is thrown when an account email code validation code is not found
                        *errors.com.epicgames.account.email_code.validation_code_not_found*
                        """
                        errorMessage: str = "Validation code not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class email_not_found(EpicException):
                    """
                    This error is thrown when the account email is not found
                    *errors.com.epicgames.account.email_not_found*
                    """
                    errorMessage: str = "Email not found"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class ext_auth:
                    """
                    Parent class for all account external auth errors
                    """

                    class access_revoked(EpicException):
                        """
                        This error is thrown when an account external auth access is revoked
                        *errors.com.epicgames.account.ext_auth.access_revoked*
                        """
                        errorMessage: str = "Access revoked"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_cert(EpicException):
                        """
                        This error is thrown when an account external auth cert is invalid
                        *errors.com.epicgames.account.ext_auth.invalid_cert*
                        """
                        errorMessage: str = "Invalid cert"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_external_auth_token(EpicException):
                        """
                        This error is thrown when an account external auth token is invalid
                        *errors.com.epicgames.account.ext_auth.invalid_external_auth_token*
                        """
                        errorMessage: str = "Invalid external auth token"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_token(EpicException):
                        """
                        This error is thrown when an account external auth token is invalid
                        *errors.com.epicgames.account.ext_auth.invalid_token*
                        """
                        errorMessage: str = "Invalid token"
                        numericErrorCode: int = 1014
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 403

                    class linking_restricted(EpicException):
                        """
                        This error is thrown when an account external auth linking is restricted
                        *errors.com.epicgames.account.ext_auth.linking_restricted*
                        """
                        errorMessage: str = "Linking restricted"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class login_not_allowed(EpicException):
                        """
                        This error is thrown when an account external auth login is not allowed
                        *errors.com.epicgames.account.ext_auth.login_not_allowed*
                        """
                        errorMessage: str = "Login not allowed"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class missing_data(EpicException):
                        """
                        This error is thrown when an account external auth data is missing
                        *errors.com.epicgames.account.ext_auth.missing_data*
                        """
                        errorMessage: str = "Missing data"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class missing_scope(EpicException):
                        """
                        This error is thrown when an account external auth scope is missing
                        *errors.com.epicgames.account.ext_auth.missing_scope*
                        """
                        errorMessage: str = "Missing scope"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class token_expired(EpicException):
                        """
                        This error is thrown when an account external auth token is expired
                        *errors.com.epicgames.account.ext_auth.token_expired*
                        """
                        errorMessage: str = "Token expired"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class unknown_external_auth_type(EpicException):
                        """
                        This error is thrown when an account external auth type is unknown
                        *errors.com.epicgames.account.ext_auth.unknown_external_auth_type*
                        """
                        errorMessage: str = "Sorry, you are using an external auth type we do not support yet."
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class external_auth:
                        """
                        Parent class for all account external auth errors
                        """

                        class remove(EpicException):
                            """
                            Parent class for all account external auth removal errors
                            """

                            class forbid(EpicException):
                                """
                                Parent class for all forbidden account external auth errors
                                """

                                class last_trusted_ext_auth_facebook(EpicException):
                                    """
                                    This error is thrown when the last trusted account external auth facebook
                                    is forbidden
                                    *errors.com.epicgames.account.ext_auth.external_auth.remove.forbid.last_trusted_ext_auth_facebook*
                                    """
                                    errorMessage: str = "Last trusted external auth facebook is forbidden"
                                    numericErrorCode: int = 0
                                    originatingService: str = "com.epicgames.account.public"
                                    statusCode: int = 400

                                class last_trusted_ext_auth_google(EpicException):
                                    """
                                    This error is thrown when the last trusted account external auth google is forbidden
                                    *errors.com.epicgames.account.ext_auth.external_auth.remove.forbid.last_trusted_ext_auth_google*
                                    """
                                    errorMessage: str = "Last trusted external auth google is forbidden"
                                    numericErrorCode: int = 0
                                    originatingService: str = "com.epicgames.account.public"
                                    statusCode: int = 400

                                class last_trusted_ext_auth_vk(EpicException):
                                    """
                                    This error is thrown when the last trusted account external auth vk is forbidden
                                    *errors.com.epicgames.account.ext_auth.external_auth.remove.forbid.last_trusted_ext_auth_vk*
                                    """
                                    errorMessage: str = "Last trusted external auth vk is forbidden"
                                    numericErrorCode: int = 0
                                    originatingService: str = "com.epicgames.account.public"
                                    statusCode: int = 400

                class external_auth_account_id_mismatch(EpicException):
                    """
                    This error is thrown when an external auth account id is mismatched
                    *errors.com.epicgames.account.external_auth_account_id_mismatch*
                    """
                    errorMessage: str = "External auth account id mismatch"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class external_auth_not_found(EpicException):
                    """
                    This error is thrown when an external auth is not found
                    *errors.com.epicgames.account.external_auth_not_found*
                    """
                    errorMessage: str = "External auth not found"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class external_auth_restriction_not_found(EpicException):
                    """
                    This error is thrown when an external auth restriction is not found
                    *errors.com.epicgames.account.external_auth_restriction_not_found*
                    """
                    errorMessage: str = "External auth restriction not found"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class external_auth_validate_failed(EpicException):
                    """
                    This error is thrown when an external auth validation fails
                    *errors.com.epicgames.account.external_auth_validate_failed*
                    """
                    errorMessage: str = "External auth validate failed"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class full_account_auth_data_required(EpicException):
                    """
                    This error is thrown when a full account auth data is required
                    *errors.com.epicgames.account.full_account_auth_data_required*
                    """
                    errorMessage: str = "Full account auth data required"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class invalid_account_credentials(EpicException):
                    """
                    This error is thrown when an account credentials are invalid
                    *errors.com.epicgames.account.invalid_account_credentials*
                    """
                    errorMessage: str = "Sorry the account credentials you are using are invalid"
                    numericErrorCode: int = 18031
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class invalid_account_id_count(EpicException):
                    """
                    This error is thrown when an account id count is invalid
                    *errors.com.epicgames.account.invalid_account_id_count*

                    Message Vars:
                     - Count limit (100)
                    """
                    errorMessage: str = "Sorry, the number of account id should be at least one and not more than {0}."
                    numericErrorCode: int = 18066
                    originatingService: str = "com.epicgames.account.public"

                class invalid_client_credentials(EpicException):
                    """
                    This error is thrown when a client credentials are invalid
                    *errors.com.epicgames.account.invalid_client_credentials*
                    """
                    errorMessage: str = "Sorry the client credentials you are using are invalid"
                    numericErrorCode: int = 18033
                    originatingService: str = "com.epicgames.account.public"

                class invalid_count(EpicException):
                    """
                    This error is thrown when a count is invalid
                    *errors.com.epicgames.account.invalid_count*
                    """
                    errorMessage: str = "The count is invalid"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class invalid_start(EpicException):
                    """
                    This error is thrown when a start is invalid
                    *errors.com.epicgames.account.invalid_start*
                    """
                    errorMessage: str = "The start is invalid"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class keyring(EpicException):
                    """
                    Parent class for all account keyring errors
                    """

                    class unknown_keyring(EpicException):
                        """
                        This error is thrown when an unknown keyring is used
                        *errors.com.epicgames.account.keyring.unknown_keyring*
                        """
                        errorMessage: str = "Unknown keyring"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class key:
                    """
                    Parent class for all account key errors
                    """

                    class key_not_found(EpicException):
                        """
                        This error is thrown when a key is not found
                        """
                        errorMessage: str = "Key not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class merge:
                    """
                    Parent class for all account merging errors
                    """

                    class destination_account_not_full(EpicException):
                        """
                        This error is thrown when a destination account is not full
                        *errors.com.epicgames.account.merge.destination_account_not_full*
                        """
                        errorMessage: str = "Destination account not full"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class external_auth_conflict(EpicException):
                        """
                        This error is thrown when an external auth conflict occurs
                        *errors.com.epicgames.account.merge.external_auth_conflict*
                        """
                        errorMessage: str = "External auth conflict"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 409

                    class invalid_account_status(EpicException):
                        """
                        This error is thrown when an account status is invalid
                        """
                        errorMessage: str = "Invalid account status"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_apps(EpicException):
                        """
                        This error is thrown when an app is invalid
                        """
                        errorMessage: str = "Invalid apps"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class not_internal_client(EpicException):
                        """
                        This error is thrown when a client is not internal
                        *errors.com.epicgames.account.merge.not_internal_client*
                        """
                        errorMessage: str = "Not internal client"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class source_account_not_headless(EpicException):
                        """
                        This error is thrown when a source account is not headless
                        *errors.com.epicgames.account.merge.source_account_not_headless*
                        """
                        errorMessage: str = "Source account not headless"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class metadata:
                    """
                    Parent class for all account metadata errors
                    """

                    class too_many_keys(EpicException):
                        """
                        This error is thrown when too many keys are used
                        *errors.com.epicgames.account.metadata.too_many_keys*
                        """
                        errorMessage: str = "Too many keys"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class metadata_key_not_found(EpicException):
                    """
                    This error is thrown when a metadata key is not found
                    *errors.com.epicgames.account.metadata_key_not_found*
                    """
                    errorMessage: str = "Metadata key not found"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class no_account_found_for_external_auth(EpicException):
                    """
                    This error is thrown when no account is found for an external auth
                    *errors.com.epicgames.account.no_account_found_for_external_auth*
                    """
                    errorMessage: str = "No account found for external auth"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class oauth:
                    """
                    Parent class for all account oauth auth errors
                    """

                    class authorization_code_not_for_your_client(EpicException):
                        """
                        This error is thrown when an authorization code is not for your client
                        *errors.com.epicgames.account.oauth.authorization_code_not_for_your_client*
                        """
                        errorMessage: str = "Sorry the authorization code you supplied was not for your client"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class authorization_code_not_found(EpicException):
                        """
                        This error is thrown when an authorization code is not found
                        *errors.com.epicgames.account.oauth.authorization_code_not_found*
                        """
                        errorMessage: str = "Sorry the authorization code you supplied was not found. It is possible " \
                                            "that it was no longer valid"
                        numericErrorCode: int = 18059
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class authorization_pending(EpicException):
                        """
                        This error is thrown when an authorization is pending
                        *errors.com.epicgames.account.oauth.authorization_pending*
                        """
                        errorMessage: str = "The authorization server request is still pending as the end user has " \
                                            "yet to visit and enter the verification code."
                        numericErrorCode: int = 1012
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class code_not_valid_for_login_type(EpicException):
                        """
                        This error is thrown when a code is not valid for a login type
                        *errors.com.epicgames.account.oauth.code_not_valid_for_login_type*
                        """
                        errorMessage: str = "Sorry the code you supplied was not valid for the login type you " \
                                            "requested"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class exchange_code_not_found(EpicException):
                        """
                        This error is thrown when an exchange code is not found
                        *errors.com.epicgames.account.oauth.exchange_code_not_found*
                        """
                        errorMessage: str = "Sorry the exchange code you supplied was not found. It is possible that" \
                                            " it was no longer valid"
                        numericErrorCode: int = 18057
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class expired_authorization_code(EpicException):
                        """
                        This error is thrown when an authorization code is expired
                        *errors.com.epicgames.account.oauth.expired_authorization_code*
                        """
                        errorMessage: str = "Sorry, your authorization code has expired. Please log in again."
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 401

                    class expired_exchange_code(EpicException):
                        """
                        This error is thrown when an exchange code is expired
                        *errors.com.epicgames.account.oauth.expired_exchange_code*
                        """
                        errorMessage: str = "Sorry, your exchange code has expired. Please log in again."
                        numericErrorCode: int = 18128
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 401

                    class expired_exchange_code_session(EpicException):
                        """
                        This error is thrown when an exchange code session is expired
                        *errors.com.epicgames.account.oauth.expired_exchange_code_session*
                        """
                        errorMessage: str = "Sorry the originating session for the exchange_code has expired."
                        numericErrorCode: int = 18128
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 401

                    class missing_real_id_association(EpicException):
                        """
                        This error is thrown when a real id association is missing
                        *errors.com.epicgames.account.oauth.missing_real_id_association*
                        """
                        errorMessage: str = "Real ID association is required to proceed"
                        numericErrorCode: int = 18109
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 403

                    class parental_control(EpicException):
                        """
                        Parent class for all account parental control errors
                        """

                        class playing_forbidden(EpicException):
                            """
                            This error is thrown when playing is forbidden by parental control
                            *errors.com.epicgames.account.oauth.parental_control.playing_forbidden*
                            """
                            errorMessage: str = "Playing is forbidden by parental control"
                            numericErrorCode: int = 0
                            originatingService: str = "com.epicgames.account.public"
                            statusCode: int = 400

                    class password_reset_required(EpicException):
                        """
                        This error is thrown when a password reset is required
                        *errors.com.epicgames.account.oauth.password_reset_required*
                        """
                        errorMessage: str = "Password reset required"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class single_use_code_expired(EpicException):
                        """
                        This error is thrown when a single use code is expired
                        *errors.com.epicgames.account.oauth.single_use_code_expired*
                        """
                        errorMessage: str = "Sorry the single use code you supplied has expired. It is possible that" \
                                            " it was no longer valid"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class single_use_code_not_found(EpicException):
                        """
                        This error is thrown when a single use code is not found
                        *errors.com.epicgames.account.oauth.single_use_code_not_found*
                        """
                        errorMessage: str = "Sorry the single use code you supplied was not found. It is possible " \
                                            "that it was no longer valid"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class token_exchange_not_allowed(EpicException):
                        """
                        This error is thrown when a token exchange is not allowed
                        *errors.com.epicgames.account.oauth.token_exchange_not_allowed*
                        """
                        errorMessage: str = "Token exchange is not allowed for this client"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class too_many_sessions(EpicException):
                        """
                        This error is thrown when too many sessions have been issued for an account
                        *errors.com.epicgames.account.oauth.too_many_sessions*
                        """
                        errorMessage: str = "Sorry too many sessions have been issued for your account. Please try " \
                                            "again later"
                        numericErrorCode: int = 18048
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 403

                class old_password_reuse(EpicException):
                    """
                    This error is thrown when an old password is reused
                    *errors.com.epicgames.account.old_password_reuse*
                    """
                    errorMessage: str = "Sorry you cannot reuse an old password"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class password_required(EpicException):
                    """
                    This error is thrown when a password is required
                    *errors.com.epicgames.account.password_required*
                    """
                    errorMessage: str = "Password is required"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class real_id(EpicException):
                    """
                    Parent class for all account real identification errors
                    """

                    class country_change_forbidden(EpicException):
                        """
                        This error is thrown when a country change is forbidden
                        *errors.com.epicgames.account.real_id.country_change_forbidden*
                        """
                        errorMessage: str = "Country change is forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class remove_default_email(EpicException):
                    """
                    This error is thrown when a default email is removed
                    *errors.com.epicgames.account.remove_default_email*
                    """
                    errorMessage: str = "You cannot remove your default email address"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class role:
                    """
                    Parent class for all account role errors
                    """

                    class duplicate_role_creation(EpicException):
                        """
                        This error is thrown when a role is duplicated
                        *errors.com.epicgames.account.role.duplicate_role_creation*
                        """
                        errorMessage: str = "Role already exists"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class duplicate_role_mapping(EpicException):
                        """
                        This error is thrown when a role mapping is duplicated
                        *errors.com.epicgames.account.role.duplicate_role_mapping*
                        """
                        errorMessage: str = "Role mapping already exists"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_role_assignment(EpicException):
                        """
                        This error is thrown when a role assignment is invalid
                        *errors.com.epicgames.account.role.invalid_role_assignment*
                        """
                        errorMessage: str = "Role assignment is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class role_in_use_cannot_be_deleted(EpicException):
                        """
                        This error is thrown when a role in use cannot be deleted
                        *errors.com.epicgames.account.role.role_in_use_cannot_be_deleted*
                        """
                        errorMessage: str = "Role in use cannot be deleted"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class role_not_found(EpicException):
                        """
                        This error is thrown when a role is not found
                        *errors.com.epicgames.account.role.role_not_found*
                        """
                        errorMessage: str = "Role not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class role_permission_not_deleted_not_found(EpicException):
                        """
                        This error is thrown when a role permission is not deleted and not found
                        *errors.com.epicgames.account.role.role_permission_not_deleted_not_found*
                        """
                        errorMessage: str = "Role permission not deleted not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class role_locked_for_delete(EpicException):
                    """
                    This error is thrown when a role is locked for deletion
                    *errors.com.epicgames.account.role_locked_for_delete*
                    """
                    errorMessage: str = "Role is locked for deletion"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class role_locked_for_update(EpicException):
                    """
                    This error is thrown when a role is locked for update
                    *errors.com.epicgames.account.role_locked_for_update*
                    """
                    errorMessage: str = "Role is locked for update"
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class sdn:
                    """
                    Parent class for all account sdn errors
                    """

                    class challenge_not_allowed(EpicException):
                        """
                        This error is thrown when a challenge is not allowed
                        *errors.com.epicgames.account.sdn.challenge_not_allowed*
                        """
                        errorMessage: str = "Challenge not allowed"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class disabled(EpicException):
                        """
                        This error is thrown when a sdn is disabled
                        *errors.com.epicgames.account.sdn.disabled*
                        """
                        errorMessage: str = "SDN is disabled"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class link_github_failed(EpicException):
                        """
                        This error is thrown when a github link is failed
                        *errors.com.epicgames.account.sdn.link_github_failed*
                        """
                        errorMessage: str = "Link github failed"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class sync_failed(EpicException):
                        """
                        This error is thrown when a sync is failed
                        *errors.com.epicgames.account.sdn.sync_failed*
                        """
                        errorMessage: str = "Sync failed"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class update_failed_due_to_sdn(EpicException):
                        """
                        This error is thrown when a update is failed due to sdn
                        *errors.com.epicgames.account.sdn.update_failed_due_to_sdn*
                        """
                        errorMessage: str = "Update failed due to SDN"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class update_not_allowed(EpicException):
                        """
                        This error is thrown when a update is not allowed
                        *errors.com.epicgames.account.sdn.update_not_allowed*
                        """
                        errorMessage: str = "Update not allowed"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class single_use_password:
                    """
                    Parent class for all account single use password errors
                    """

                    class conflict(EpicException):
                        """
                        This error is thrown when a single use password is in conflict
                        *errors.com.epicgames.account.single_use_password.conflict*
                        """
                        errorMessage: str = "Single use password in conflict"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 409

                    class not_found(EpicException):
                        """
                        This error is thrown when a single use password is not found
                        *errors.com.epicgames.account.single_use_password.not_found*
                        """
                        errorMessage: str = "Single use password not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class throttled(EpicException):
                    """
                    This error is thrown when being ratelimited on the account service
                    *errors.com.epicgames.account.throttled*

                    Message Vars:
                     - Retry-After seconds (500)
                    """
                    errorMessage: str = "Operation access is limited by throttling policy, please try again in {0} " \
                                        "second(s)."
                    numericErrorCode: int = 1041
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 429

                class token_account_id_does_not_match_url_accountId(EpicException):
                    """
                    This error is thrown when the accountId supplied in the url does not match the accountId for the
                    OAuth token.
                    *errors.com.epicgames.account.token_account_id_does_not_match_url_accountId*
                    """
                    errorMessage: str = "The accountId supplied in the url does not match the accountId for the " \
                                        "OAuth token."
                    numericErrorCode: int = 18055
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class white_list:
                    """
                    Parent class for all account white list errors
                    """

                    class duplicate_white_list_entry(EpicException):
                        """
                        This error is thrown when a duplicate white list entry is found
                        *errors.com.epicgames.account.white_list.duplicate_white_list_entry*
                        """
                        errorMessage: str = "Duplicate white list entry"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class white_list_entry_not_found(EpicException):
                        """
                        This error is thrown when a white list entry is not found
                        *errors.com.epicgames.account.white_list.white_list_entry_not_found*
                        """
                        errorMessage: str = "White list entry not found"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class xbl:
                    """
                    Parent class for all xbox live account errors
                    """

                    class invalid_token(EpicException):
                        """
                        This error is thrown when a xbox live token is invalid
                        *errors.com.epicgames.account.xbl.invalid_token*
                        """
                        errorMessage: str = "Invalid token"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class invalid_token_date(EpicException):
                        """
                        This error is thrown when a xbox live token date is invalid
                        *errors.com.epicgames.account.xbl.invalid_token_date*
                        """
                        errorMessage: str = "Invalid token date"
                        numericErrorCode: int = 0
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

            class affiliate:
                """
                Parent class for all affiliate errors
                """

                class slug_not_found(EpicException):
                    """
                    This error is thrown when a support a creator code is not found
                    *errors.com.epicgames.affiliate.slug_not_found*
                    """
                    errorMessage: str = "The creator code was not found."
                    numericErrorCode: int = 16004
                    originatingService: str = "WEX"
                    statusCode: int = 404

            class bad_request(EpicException):
                """
                This error is thrown when a bad request is made
                *errors.com.epicgames.bad_request*
                """
                errorMessage: str = "Sorry the request you made was invalid"
                numericErrorCode: int = 1006
                originatingService: str = "WEX"
                statusCode: int = 400

            class catalog_helper:
                """
                Parent class for all catalog helper errors
                """

                class unable_to_parse_receipts(EpicException):
                    """
                    This error is thrown when a catalog helper is unable to parse receipts
                    *errors.com.epicgames.catalog_helper.unable_to_parse_receipts*
                    """
                    errorMessage: str = "Unable to parse receipts"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class chat:
                """
                Parent class for all chat errors
                """

                class forbidden_chat_operation(EpicException):
                    """
                    This error is thrown when a chat operation is forbidden
                    *errors.com.epicgames.chat.forbidden_chat_operation*
                    """
                    errorMessage: str = "Forbidden chat operation"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_room_settings(EpicException):
                    """
                    This error is thrown when a room settings is invalid
                    *errors.com.epicgames.chat.invalid_room_settings*
                    """
                    errorMessage: str = "Invalid room settings"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class room_creation_conflict(EpicException):
                    """
                    This error is thrown when a room creation is in conflict
                    *errors.com.epicgames.chat.room_creation_conflict*
                    """
                    errorMessage: str = "Room creation conflict"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 409

                class room_creation_failed(EpicException):
                    """
                    This error is thrown when a room creation fails
                    *errors.com.epicgames.chat.room_creation_failed*
                    """
                    errorMessage: str = "Room creation failed"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class room_not_found(EpicException):
                    """
                    This error is thrown when a room is not found
                    *errors.com.epicgames.chat.room_not_found*
                    """
                    errorMessage: str = "Room not found"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class xmpp_connection_error(EpicException):
                    """
                    This error is thrown when a xmpp connection error occurs
                    *errors.com.epicgames.chat.xmpp_connection_error*
                    """
                    errorMessage: str = "XMPP connection error"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class cloudstorage:
                """
                Parent class for all cloud storage errors
                """

                class connection_close_failed(EpicException):
                    """
                    This error is thrown when a connection close fails
                    *errors.com.epicgames.cloudstorage.connection_close_failed*
                    """
                    errorMessage: str = "Connection close failed"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class data_read(EpicException):
                    """
                    This error is thrown when a data read fails
                    *errors.com.epicgames.cloudstorage.data_read*
                    """
                    errorMessage: str = "Data read failed"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class duplicate_system_file(EpicException):
                    """
                    This error is thrown when a system file is duplicated
                    *errors.com.epicgames.cloudstorage.duplicate_system_file*
                    """
                    errorMessage: str = "Duplicate system file"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class file_not_found(EpicException):
                    """
                    This error is thrown when a file is not found
                    *errors.com.epicgames.cloudstorage.file_not_found*
                    """
                    errorMessage: str = "Sorry, we couldn't find a file {0} for account {1}"
                    numericErrorCode: int = 12007
                    originatingService: str = "WEX"
                    statusCode: int = 404

                class invalid_storage_size(EpicException):
                    """
                    This error is thrown when a storage size is invalid
                    *errors.com.epicgames.cloudstorage.invalid_storage_size*
                    """
                    errorMessage: str = "Invalid storage size"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_user_storage_data(EpicException):
                    """
                    This error is thrown when a user storage data is invalid
                    *errors.com.epicgames.cloudstorage.invalid_user_storage_data*
                    """
                    errorMessage: str = "Invalid user storage data"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_window_dates(EpicException):
                    """
                    This error is thrown when a window date is invalid
                    *errors.com.epicgames.cloudstorage.invalid_window_dates*
                    """
                    errorMessage: str = "Invalid window dates"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class new_quota_below_current_usage(EpicException):
                    """
                    This error is thrown when a new quota is below current usage
                    *errors.com.epicgames.cloudstorage.new_quota_below_current_usage*
                    """
                    errorMessage: str = "New quota below current usage"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class user_storage_data_not_found(EpicException):
                    """
                    This error is thrown when a user storage data is not found
                    *errors.com.epicgames.cloudstorage.user_storage_data_not_found*
                    """
                    errorMessage: str = "User storage data not found"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class window_dates_required(EpicException):
                    """
                    This error is thrown when window dates are required
                    *errors.com.epicgames.cloudstorage.window_dates_required*
                    """
                    errorMessage: str = "Window dates required"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class coderedemption:
                """
                Parent class for all code redemption errors
                """

                class code_used(EpicException):
                    """
                    This error is thrown when a code is already used
                    *errors.com.epicgames.coderedemption.code_used*

                    Message Vars:
                     - The code used (PHKJB92N4UWDGQKKALG3)
                    """
                    errorMessage: str = "Code used; code:{0}"
                    numericErrorCode: int = 19010
                    originatingService: str = "com.epicgames.coderedemption.public"
                    statusCode: int = 400

            class common:
                """
                Parent class for all common errors
                """

                class argus:
                    """
                    Parent class for all argus errors
                    """

                    class vulnerable_credentials(EpicException):
                        """
                        This error is thrown when vulnerable credentials are used
                        *errors.com.epicgames.common.argus.vulnerable_credentials*
                        """
                        errorMessage: str = "Vulnerable credentials"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class authentication:
                    """
                    Parent class for all authentication errors
                    """

                    class authentication_failed(EpicException):
                        """
                        This error is thrown when an authentication fails
                        *errors.com.epicgames.common.authentication.authentication_failed*

                        Message Vars:
                         - URL (/api/v1)
                        """
                        errorMessage: str = "Authentication failed for {0}"
                        numericErrorCode: int = 1032
                        statusCode: int = 401

                    class invalid_client_service(EpicException):
                        """
                        This error is thrown when a client service is invalid
                        *errors.com.epicgames.common.authentication.invalid_client_service*
                        """
                        errorMessage: str = "Invalid client service"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class token_verification_failed(EpicException):
                        """
                        This error is thrown when a token verification fails
                        *errors.com.epicgames.common.authentication.token_verification_failed*

                        Message Vars:
                         - Token used (bearer eg1~...)
                        """
                        errorMessage: str = "Sorry we couldn't validate your token {0}. Please try with a new token."
                        numericErrorCode: int = 1031
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class unable_to_retrieve_perms(EpicException):
                        """
                        This error is thrown when permissions cannot be retrieved
                        *errors.com.epicgames.common.authentication.unable_to_retrieve_perms*
                        """
                        errorMessage: str = "Unable to retrieve permissions"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class bad_gateway(EpicException):
                    """
                    This error is thrown when a bad gateway is received
                    *errors.com.epicgames.common.bad_gateway*
                    """
                    errorMessage: str = "Bad gateway"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class concurrent_modification_error(EpicException):
                    """
                    This error is thrown when a concurrent modification occurs
                    *errors.com.epicgames.common.concurrent_modification_error*
                    """
                    errorMessage: str = "Sorry, the item you were trying to edit was changed before your edit could " \
                                        "be completed. Please retry your edit."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 409

                class duplicate_entry(EpicException):
                    """
                    This error is thrown when a duplicate entry is found
                    *errors.com.epicgames.common.duplicate_entry*
                    """
                    errorMessage: str = "Duplicate entry"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class early_eof(EpicException):
                    """
                    This error is thrown when an early EOF is received
                    *errors.com.epicgames.common.early_eof*
                    """
                    errorMessage: str = "Early EOF"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class http_request_timeout(EpicException):
                    """
                    This error is thrown when an HTTP request times out
                    *errors.com.epicgames.common.http_request_timeout*
                    """
                    errorMessage: str = "HTTP request timed out"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class json_mapping_error(EpicException):
                    """
                    This error is thrown when a JSON mapping fails
                    *errors.com.epicgames.common.json_mapping_error*
                    """
                    errorMessage: str = "Json mapping failed."
                    numericErrorCode: int = 1019

                class json_parse_error(EpicException):
                    """
                    This error is thrown when a JSON parse fails
                    *errors.com.epicgames.common.json_parse_error*
                    """
                    errorMessage: str = "Json parse failed."
                    numericErrorCode: int = 1019

                class json_payload_required(EpicException):
                    """
                    This error is thrown when a JSON payload is required
                    *errors.com.epicgames.common.json_payload_required*
                    """
                    errorMessage: str = "Json payload is required."
                    numericErrorCode: int = 1020

                class method_not_allowed(EpicException):
                    """
                    This error is thrown when a method is not allowed
                    *errors.com.epicgames.common.method_not_allowed*
                    """
                    errorMessage: str = "Sorry the resource you were trying to access cannot be accessed with the " \
                                        "HTTP method you used."
                    numericErrorCode: int = 1009
                    originatingService: str = "WEX"
                    statusCode: int = 405

                class missing_permission(EpicException):
                    """
                    This error is thrown when a permission is missing
                    *errors.com.epicgames.common.missing_permission*

                    Message Vars:
                     - Permission (fortnite:profile:<account_id>:commands)
                     - Scope (ALL)
                    """
                    errorMessage: str = "Sorry your login does not posses the permissions '{0} {1}' needed to " \
                                        "perform the requested operation"
                    numericErrorCode: int = 1023
                    statusCode: int = 403

                class missing_action(EpicException):
                    """
                    This error is thrown when an action is missing
                    *errors.com.epicgames.common.missing_action*

                    Message Vars:
                     - Action (PLAY)
                     - Platform (Windows)
                    """
                    errorMessage: str = "Login is banned or does not posses the action '{0}' needed to perform the " \
                                        "requested operation for platform '{1}'"
                    numericErrorCode: int = 1023
                    statusCode: int = 403

                class mongo_execution_timeout_error(EpicException):
                    """
                    This error is thrown when a mongo execution times out
                    *errors.com.epicgames.common.mongo_execution_timeout_error*
                    """
                    errorMessage: str = "Sorry, there was a timeout utilizing the database."
                    numericErrorCode: int = 1045

                class not_found(EpicException):
                    """
                    This error is thrown when a resource is not found
                    *errors.com.epicgames.common.not_found*
                    """
                    errorMessage: str = "Sorry the resource you were trying to find could not be found"
                    numericErrorCode: int = 1004
                    statusCode: int = 404

                class oauth:
                    """
                    Parent class for common oauth errors
                    """

                    class invalid_client(EpicException):
                        """
                        This error is thrown when a client is invalid
                        *errors.com.epicgames.common.oauth.invalid_client*
                        """
                        errorMessage: str = "Sorry the client credentials you are using are invalid"
                        numericErrorCode: int = 18033
                        originatingService: str = "com.epicgames.account.public"

                    class invalid_grant(EpicException):
                        """
                        This error is thrown when a grant is invalid
                        *errors.com.epicgames.common.oauth.invalid_grant*
                        """
                        errorMessage: str = "Sorry the grant you are using is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_request(EpicException):
                        """
                        This error is thrown when a request is invalid
                        *errors.com.epicgames.common.oauth.invalid_request*
                        """
                        errorMessage: str = "Sorry the request you are using is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_token(EpicException):
                        """
                        This error is thrown when a token is invalid
                        *errors.com.epicgames.common.oauth.invalid_token*
                        """
                        errorMessage: str = "Sorry the token you are using is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 401

                    class oauth_error(EpicException):
                        """
                        This error is thrown when an oauth error occurs
                        *errors.com.epicgames.common.oauth.oauth_error*
                        """
                        errorMessage: str = "Sorry an oauth error occurred"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class unauthorized_client(EpicException):
                        """
                        This error is thrown when a client is unauthorized
                        *errors.com.epicgames.common.oauth.unauthorized_client*
                        """
                        errorMessage: str = "Sorry your client is not allowed to use the grant type token_to_token"
                        numericErrorCode: int = 1015
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                    class unsupported_grant_type(EpicException):
                        """
                        This error is thrown when a grant type is unsupported
                        *errors.com.epicgames.common.oauth.unsupported_grant_type*
                        """
                        errorMessage: str = "Sorry, your client does not have the proper grant_type for access."
                        numericErrorCode: int = 1016
                        originatingService: str = "com.epicgames.account.public"
                        statusCode: int = 400

                class oauth_account_authentication_required(EpicException):
                    """
                    This error is thrown when an oauth account authentication is required
                    *errors.com.epicgames.common.oauth_account_authentication_required*
                    """
                    errorMessage: str = "OAuth account authentication required."
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class oauth_authentication_required(EpicException):
                    """
                    This error is thrown when an oauth authentication is required
                    *errors.com.epicgames.common.oauth_authentication_required*
                    """
                    errorMessage: str = "OAuth authentication required."
                    numericErrorCode: int = 0
                    originatingService: str = "com.epicgames.account.public"
                    statusCode: int = 400

                class request_not_acceptable(EpicException):
                    """
                    This error is thrown when a request is not acceptable
                    *errors.com.epicgames.common.request_not_acceptable*
                    """
                    errorMessage: str = "Sorry the request you are using is not acceptable"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class throttled(EpicException):
                    """
                    This error is thrown when a request is rate limited
                    *errors.com.epicgames.common.throttled*

                    Message Vars:
                     - API group (high)
                    """
                    errorMessage: str = "Server have no capacity to serve request for API group {0}."
                    numericErrorCode: int = 1041
                    statusCode: int = 429

                class timeout(EpicException):
                    """
                    This error is thrown when a request times out
                    *errors.com.epicgames.common.timeout*
                    """
                    errorMessage: str = "Sorry the request you are using timed out"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class two_factor_authentication(EpicException):
                    """
                    Parent class for common 2fa errors
                    """

                    class required(EpicException):
                        """
                        This error is thrown when 2fa is required
                        *errors.com.epicgames.common.two_factor_authentication.required*
                        """
                        errorMessage: str = "Sorry, two factor authentication is required for this account."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class verification_failed(EpicException):
                        """
                        This error is thrown when 2fa verification fails
                        *errors.com.epicgames.common.two_factor_authentication.verification_failed*
                        """
                        errorMessage: str = "Sorry, two factor authentication verification failed."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

            class conflict(EpicException):
                """
                This exception is thrown when a conflict occurs
                *errors.com.epicgames.conflict*
                """
                errorMessage: str = "Sorry, the resource you are trying to access is conflicting with another " \
                                    "resource."
                numericErrorCode: int = 0
                originatingService: str = "WEX"
                statusCode: int = 409

            class couldstorage:
                """
                Parent class for all remaining cloudstorage exceptions
                Yes, the typo is apparently intentional
                """

                class file_move_failed(EpicException):
                    """
                    This exception is thrown when a file move fails
                    *errors.com.epicgames.couldstorage.file_move_failed*
                    """
                    errorMessage: str = "Sorry, the file move failed."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_account_id(EpicException):
                    """
                    This exception is thrown when an invalid account ID is used
                    *errors.com.epicgames.couldstorage.invalid_account_id*
                    """
                    errorMessage: str = "Sorry, the account ID you are using is invalid."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_user_file(EpicException):
                    """
                    This exception is thrown when an invalid user file is used
                    *errors.com.epicgames.couldstorage.invalid_user_file*
                    """
                    errorMessage: str = "Sorry, the user file you are using is invalid."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class out_of_user_space(EpicException):
                    """
                    This exception is thrown when the user is out of space
                    *errors.com.epicgames.couldstorage.out_of_user_space*
                    """
                    errorMessage: str = "Sorry, you are out of space."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class user_file_post_move_delete_failed(EpicException):
                    """
                    This exception is thrown when a user file post move delete fails
                    """
                    errorMessage: str = "Sorry, the user file post move delete failed."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class datarouter:
                """
                Parent class for all datarouter exceptions
                """

                class request_limit_reached(EpicException):
                    """
                    This exception is thrown when the request limit is reached
                    *errors.com.epicgames.datarouter.request_limit_reached*
                    """
                    errorMessage: str = "Sorry, the request limit has been reached."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class ecommerce:
                """
                Parent class for all ecommerce exceptions
                """

                class affiliate:
                    """
                    Parent class for all affiliate exceptions
                    """

                    class not_whitelisted(EpicException):
                        """
                        This exception is thrown when the affiliate is not whitelisted
                        *errors.com.epicgames.ecommerce.affiliate.not_whitelisted*
                        """
                        errorMessage: str = "Sorry, the affiliate is not whitelisted."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class fulfillment:
                    """
                    Parent class for all ecommerce fulfillment exceptions
                    """

                    class code:
                        """
                        Parent class for all ecommerce fulfillment code exceptions
                        """

                        class criteria:
                            """
                            Parent class for all ecommerce fulfillment code criteria exceptions
                            """

                            class reject(EpicException):
                                """
                                This exception is thrown when the fulfillment code is rejected
                                *errors.com.epicgames.ecommerce.fulfillment.code.criteria.reject*
                                """
                                errorMessage: str = "Sorry, the fulfillment code is rejected."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                    class integration:
                        """
                        Parent class for all ecommerce fulfillment integration exceptions
                        """

                        class entitlement:
                            """
                            Parent class for all ecommerce fulfillment integration entitlement exceptions
                            """

                            class jwt:
                                """
                                Parent class for all ecommerce fulfillment integration entitlement JWT exceptions
                                """

                                class entitlement_not_found(EpicException):
                                    """
                                    This exception is thrown when the entitlement is not found
                                    *errors.com.epicgames.ecommerce.fulfillment.integration.entitlement.jwt.entitlement_not_found*
                                    """
                                    errorMessage: str = "Sorry, the entitlement is not found."
                                    numericErrorCode: int = 0
                                    originatingService: str = "WEX"
                                    statusCode: int = 400

                        class invalid_parameter(EpicException):
                            """
                            This exception is thrown when an invalid parameter is used
                            *errors.com.epicgames.ecommerce.fulfillment.integration.invalid_parameter*
                            """
                            errorMessage: str = "Sorry, the parameter you are using is invalid."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

            class forbidden(EpicException):
                """
                This exception is thrown when the request is forbidden
                *errors.com.epicgames.forbidden*
                """
                errorMessage: str = "Forbidden from accessing this resource."
                numericErrorCode: int = 1023
                statusCode: int = 403

            class friends:
                """
                Parent class for all friends exceptions
                """

                class cannot_friend_due_to_target_settings(EpicException):
                    """
                    This exception is thrown when the target cannot be friended due to settings
                    *errors.com.epicgames.friends.cannot_friend_due_to_target_settings*
                    """
                    errorMessage: str = "Cannot friend this person due to their privacy settings."
                    numericErrorCode: int = 16003
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class duplicate_friendship(EpicException):
                    """
                    This exception is thrown when a duplicate friendship is used
                    *errors.com.epicgames.friends.duplicate_friendship*
                    """
                    errorMessage: str = "Sorry, a friendship already exists with this user."
                    numericErrorCode: int = 16004
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class execution_failed(EpicException):
                    """
                    This exception is thrown when the execution fails
                    *errors.com.epicgames.friends.execution_failed*
                    """
                    errorMessage: str = "Sorry, the execution failed."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class friend_request_already_sent(EpicException):
                    """
                    This exception is thrown when the friend request is already sent
                    *errors.com.epicgames.friends.friend_request_already_sent*
                    """
                    errorMessage: str = "You have already sent a friend request to this user."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class friendship_not_found(EpicException):
                    """
                    This exception is thrown when the friendship is not found
                    *errors.com.epicgames.friends.friendship_not_found*
                    """
                    errorMessage: str = "Sorry, it appears you are not friends with this person."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_connection_source_name(EpicException):
                    """
                    This exception is thrown when the connection source name is invalid
                    *errors.com.epicgames.friends.invalid_connection_source_name*
                    """
                    errorMessage: str = "Sorry, the connection source name is invalid."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_friendship(EpicException):
                    """
                    This exception is thrown when the friendship is invalid
                    *errors.com.epicgames.friends.invalid_friendship*
                    """
                    errorMessage: str = "Sorry, the friendship is invalid."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class no_external_auth_profile_id(EpicException):
                    """
                    This exception is thrown when there is no external auth profile ID
                    *errors.com.epicgames.friends.no_external_auth_profile_id*
                    """
                    errorMessage: str = "Sorry, there is no external auth profile ID."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class recent_players_events_disabled(EpicException):
                    """
                    This exception is thrown when recent players events are disabled
                    *errors.com.epicgames.friends.recent_players_events_disabled*
                    """
                    errorMessage: str = "Sorry, recent players events are disabled."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class user_list_not_found(EpicException):
                    """
                    This exception is thrown when the user list is not found
                    *errors.com.epicgames.friends.user_list_not_found*
                    """
                    errorMessage: str = "Sorry, the user list is not found."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class user_list_not_supported(EpicException):
                    """
                    This exception is thrown when the user list is not supported
                    *errors.com.epicgames.friends.user_list_not_supported*
                    """
                    errorMessage: str = "Sorry, the user list is not supported."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class user_not_found_in_list(EpicException):
                    """
                    This exception is thrown when the user is not found in the list
                    *errors.com.epicgames.friends.user_not_found_in_list*
                    """
                    errorMessage: str = "Sorry, the user is not found in the list."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class identity:
                """
                Parent class for all identity exceptions
                """

                class realid:
                    """
                    Parent class for all realid exceptions
                    """

                    class account_not_found(EpicException):
                        """
                        This exception is thrown when the account is not found
                        *errors.com.epicgames.identity.realid.account_not_found*
                        """
                        errorMessage: str = "Sorry, the account is not found."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                        class auth:
                            """
                            Parent class for all real identity auth exceptions
                            """

                            class failed(EpicException):
                                """
                                This exception is thrown when the real identity auth failed
                                *errors.com.epicgames.identity.realid.account_not_found.auth.failed*
                                """
                                errorMessage: str = "Sorry, the real identity auth failed."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                        class link_epic_account:
                            """
                            Parent class for all real identity link epic account exceptions
                            """

                            class already_linked(EpicException):
                                """
                                This exception is thrown when the real identity link epic account is already linked
                                *errors.com.epicgames.identity.realid.account_not_found.link_epic_account.already_linked*
                                """
                                errorMessage: str = "Sorry, the real identity link epic account is already linked."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class max_linked_accounts_restriction(EpicException):
                                """
                                This exception is thrown when the real identity link epic account has max linked
                                accounts restriction
                                *errors.com.epicgames.identity.realid.account_not_found.link_epic_account.max_linked_accounts_restriction*
                                """
                                errorMessage: str = "Sorry, the real identity link epic account has max linked " \
                                                    "accounts restriction."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class not_linked(EpicException):
                                """
                                This exception is thrown when the real identity link epic account is not linked
                                *errors.com.epicgames.identity.realid.account_not_found.link_epic_account.not_linked*
                                """
                                errorMessage: str = "Sorry, the real identity link epic account is not linked."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class operation_conflict(EpicException):
                                """
                                This exception is thrown when the real identity link epic account has operation conflict
                                *errors.com.epicgames.identity.realid.account_not_found.link_epic_account.operation_conflict*
                                """
                                errorMessage: str = "Sorry, the real identity link epic account has operation conflict."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 409

                            class token_account_mismatch(EpicException):
                                """
                                This exception is thrown when the real identity link epic account has token
                                account mismatch
                                *errors.com.epicgames.identity.realid.account_not_found.link_epic_account.token_account_mismatch*
                                """
                                errorMessage: str = "Sorry, the real identity link epic account has token account " \
                                                    "mismatch."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                        class link_minor:
                            """
                            Parent class for all real identity link minor exceptions
                            """

                            class adult_age_group(EpicException):
                                """
                                This exception is thrown when the real identity link minor has adult age group
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.adult_age_group*
                                """
                                errorMessage: str = "Sorry, the real identity link minor has adult age group."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class birthday_mismatch(EpicException):
                                """
                                This exception is thrown when the real identity link minor has birthday mismatch
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.birthday_mismatch*
                                """
                                errorMessage: str = "Sorry, the real identity link minor has birthday mismatch."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class guardian_age(EpicException):
                                """
                                This exception is thrown when the real identity link minor has guardian age
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.guardian_age*
                                """
                                errorMessage: str = "Sorry, the guardian age is missing probably."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class guardian_exists(EpicException):
                                """
                                This exception is thrown when the real identity link minor has guardian exists
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.guardian_exists*
                                """
                                errorMessage: str = "Sorry, the guardian exists."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class guardian_not_linked(EpicException):
                                """
                                This exception is thrown when the real identity link minor has guardian not linked
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.guardian_not_linked*
                                """
                                errorMessage: str = "Sorry, the guardian is not linked."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class link_foreignor_forbidden(EpicException):
                                """
                                This exception is thrown when the real identity link minor has link foreignor forbidden
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.link_foreignor_forbidden*
                                """
                                errorMessage: str = "Sorry, the link foreignor is forbidden."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class max_linked_minors_restriction(EpicException):
                                """
                                This exception is thrown when the real identity link minor has max linked
                                minors restriction
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.max_linked_minors_restriction*
                                """
                                errorMessage: str = "Sorry, the minor has max linked minors restriction."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                            class operation_conflict(EpicException):
                                """
                                This exception is thrown when the operation conflicts
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.operation_conflict*
                                """
                                errorMessage: str = "Sorry, the operation conflicts."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 409

                            class realname_mismatch(EpicException):
                                """
                                This exception is thrown when the real identity link minor has realname mismatch
                                *errors.com.epicgames.identity.realid.account_not_found.link_minor.realname_mismatch*
                                """
                                errorMessage: str = "Sorry, real name mismatch."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                    class minor_not_linked(EpicException):
                        """
                        This exception is thrown when the real identity link minor is not linked
                        *errors.com.epicgames.identity.realid.minor_not_linked*
                        """
                        errorMessage: str = "Sorry, the real identity link minor is not linked."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class no_guardian(EpicException):
                        """
                        This exception is thrown when the real identity has no guardian
                        *errors.com.epicgames.identity.realid.no_guardian*
                        """
                        errorMessage: str = "Sorry, the real identity has no guardian."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class result_verification:
                        """
                        Parent class for all real identity result verification exceptions
                        """

                        class client_error:
                            """
                            Parent class for all real identity result verification client errors
                            """

                            class authentication_attempts_exceeded(EpicException):
                                """
                                This exception is thrown when the real identity result verification client
                                has authentication attempts exceeded
                                *errors.com.epicgames.identity.realid.result_verification.client_error.authentication_attempts_exceeded*
                                """
                                errorMessage: str = "Sorry, the real identity result verification client has " \
                                                    "authentication attempts exceeded."
                                numericErrorCode: int = 0
                                originatingService: str = "WEX"
                                statusCode: int = 400

                        class decrypt_error(EpicException):
                            """
                            This exception is thrown when the real identity result verification has decrypt error
                            *errors.com.epicgames.identity.realid.result_verification.decrypt_error*

                            Message Vars:
                             - Result ()
                             - Reason ([com.google.common.io.BaseEncoding$DecodingException: Unrecognized character: {])
                            """
                            errorMessage: str = "Unable to decrypt verification result: [{0}] by reason of : [{1}]"
                            numericErrorCode: int = 43001

                        class invalid_birthday(EpicException):
                            """
                            This exception is thrown when the real identity result verification has invalid birthday
                            *errors.com.epicgames.identity.realid.result_verification.invalid_birthday*
                            """
                            errorMessage: str = "Sorry, the real identity result verification has invalid birthday."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class invalid_format(EpicException):
                            """
                            This exception is thrown when the real identity result verification has invalid format
                            *errors.com.epicgames.identity.realid.result_verification.invalid_format*
                            """
                            errorMessage: str = "Sorry, the real identity result verification has invalid format."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class invalid_nationality(EpicException):
                            """
                            This exception is thrown when the real id inationality is invalid
                            *errors.com.epicgames.identity.realid.invalid_nationality*
                            """
                            errorMessage: str = "Sorry, the real id inationality is invalid."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class invalid_response(EpicException):
                            """
                            This exception is thrown when the real identity result verification has invalid response
                            *errors.com.epicgames.identity.realid.result_verification.invalid_response*
                            """
                            errorMessage: str = "Sorry, the real identity result verification has invalid response."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class missing_required_data(EpicException):
                            """
                            This exception is thrown when the real identity result verification is missing required data
                            *errors.com.epicgames.identity.realid.result_verification.missing_required_data*
                            """
                            errorMessage: str = "Sorry, the real identity result verification is missing required data."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class server_error(EpicException):
                            """
                            This exception is thrown when the real identity result verification has server error
                            *errors.com.epicgames.identity.realid.result_verification.server_error*

                            Message Vars:
                             - Request UUID (31d44b64-4db5-4f1d-8909-b7d5afbb67e3)
                            """
                            errorMessage: str = "Sorry an error occurred and we were unable to resolve it (tracking " \
                                                "id: [{0}])"
                            numericErrorCode: int = 1000
                            statusCode: int = 500

                    class timetable:
                        """
                        Parent class for all real identity timetable exceptions
                        """

                        class compulsory_shutdown_time_override(EpicException):
                            """
                            This exception is thrown when the real identity timetable has compulsory shutdown
                            time override
                            *errors.com.epicgames.identity.realid.timetable.compulsory_shutdown_time_override*
                            """
                            errorMessage: str = "Sorry, the real identity has compulsory shutdown."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class no_timetable_for_adult(EpicException):
                            """
                            This exception is thrown when the real identity timetable has no timetable for adult
                            *errors.com.epicgames.identity.realid.timetable.no_timetable_for_adult*
                            """
                            errorMessage: str = "Sorry, the real identity has no timetable for adult."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class wrong_format(EpicException):
                            """
                            This exception is thrown when the real identity timetable has wrong format
                            *errors.com.epicgames.identity.realid.timetable.wrong_format*
                            """
                            errorMessage: str = "Sorry, the real identity timetable has wrong format."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                    class token_verify_failed(EpicException):
                        """
                        This exception is thrown when the real identity token verify failed
                        *errors.com.epicgames.identity.realid.token_verify_failed*
                        """
                        errorMessage: str = "Sorry, the real identity token verify failed."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class under_12(EpicException):
                        """
                        This exception is thrown when the real identity is under 12
                        *errors.com.epicgames.identity.realid.under_12*
                        """
                        errorMessage: str = "Sorry, the real identity is under 12."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class update:
                        """
                        Parent class for all real identity update exceptions
                        """

                        class email_is_used(EpicException):
                            """
                            This exception is thrown when the email is used
                            *errors.com.epicgames.identity.realid.update.email_is_used*
                            """
                            errorMessage: str = "Sorry, the email is used."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

                        class email_not_allowed_for_minors(EpicException):
                            """
                            This exception is thrown when the email is not allowed for minors
                            *errors.com.epicgames.identity.realid.update.email_not_allowed_for_minors*
                            """
                            errorMessage: str = "Sorry, the email is not allowed for minors."
                            numericErrorCode: int = 0
                            originatingService: str = "WEX"
                            statusCode: int = 400

            class launcher:
                """
                Parent class for all launcher exceptions
                """

                class not_entitled(EpicException):
                    """
                    This exception is thrown when the user is missing an entitlement to play the game.
                    *errors.com.epicgames.launcher.not_entitled*
                    """
                    errorMessage: str = "Missing entitlement to play the game"
                    numericErrorCode: int = 30000
                    originatingService: str = "launcher-service"

            class links:
                """
                Parent class for all links exceptions
                """

                class creator_name_required(EpicException):
                    """
                    This exception is thrown when the creator name is required.
                    *errors.com.epicgames.links.creator_name_required*
                    """
                    errorMessage: str = "Creator name is required"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class mcpcataloghelper(EpicException):
                """
                This exception is thrown when the catalog helper fails.
                *errors.com.epicgames.mcpcataloghelper*
                """
                errorMessage: str = "MCPCatalogHelper failed to load catalog"
                numericErrorCode: int = 0
                originatingService: str = "WEX"
                statusCode: int = 400

            class mcpprofilegroup(EpicException):
                """
                This exception is thrown when the profile group fails.
                *errors.com.epicgames.mcpprofilegroup*
                """
                errorMessage: str = "MCPProfileGroup failed to load profile"
                numericErrorCode: int = 0
                originatingService: str = "WEX"
                statusCode: int = 400

                class no_service_permissions(EpicException):
                    """
                    This exception is thrown when the service permissions are missing.
                    *errors.com.epicgames.mcpprofilegroup.no_service_permissions*
                    """
                    errorMessage: str = "Unable to find service permissions for server."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class modules:
                """
                Parent class for all modules exceptions
                """

                class gameplayutils:
                    """
                    Parent class for all gameplay utils exceptions
                    """

                    class recipe_failed(EpicException):
                        """
                        This exception is thrown when the recipe fails.
                        """
                        errorMessage: str = "Insufficient materials to foil this character."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class gamesubcatalog:
                    """
                    Parent class for all game sub catalog exceptions
                    """

                    class gift_recipient_not_eligible(EpicException):
                        """
                        This exception is thrown when the gift recipient is not eligible.
                        *errors.com.epicgames.modules.gamesubcatalog.gift_recipient_not_eligible*
                        """
                        errorMessage: str = "Gift recipient is not eligible to receive this gift"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class purchase_not_allowed(EpicException):
                        """
                        This exception is thrown when the purchase is not allowed.
                        *errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed*

                        Message Vars:
                         - Offer name ([VIRTUAL]1 x Ninja Style for 300 MtxCurrency)
                         - Item (AthenaDance:eid_tourbus)
                         - Quantity (1)
                         - Limit (0)
                        """
                        errorMessage: str = "Could not purchase catalog offer {0}, item {1} x {2} (exceeding the " \
                                            "limit of {3})"
                        numericErrorCode: int = 28004
                        originatingService: str = "WEX"

                    class validation_info_expired(EpicException):
                        """
                        This exception is thrown when the validation info is expired.
                        *errors.com.epicgames.modules.gamesubcatalog.validation_info_expired*
                        """
                        errorMessage: str = "Validation info expired"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class matchmaking:
                    """
                    Parent class for all matchmaking exceptions
                    """

                    class too_few_players(EpicException):
                        """
                        This exception is thrown when there are too few players.
                        *errors.com.epicgames.modules.matchmaking.too_few_players*
                        """
                        errorMessage: str = "Too few players"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class messaging:
                    """
                    Parent class for all messaging exceptions
                    """

                    class cannot_send_to_yourself(EpicException):
                        """
                        This exception is thrown when you cannot send to yourself.
                        *errors.com.epicgames.modules.messaging.cannot_send_to_yourself*
                        """
                        errorMessage: str = "Cannot send to yourself"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class message_not_found(EpicException):
                        """
                        This exception is thrown when the message is not found.
                        *errors.com.epicgames.modules.messaging.message_not_found*
                        """
                        errorMessage: str = "Message not found"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class profile:
                    """
                    Parent class for all profile exceptions
                    """

                    class account_not_found(EpicException):
                        """
                        This exception is thrown when the account is not found.
                        *errors.com.epicgames.modules.profile.account_not_found*
                        """
                        errorMessage: str = "Account not found"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class data_delete_failed(EpicException):
                        """
                        This exception is thrown when the data delete fails.
                        *errors.com.epicgames.modules.profile.data_delete_failed*
                        """
                        errorMessage: str = "Failed to delete data"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class data_move_failed(EpicException):
                        """
                        This exception is thrown when the data move fails.
                        *errors.com.epicgames.modules.profile.data_move_failed*
                        """
                        errorMessage: str = "Failed to move data"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_account_id_param(EpicException):
                        """
                        This exception is thrown when the account id param is invalid.
                        *errors.com.epicgames.modules.profile.invalid_account_id_param*
                        """
                        errorMessage: str = "Invalid account id param"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_payload(EpicException):
                        """
                        This exception is thrown when the payload is invalid.
                        *errors.com.epicgames.modules.profile.invalid_payload*

                        Message Vars:
                         - Command (com.epicgames.fortnite.core.game.commands.QueryProfile)
                         - Reason (Could not deserialize payload for com.epicgames.fortnite.core.game.commands.QueryProfile)
                        """
                        errorMessage: str = "Unable to parse command {0}. {1}"
                        numericErrorCode: int = 12806
                        originatingService: str = "WEX"

                    class invalid_profile_command(EpicException):
                        """
                        This exception is thrown when the profile command is invalid.
                        *errors.com.epicgames.modules.profile.invalid_profile_command*

                        Message Vars:
                         - Command (UnlockRewardNode)
                         - Profile template (player:profile_common_core)
                         - Profile ID (common_core)
                        """
                        errorMessage: str = "{0} is not valid on {1} profiles ({2})"
                        numericErrorCode: int = 12801
                        originatingService: str = "WEX"

                    class invalid_profile_id_param(EpicException):
                        """
                        This exception is thrown when the profile id param is invalid.
                        *errors.com.epicgames.modules.profile.invalid_profile_id_param*
                        """
                        errorMessage: str = "Invalid profile id param"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class operation_not_found(EpicException):
                        """
                        This exception is thrown when the operation is not found.
                        *errors.com.epicgames.modules.profile.operation_not_found*

                        Message Vars:
                         - Operation (UnlockRewardNode)
                        """
                        errorMessage: str = "Operation {0} not found"
                        numericErrorCode: int = 12813
                        originatingService: str = "WEX"

                    class profile_not_found(EpicException):
                        """
                        This exception is thrown when the profile is not found.
                        *errors.com.epicgames.modules.profile.profile_not_found*

                        Message Vars:
                         - Proile ID (profile0)
                        """
                        errorMessage: str = "Profile {0} not found"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class template_not_found(EpicException):
                        """
                        This exception is thrown when the template is not found.
                        *errors.com.epicgames.modules.profile.template_not_found*

                        Message Vars:
                         - Profile Template (profile0)
                        """
                        errorMessage: str = "Template {0} not found"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

            class not_found(EpicException):
                """
                This exception is thrown when the resource is not found.
                *errors.com.epicgames.common.not_found*
                """
                errorMessage: str = "Sorry the resource you were trying to find could not be found"
                numericErrorCode: int = 1004
                statusCode: int = 404

            class not_implemented(EpicException):
                """
                This exception is thrown when the resource is not implemented.
                *errors.com.epicgames.common.not_implemented*
                """
                errorMessage: str = "Sorry this resource has not been implemented yet"
                numericErrorCode: int = 1005
                statusCode: int = 501

            class ogf:
                """
                Parent class for all ogf exceptions
                """

                class sidecar:
                    """
                    Parent class for all ogf sidecar exceptions
                    """

                    class dss(EpicException):
                        """
                        This exception is thrown when the dss is invalid.
                        *errors.com.epicgames.ogf.sidecar.dss*
                        """
                        errorMessage: str = "The DSS is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class inventory(EpicException):
                        """
                        This exception is thrown when the inventory is invalid.
                        *errors.com.epicgames.ogf.sidecar.inventory*
                        """
                        errorMessage: str = "The inventory is invalid"
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

            class online:
                """
                Parent class for all online exceptions
                """

                class generic(EpicException):
                    """
                    This exception is thrown when a generic online exception occurs.
                    *errors.com.epicgames.online.generic*
                    """
                    errorMessage: str = "An error occurred while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class oss:
                """
                Parent class for all online subsystem errors
                """

                class accountmapping(EpicException):
                    """
                    Parent class for account mapping errors
                    *errors.com.epicgames.oss.accountmapping*
                    """
                    errorMessage: str = "An error occurred with account mapping while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class availability(EpicException):
                    """
                    Parent class for availability errors
                    *errors.com.epicgames.oss.availability*
                    """
                    errorMessage: str = "An error occurred with availability while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class catalog(EpicException):
                    """
                    Parent class for catalog errors
                    *errors.com.epicgames.oss.catalog*
                    """
                    errorMessage: str = "An error occurred with the catalog while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class chat(EpicException):
                    """
                    Parent class for chat errors
                    *errors.com.epicgames.oss.chat*
                    """
                    errorMessage: str = "An error occurred with chat while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class entitlements(EpicException):
                    """
                    Parent class for entitlement errors
                    *errors.com.epicgames.oss.entitlements*
                    """
                    errorMessage: str = "An error occurred with entitlements while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class eula(EpicException):
                    """
                    Parent class for eula errors
                    *errors.com.epicgames.oss.eula*
                    """
                    errorMessage: str = "An error occurred with eula while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class externalui(EpicException):
                    """
                    Parent class for externalui errors
                    *errors.com.epicgames.oss.externalui*
                    """
                    errorMessage: str = "An error occurred with externalui while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class friend(EpicException):
                    """
                    Parent class for friend errors
                    *errors.com.epicgames.oss.friend*
                    """
                    errorMessage: str = "An error occurred with friend while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class gameaccess(EpicException):
                    """
                    Parent class for gameaccess errors
                    *errors.com.epicgames.oss.gameaccess*
                    """
                    errorMessage: str = "You do not have permission to access this game."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class gameservicemcp(EpicException):
                    """
                    Parent class for gameservicemcp errors
                    *errors.com.epicgames.oss.gameservicemcp*
                    """
                    errorMessage: str = "An error occurred with gameservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class groups(EpicException):
                    """
                    Parent class for groups errors
                    *errors.com.epicgames.oss.groups*
                    """
                    errorMessage: str = "An error occurred with groups while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class identity(EpicException):
                    """
                    Parent class for identity errors
                    *errors.com.epicgames.oss.identity*
                    """
                    errorMessage: str = "An error occurred with identity while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class images(EpicException):
                    """
                    Parent class for images errors
                    *errors.com.epicgames.oss.images*
                    """
                    errorMessage: str = "An error occurred with images while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class links(EpicException):
                    """
                    Parent class for links errors
                    *errors.com.epicgames.oss.links*
                    """
                    errorMessage: str = "An error occurred with links while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class messages(EpicException):
                    """
                    Parent class for messages errors
                    *errors.com.epicgames.oss.messages*
                    """
                    errorMessage: str = "An error occurred with messages while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlineaccessmcp(EpicException):
                    """
                    Parent class for onlineaccessmcp errors
                    *errors.com.epicgames.oss.onlineaccessmcp*
                    """
                    errorMessage: str = "An error occurred with onlineaccessmcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlineaffiliatemcp(EpicException):
                    """
                    Parent class for onlineaffiliatemcp errors
                    *errors.com.epicgames.oss.onlineaffiliatemcp*
                    """
                    errorMessage: str = "An error occurred with onlineaffiliatemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinebuildinfoservicemcpv2(EpicException):
                    """
                    Parent class for onlinebuildinfoservicemcpv2 errors
                    *errors.com.epicgames.oss.onlinebuildinfoservicemcpv2*
                    """
                    errorMessage: str = "An error occurred with onlinebuildinfoservicemcpv2 while processing your " \
                                        "request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinechannelsservicemcp(EpicException):
                    """
                    Parent class for onlinechannelsservicemcp errors
                    *errors.com.epicgames.oss.onlinechannelsservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinechannelsservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinecoderedemptionservicemcp(EpicException):
                    """
                    Parent class for onlinecoderedemptionservicemcp errors
                    *errors.com.epicgames.oss.onlinecoderedemptionservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinecoderedemptionservicemcp while processing your " \
                                        "request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlineconnectionstatusmcp(EpicException):
                    """
                    Parent class for onlineconnectionstatusmcp errors
                    *errors.com.epicgames.oss.onlineconnectionstatusmcp*
                    """
                    errorMessage: str = "An error occurred with onlineconnectionstatusmcp while processing your " \
                                        "request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinecontentcontrolsservicemcp(EpicException):
                    """
                    Parent class for onlinecontentcontrolsservicemcp errors
                    *errors.com.epicgames.oss.onlinecontentcontrolsservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinecontentcontrolsservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinedatastorageservicemcp(EpicException):
                    """
                    Parent class for onlinedatastorageservicemcp errors
                    *errors.com.epicgames.oss.onlinedatastorageservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinedatastorageservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinedevicenotificationservicemcp(EpicException):
                    """
                    Parent class for onlinedevicenotificationservicemcp errors
                    *errors.com.epicgames.oss.onlinedevicenotificationservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinedevicenotificationservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinediscovery(EpicException):
                    """
                    Parent class for onlinediscovery errors
                    *errors.com.epicgames.oss.onlinediscovery*
                    """
                    errorMessage: str = "An error occurred with onlinediscovery while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlineeventsservicemcp(EpicException):
                    """
                    Parent class for onlineeventsservicemcp errors
                    *errors.com.epicgames.oss.onlineeventsservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlineeventsservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinefulfillmentservice(EpicException):
                    """
                    Parent class for onlinefulfillmentservice errors
                    *errors.com.epicgames.oss.onlinefulfillmentservice*
                    """
                    errorMessage: str = "An error occurred with onlinefulfillmentservice while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinegiftservicemcp(EpicException):
                    """
                    Parent class for onlinegiftservicemcp errors
                    *errors.com.epicgames.oss.onlinegiftservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinegiftservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinehandoverservicemcp(EpicException):
                    """
                    Parent class for onlinehandoverservicemcp errors
                    *errors.com.epicgames.oss.onlinehandoverservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinehandoverservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinemeshemcp(EpicException):
                    """
                    Parent class for onlinemeshemcp errors
                    *errors.com.epicgames.oss.onlinemeshemcp*
                    """
                    errorMessage: str = "An error occurred with onlinemeshemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinemessagestorageservicemcp(EpicException):
                    """
                    Parent class for onlinemessagestorageservicemcp errors
                    """
                    errorMessage: str = "An error occurred with onlinemessagestorageservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinesidecarmcp(EpicException):
                    """
                    Parent class for onlinesidecarmcp errors
                    *errors.com.epicgames.oss.onlinesidecarmcp*
                    """
                    errorMessage: str = "An error occurred with onlinesidecarmcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinesocialbanservicemcp(EpicException):
                    """
                    Parent class for onlinesocialbanservicemcp errors
                    *errors.com.epicgames.oss.onlinesocialbanservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinesocialbanservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinestats(EpicException):
                    """
                    Parent class for onlinestats errors
                    *errors.com.epicgames.oss.onlinestats*
                    """
                    errorMessage: str = "An error occurred with onlinestats while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                    class disabled(EpicException):
                        """
                        This error is returned when the stats service is disabled.
                        *errors.com.epicgames.oss.onlinestats.disabled*
                        """
                        errorMessage: str = "Stats are disabled."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_leaderboard_specified(EpicException):
                        """
                        This error is returned when the leaderboard specified is invalid.
                        *errors.com.epicgames.oss.onlinestats.invalid_leaderboard_specified*
                        """
                        errorMessage: str = "Invalid leaderboard specified."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class invalid_user_specified(EpicException):
                        """
                        This error is returned when the user specified is invalid.
                        *errors.com.epicgames.oss.onlinestats.invalid_user_specified*
                        """
                        errorMessage: str = "Invalid user specified."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class no_stats_specified(EpicException):
                        """
                        This error is returned when no stats are specified.
                        *errors.com.epicgames.oss.onlinestats.no_stats_specified*
                        """
                        errorMessage: str = "No stats specified."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class no_users_specified(EpicException):
                        """
                        This error is returned when no users are specified.
                        *errors.com.epicgames.oss.onlinestats.no_users_specified*
                        """
                        errorMessage: str = "No users specified."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class payload_empty(EpicException):
                        """
                        This error is returned when the payload is empty.
                        *errors.com.epicgames.oss.onlinestats.payload_empty*
                        """
                        errorMessage: str = "Payload is empty."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                    class request_failed(EpicException):
                        """
                        This error is returned when the request failed.
                        *errors.com.epicgames.oss.onlinestats.request_failed*
                        """
                        errorMessage: str = "Request failed."
                        numericErrorCode: int = 0
                        originatingService: str = "WEX"
                        statusCode: int = 400

                class onlinestatsingestionservicemcp(EpicException):
                    """
                    Parent class for onlinestatsingestionservicemcp errors
                    *errors.com.epicgames.oss.onlinestatsingestionservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinestatsingestionservicemcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinestompconnectionmanagermcp(EpicException):
                    """
                    Parent class for onlinestompconnectionmanagermcp errors
                    *errors.com.epicgames.oss.onlinestompconnectionmanagermcp*
                    """
                    errorMessage: str = "An error occurred with onlinestompconnectionmanagermcp while processing " \
                                        "your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinetime(EpicException):
                    """
                    Parent class for onlinetime errors
                    *errors.com.epicgames.oss.onlinetime*
                    """
                    errorMessage: str = "An error occurred with onlinetime while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class onlinetssproxyservicemcp(EpicException):
                    """
                    Parent class for onlinetssproxyservicemcp errors
                    *errors.com.epicgames.oss.onlinetssproxyservicemcp*
                    """
                    errorMessage: str = "An error occurred with onlinetssproxyservicemcp while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class orders(EpicException):
                    """
                    Parent class for orders errors
                    *errors.com.epicgames.oss.orders*
                    """
                    errorMessage: str = "An error occurred with orders while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class party(EpicException):
                    """
                    Parent class for party errors
                    *errors.com.epicgames.oss.party*
                    """
                    errorMessage: str = "An error occurred with party while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class payment(EpicException):
                    """
                    Parent class for payment errors
                    *errors.com.epicgames.oss.payment*
                    """
                    errorMessage: str = "An error occurred with payment while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class presence(EpicException):
                    """
                    Parent class for presence errors
                    *errors.com.epicgames.oss.presence*
                    """
                    errorMessage: str = "An error occurred with presence while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class priceengine(EpicException):
                    """
                    Parent class for priceengine errors
                    *errors.com.epicgames.oss.priceengine*
                    """
                    errorMessage: str = "An error occurred with priceengine while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class purchase(EpicException):
                    """
                    Parent class for purchase errors
                    *errors.com.epicgames.oss.purchase*
                    """
                    errorMessage: str = "An error occurred with purchase while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class session(EpicException):
                    """
                    Parent class for session errors
                    *errors.com.epicgames.oss.session*
                    """
                    errorMessage: str = "An error occurred with session while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class store(EpicException):
                    """
                    Parent class for store errors
                    *errors.com.epicgames.oss.store*
                    """
                    errorMessage: str = "An error occurred with store while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class titlefile(EpicException):
                    """
                    Parent class for titlefile errors
                    *errors.com.epicgames.oss.titlefile*
                    """
                    errorMessage: str = "An error occurred with titlefile while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class turnauth(EpicException):
                    """
                    Parent class for turnauth errors
                    *errors.com.epicgames.oss.turnauth*
                    """
                    errorMessage: str = "An error occurred with turnauth while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class usercloud(EpicException):
                    """
                    Parent class for usercloud errors
                    *errors.com.epicgames.oss.usercloud*
                    """
                    errorMessage: str = "An error occurred with usercloud while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class users(EpicException):
                    """
                    Parent class for users errors
                    *errors.com.epicgames.oss.users*
                    """
                    errorMessage: str = "An error occurred with users while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class waitingroom(EpicException):
                    """
                    Parent class for waitingroom errors
                    *errors.com.epicgames.oss.waitingroom*
                    """
                    errorMessage: str = "An error occurred with waitingroom while processing your request."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class purchase:
                """
                Parent class for all purchase exceptions
                """

                class no_new_entitlements_found(EpicException):
                    """
                    This error is returned when the user has no new entitlements to redeem
                    *errors.com.epicgames.purchase.no_new_entitlements_found*
                    """
                    errorMessage: str = "No new entitlements found"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class redemption_failed(EpicException):
                    """
                    This error is returned when the user has no new entitlements to redeem
                    *errors.com.epicgames.purchase.redemption_failed*
                    """
                    errorMessage: str = "Redemption failed"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

            class server_error(EpicException):
                """
                This error is returned when an internal server error occurs
                *errors.com.epicgames.server_error*

                Message Vars:
                 - Request UUID (31d44b64-4db5-4f1d-8909-b7d5afbb67e3)
                """
                errorMessage: str = "Sorry an error occurred and we were unable to resolve it (tracking " \
                                    "id: [{0}])"
                numericErrorCode: int = 1000
                originatingService: str = "unknown"
                statusCode: int = 500

            class service_unavailable(EpicException):
                """
                This error is returned when the service is unavailable
                *errors.com.epicgames.service_unavailable*
                """
                errorMessage: str = "Sorry, the service is temporarily unavailable."
                numericErrorCode: int = 0
                originatingService: str = "WEX"
                statusCode: int = 503

            class social:
                """
                Parent class for all social exceptions
                """

                class activity:
                    """
                    Parent class for all social activity exceptions
                    """

                    class account_not_found(EpicException):
                        """
                        This error is returned when the account is not found
                        *errors.com.epicgames.social.activity.account_not_found*
                        """
                        errorMessage: str = "Account not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class bad_request:
                        """
                        Parent class for all social activity bad request exceptions
                        """

                        class likes_feed_not_supported(EpicException):
                            """
                            This error is returned when the likes feed is not supported
                            *errors.com.epicgames.social.activity.bad_request.likes_feed_not_supported*
                            """
                            errorMessage: str = "Likes feed not supported"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 400

                    class conflict:
                        """
                        Parent class for all social activity conflict exceptions
                        """

                        class concurrent_post_modification(EpicException):
                            """
                            This error is returned when the post is being modified concurrently
                            *errors.com.epicgames.social.activity.conflict.concurrent_post_modification*
                            """
                            errorMessage: str = "Concurrent post modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class subscriptions_limit_reached(EpicException):
                            """
                            This error is returned when the subscriptions limit is reached
                            *errors.com.epicgames.social.activity.conflict.subscriptions_limit_reached*
                            """
                            errorMessage: str = "Subscriptions limit reached"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                    class execution_failed(EpicException):
                        """
                        This error is returned when the execution failed
                        *errors.com.epicgames.social.activity.execution_failed*
                        """
                        errorMessage: str = "Execution failed"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class forbidden:
                        """
                        Parent class for all social activity forbidden exceptions
                        """

                        class account_token_request_only(EpicException):
                            """
                            This error is returned when the account token request is only
                            *errors.com.epicgames.social.activity.forbidden.account_token_request_only*
                            """
                            errorMessage: str = "Account token request only"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class activity_access_forbidden(EpicException):
                            """
                            This error is returned when the activity access is forbidden
                            *errors.com.epicgames.social.activity.forbidden.activity_access_forbidden*
                            """
                            errorMessage: str = "Activity access forbidden"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class channel_post_forbidden(EpicException):
                            """
                            This error is returned when the channel post is forbidden
                            *errors.com.epicgames.social.activity.forbidden.channel_post_forbidden*
                            """
                            errorMessage: str = "Channel post forbidden"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class delete_non_post_activity_forbidden(EpicException):
                            """
                            This error is returned when the delete non post activity is forbidden
                            *errors.com.epicgames.social.activity.forbidden.delete_non_post_activity_forbidden*
                            """
                            errorMessage: str = "Delete non post activity forbidden"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class delete_post_forbidden(EpicException):
                            """
                            This error is returned when the delete post is forbidden
                            *errors.com.epicgames.social.activity.forbidden.delete_post_forbidden*
                            """
                            errorMessage: str = "Delete post forbidden"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class own_channel_unsubscription_forbidden(EpicException):
                            """
                            This error is returned when the own channel unsubscription is forbidden
                            *errors.com.epicgames.social.activity.forbidden.own_channel_unsubscription_forbidden*
                            """
                            errorMessage: str = "Own channel unsubscription forbidden"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                    class friend_not_found(EpicException):
                        """
                        This error is returned when the friend is not found
                        *errors.com.epicgames.social.activity.friend_not_found*
                        """
                        errorMessage: str = "Friend not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class friendship_exist(EpicException):
                        """
                        This error is returned when the friendship exist
                        *errors.com.epicgames.social.activity.friendship_exist*
                        """
                        errorMessage: str = "Friendship exist"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class invalid_arguments(EpicException):
                        """
                        This error is returned when the arguments are invalid
                        *errors.com.epicgames.social.activity.invalid_arguments*
                        """
                        errorMessage: str = "Invalid arguments"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class invalid_credential(EpicException):
                        """
                        This error is returned when the credential is invalid
                        *errors.com.epicgames.social.activity.invalid_credential*
                        """
                        errorMessage: str = "Invalid credential"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class not_found(EpicException):
                        """
                        This error is returned when the activity is not found
                        *errors.com.epicgames.social.activity.not_found*
                        """
                        errorMessage: str = "Not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                        class activity_not_found(EpicException):
                            """
                            This error is returned when the activity is not found
                            *errors.com.epicgames.social.activity.not_found.activity_not_found*
                            """
                            errorMessage: str = "Activity not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class subscription_not_found(EpicException):
                            """
                            This error is returned when the subscription is not found
                            *errors.com.epicgames.social.activity.not_found.subscription_not_found*
                            """
                            errorMessage: str = "Subscription not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class unknown_channel(EpicException):
                            """
                            This error is returned when the channel is unknown
                            *errors.com.epicgames.social.activity.not_found.unknown_channel*
                            """
                            errorMessage: str = "Unknown channel"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                class group:
                    """
                    Parent class for all group errors
                    """

                    class not_found:
                        """
                        Parent class for all group not found errors
                        """

                        class tag(EpicException):
                            """
                            This error is returned when the tag is not found
                            *errors.com.epicgames.social.group.not_found.tag*
                            """
                            errorMessage: str = "Tag not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                class groups:
                    """
                    Parent class for all groups errors
                    """

                    class bad_request:
                        """
                        Parent class for all groups bad request errors
                        """

                        class invalid_metadata_key(EpicException):
                            """
                            This error is returned when the metadata key is invalid
                            *errors.com.epicgames.social.groups.bad_request.invalid_metadata_key*
                            """
                            errorMessage: str = "Invalid metadata key"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 400

                        class user_not_identified(EpicException):
                            """
                            This error is returned when the user is not identified
                            *errors.com.epicgames.social.groups.bad_request.user_not_identified*
                            """
                            errorMessage: str = "User not identified"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 400

                    class conflict:
                        """
                        Parent class for all groups conflict errors
                        """

                        class blocked_user(EpicException):
                            """
                            This error is returned when the user is blocked
                            *errors.com.epicgames.social.groups.conflict.blocked_user*
                            """
                            errorMessage: str = "Blocked user"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class concurrent_group_details_modification(EpicException):
                            """
                            This error is returned when the group details are modified concurrently
                            *errors.com.epicgames.social.groups.conflict.concurrent_group_details_modification*
                            """
                            errorMessage: str = "Concurrent group details modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class concurrent_job_modification(EpicException):
                            """
                            This error is returned when the job is modified concurrently
                            *errors.com.epicgames.social.groups.conflict.concurrent_job_modification*
                            """
                            errorMessage: str = "Concurrent job modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class concurrent_member_info_modification(EpicException):
                            """
                            This error is returned when the member info is modified concurrently
                            *errors.com.epicgames.social.groups.conflict.concurrent_member_info_modification*
                            """
                            errorMessage: str = "Concurrent member info modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class concurrent_metadata_modification(EpicException):
                            """
                            This error is returned when the metadata is modified concurrently
                            *errors.com.epicgames.social.groups.conflict.concurrent_metadata_modification*
                            """
                            errorMessage: str = "Concurrent metadata modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class concurrent_profile_modification(EpicException):
                            """
                            This error is returned when the profile is modified concurrently
                            *errors.com.epicgames.social.groups.conflict.concurrent_profile_modification*
                            """
                            errorMessage: str = "Concurrent profile modification"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class duplicate_name(EpicException):
                            """
                            This error is returned when the name is duplicated
                            *errors.com.epicgames.social.groups.conflict.duplicate_name*
                            """
                            errorMessage: str = "Duplicate name"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class existing_member(EpicException):
                            """
                            This error is returned when the member already exists
                            *errors.com.epicgames.social.groups.conflict.existing_member*
                            """
                            errorMessage: str = "Existing member"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class headcount_limit_exceeded(EpicException):
                            """
                            This error is returned when the headcount limit is exceeded
                            *errors.com.epicgames.social.groups.conflict.headcount_limit_exceeded*
                            """
                            errorMessage: str = "Headcount limit exceeded"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class invite_only_group(EpicException):
                            """
                            This error is returned when the group is invite only
                            *errors.com.epicgames.social.groups.conflict.invite_only_group*
                            """
                            errorMessage: str = "Invite only group"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class membership_limit_exceeded(EpicException):
                            """
                            This error is returned when the membership limit is exceeded
                            *errors.com.epicgames.social.groups.conflict.membership_limit_exceeded*
                            """
                            errorMessage: str = "Membership limit exceeded"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class pending_application(EpicException):
                            """
                            This error is returned when the application is pending
                            *errors.com.epicgames.social.groups.conflict.pending_application*
                            """
                            errorMessage: str = "Pending application"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                        class pending_invitation(EpicException):
                            """
                            This error is returned when the invitation is pending
                            *errors.com.epicgames.social.groups.conflict.pending_invitation*
                            """
                            errorMessage: str = "Pending invitation"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 409

                    class forbidden:
                        """
                        Parent class for all groups forbidden errors
                        """

                        class group_authorize(EpicException):
                            """
                            This error is returned when the group is not authorized
                            *errors.com.epicgames.social.groups.forbidden.group_authorize*
                            """
                            errorMessage: str = "Group authorize"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class job_state(EpicException):
                            """
                            This error is returned when the job state is invalid
                            *errors.com.epicgames.social.groups.forbidden.job_state*
                            """
                            errorMessage: str = "Job state"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                        class private_group(EpicException):
                            """
                            This error is returned when the group is private
                            *errors.com.epicgames.social.groups.forbidden.private_group*
                            """
                            errorMessage: str = "Private group"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 403

                    class not_found:
                        """
                        Parent class for all groups not found errors
                        """

                        class admin(EpicException):
                            """
                            This error is returned when the admin is not found
                            *errors.com.epicgames.social.groups.not_found.admin*
                            """
                            errorMessage: str = "Group admin not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class application(EpicException):
                            """
                            This error is returned when the application is not found
                            *errors.com.epicgames.social.groups.not_found.application*
                            """
                            errorMessage: str = "Group application not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class block(EpicException):
                            """
                            This error is returned when the block is not found
                            *errors.com.epicgames.social.groups.not_found.block*
                            """
                            errorMessage: str = "Group block not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class group(EpicException):
                            """
                            This error is returned when the group is not found
                            *errors.com.epicgames.social.groups.not_found.group*
                            """
                            errorMessage: str = "Group not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class invitation(EpicException):
                            """
                            This error is returned when the invitation is not found
                            *errors.com.epicgames.social.groups.not_found.invitation*
                            """
                            errorMessage: str = "Group invitation not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class member(EpicException):
                            """
                            This error is returned when the member is not found
                            *errors.com.epicgames.social.groups.not_found.member*
                            """
                            errorMessage: str = "Group member not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                        class metadata(EpicException):
                            """
                            This error is returned when the metadata is not found
                            *errors.com.epicgames.social.groups.not_found.metadata*
                            """
                            errorMessage: str = "Group metadata not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

                class party(EpicException):
                    """
                    This error is returned when the party is invalid
                    *errors.com.epicgames.social.party*
                    """
                    errorMessage: str = "Party error"
                    numericErrorCode: int = 0
                    originatingService: str = "party"
                    statusCode: int = 400

                    class account_not_found(EpicException):
                        """
                        This error is returned when the account is not found
                        *errors.com.epicgames.social.party.account_not_found*
                        """
                        errorMessage: str = "Account not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class appid_does_not_match(EpicException):
                        """
                        This error is returned when the appid does not match
                        *errors.com.epicgames.social.party.appid_does_not_match*
                        """
                        errorMessage: str = "Appid does not match"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 409

                    class applicant_not_found(EpicException):
                        """
                        This error is returned when the applicant is not found
                        *errors.com.epicgames.social.party.applicant_not_found*
                        """
                        errorMessage: str = "Applicant not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class connection_not_found(EpicException):
                        """
                        This error is returned when the connection is not found
                        *errors.com.epicgames.social.party.connection_not_found*
                        """
                        errorMessage: str = "Connection not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class invalid_connection_offline_ttl(EpicException):
                        """
                        This error is returned when the connection offline ttl is invalid
                        *errors.com.epicgames.social.party.invalid_connection_offline_ttl*
                        """
                        errorMessage: str = "Invalid connection offline ttl"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class invite_already_exists(EpicException):
                        """
                        This error is returned when the invite already exists
                        *errors.com.epicgames.social.party.invite_already_exists*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                         - Party ID (9c76a6c9ebcc41bc9fe990337646c94e)
                        """
                        errorMessage: str = "Invite for user [{0}] to party [{1}] already exists."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 409

                    class invite_forbidden(EpicException):
                        """
                        This error is returned when the invite is forbidden
                        *errors.com.epicgames.social.party.invite_forbidden*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                         - Party ID (9c76a6c9ebcc41bc9fe990337646c94e)
                        """
                        errorMessage: str = "User [{0}] is not authorized to invite to party [{1}]."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class invite_not_found(EpicException):
                        """
                        This error is returned when the invite is not found
                        *errors.com.epicgames.social.party.invite_not_found*
                        """
                        errorMessage: str = "Invite not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class invite_status_change_forbidden(EpicException):
                        """
                        This error is returned when the invite status change is forbidden
                        *errors.com.epicgames.social.party.invite_status_change_forbidden*
                        """
                        errorMessage: str = "Invite status change forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class member_not_found(EpicException):
                        """
                        This error is returned when the member is not found
                        *errors.com.epicgames.social.party.member_not_found*
                        """
                        errorMessage: str = "Member not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class member_state_change_forbidden(EpicException):
                        """
                        This error is returned when the member state change is forbidden
                        *errors.com.epicgames.social.party.member_state_change_forbidden*
                        """
                        errorMessage: str = "Member state change forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class party_change_forbidden(EpicException):
                        """
                        This error is returned when the party change is forbidden
                        *errors.com.epicgames.social.party.party_change_forbidden*
                        """
                        errorMessage: str = "Party change forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class party_is_full(EpicException):
                        """
                        This error is returned when the party is full
                        *errors.com.epicgames.social.party.party_is_full*
                        """
                        errorMessage: str = "Party is full"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class party_join_forbidden(EpicException):
                        """
                        This error is returned when the party join is forbidden
                        *errors.com.epicgames.social.party.party_join_forbidden*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                         - Party ID (9c76a6c9ebcc41bc9fe990337646c94e)
                        """
                        errorMessage: str = "The user {0} has no right to join party {1}."
                        numericErrorCode: int = 51006
                        originatingService: str = "party"
                        statusCode: int = 403

                    class party_not_found(EpicException):
                        """
                        This error is returned when the party is not found
                        *errors.com.epicgames.social.party.party_not_found*
                        """
                        errorMessage: str = "Party not found"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class party_query_forbidden(EpicException):
                        """
                        This error is returned when the party query is forbidden
                        *errors.com.epicgames.social.party.party_query_forbidden*
                        """
                        errorMessage: str = "Party query forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class ping_forbidden(EpicException):
                        """
                        This error is returned when the ping is forbidden
                        *errors.com.epicgames.social.party.ping_forbidden*
                        """
                        errorMessage: str = "message"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 403

                    class ping_not_found(EpicException):
                        """
                        This error is returned when the ping is not found
                        *errors.com.epicgames.social.party.ping_not_found*
                        """
                        errorMessage: str = "message"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 404

                    class response:
                        """
                        Parent class for all party response responses
                        """

                        class missing_required_fields(EpicException):
                            """
                            This error is returned when the response is missing required fields
                            *errors.com.epicgames.social.party.response.missing_required_fields*
                            """
                            errorMessage: str = "Missing required fields"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 400

                    class self_ping(EpicException):
                        """
                        This error is returned when the self ping is forbidden
                        *errors.com.epicgames.social.party.self_ping*
                        """
                        errorMessage: str = "Self ping forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class stale_revision(EpicException):
                        """
                        This error is returned when the revision is stale

                        Message Vars:
                         - Revision ()
                        """
                        errorMessage: str = "Revision {0} is stale."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class too_many_connections(EpicException):
                        """
                        This error is returned when there are too many connections
                        *errors.com.epicgames.social.party.too_many_connections*
                        """
                        errorMessage: str = "Too many connections"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class user_already_in_party(EpicException):
                        """
                        This error is returned when the user is already in a party
                        *errors.com.epicgames.social.party.user_already_in_party*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                         - Demployment ID (fortnite)
                        """
                        errorMessage: str = "User [{0}] is already in a party with deployment id [{1}]."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class user_has_no_party(EpicException):
                        """
                        This error is returned when the user has no party
                        *errors.com.epicgames.social.party.user_has_no_party*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                        """
                        errorMessage: str = "User [{0}] has no party."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                    class user_has_party(EpicException):
                        """
                        This error is returned when the user has a party
                        *errors.com.epicgames.social.party.user_has_party*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                         - Deployment ID (fortnite)
                        """
                        errorMessage: str = "User [{0}] is already in a party with deployment id [{1}]."
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 409

                    class user_is_offline(EpicException):
                        """
                        This error is returned when the user is offline
                        *errors.com.epicgames.social.party.user_is_offline*

                        Message Vars:
                         - User ID (0fc2397a34c1407ca539d39c0921d647)
                        """
                        errorMessage: str = "User [{0}] is offline."
                        numericErrorCode: int = 51024
                        originatingService: str = "party"

                    class user_operation_forbidden(EpicException):
                        """
                        This error is returned when the user operation is forbidden
                        *errors.com.epicgames.social.party.user_operation_forbidden*
                        """
                        errorMessage: str = "User operation forbidden"
                        numericErrorCode: int = 0
                        originatingService: str = "party"
                        statusCode: int = 400

                class repolink:
                    """
                    Parent class for all repolink responses
                    """

                    class not_found:
                        """
                        Parent class for all repolink not found responses
                        """

                        class repo_not_found(EpicException):
                            """
                            This error is returned when the repo is not found
                            """
                            errorMessage: str = "Repo not found"
                            numericErrorCode: int = 0
                            originatingService: str = "party"
                            statusCode: int = 404

            class unauthorized(EpicException):
                """
                This error is returned when the user is not authorized to perform the requested operation.
                *errors.com.epicgames.unauthorized*
                """
                errorMessage: str = "You are not authorized to perform this action."
                numericErrorCode: int = 0
                originatingService: str = "WEX"
                statusCode: int = 401

            class unknown_error(EpicException):
                """
                This error is returned when an unknown error has occurred.
                *errors.com.epicgames.unknown_error*
                """
                errorMessage: str = "An unknown server error has occurred. Please report to admin."
                intent: str = None

                class v2(EpicException):
                    """
                    This error is returned when an unknown error has occurred.
                    *errors.com.epicgames.unknown_error.v2*
                    """
                    errorMessage: str = "An unknown server error has occurred. Please report to admin."
                    intent: str = None

            class unsupported_media_type(EpicException):
                """
                This error is returned when the request is not supported.
                *errors.com.epicgames.unsupported_media_type*
                """
                errorMessage: str = "Sorry your request could not be processed as you are supplying a media type we " \
                                    "do not support."
                numericErrorCode: int = 1006
                originatingService: str = "WEX"
                statusCode: int = 415

            class validation:
                """
                Parent class for all validation errors
                """

                class validation_failed(EpicException):
                    """
                    This error is returned when validation fails.
                    *errors.com.epicgames.validation_failed*

                    Message Vars:
                     - Invalid Field name (display_name)
                    """
                    errorMessage: str = "Validation Failed. Invalid fields were {0}"
                    numericErrorCode: int = 1040
                    validationFailures: dict = {}

            class world_explorers:
                """
                Parent class for all Battle Breakers errors
                """

                class bad_request(EpicException):
                    """
                    This error is returned when the request is malformed.
                    *errors.com.epicgames.world_explorers.bad_request*
                    """
                    errorMessage: str = "Does not meet minimum requirements."
                    numericErrorCode: int = 92014
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class banned_access_found_when_granting(EpicException):
                    """
                    This error is returned when the user is banned.
                    *errors.com.epicgames.world_explorers.banned_access_found_when_granting*
                    """
                    errorMessage: str = "Client requested access grant but has banned access entitlement."
                    numericErrorCode: int = 16156
                    originatingService: str = "WEX"
                    statusCode: int = 403

                class friend_limit_exceeded(EpicException):
                    """
                    This error is returned when the user has too many friends.
                    *errors.com.epicgames.world_explorers.friend_limit_exceeded*
                    """
                    errorMessage: str = "You've exceeded your friend limit."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class invalid_friend(EpicException):
                    """
                    This error is returned when a friend is invalid.
                    *errors.com.epicgames.world_explorers.invalid_friend*
                    """
                    errorMessage: str = "Unable load level due to missing Friend Commander, perhaps they unfriended " \
                                        "you?"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class level_in_progress(EpicException):
                    """
                    This error is returned when the user has another level in progress.
                    *errors.com.epicgames.world_explorers.level_in_progress*
                    """
                    errorMessage: str = "You already have another level in progress."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class level_not_found(EpicException):
                    """
                    This error is returned when the level is not found.
                    *errors.com.epicgames.world_explorers.level_not_found*
                    """
                    errorMessage: str = "Mcp does not recognize this level."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class level_requirements_not_met(EpicException):
                    """
                    This error is returned when the user does not meet the requirements to play the level.
                    *errors.com.epicgames.world_explorers.level_requirements_not_met*
                    """
                    errorMessage: str = "You do not meet the requirements to play this level."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class login_reward_not_available(EpicException):
                    """
                    This error is returned when the login reward is not available.
                    *errors.com.epicgames.world_explorers.login_reward_not_available*

                    Message Vars:
                     - Next Day (2)
                     - Next available time (2022-01-01T00:00:00.000Z)
                    """
                    errorMessage: str = "{0} day login reward not available until {1}"
                    numericErrorCode: int = 92030
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class manifest_out_of_date(EpicException):
                    """
                    This error is returned when the manifest is out of date.
                    *errors.com.epicgames.world_explorers.manifest_out_of_date*
                    """
                    errorMessage: str = "A content update is required before starting a mew level. May we apply it " \
                                        "meow?"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class no_matchmaking_id(EpicException):
                    """
                    This error is returned when the matchmaking id is not found.
                    *errors.com.epicgames.world_explorers.no_matchmaking_id*
                    """
                    errorMessage: str = "Opponent has not joined matchmaking yet"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class not_enough_energy(EpicException):
                    """
                    This error is returned when the user does not have enough energy to play the level.
                    *errors.com.epicgames.world_explorers.not_enough_energy*
                    """
                    errorMessage: str = "You do not have enough energy to play this level."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class not_found(EpicException):
                    """
                    This error is returned when something is not found.
                    *errors.com.epicgames.world_explorers.not_found*
                    """
                    # We're sorry, but we were unable to sell your item as it was not found in your inventory.
                    errorMessage: str = "Sorry, we were unable to find any friends with that search criteria"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 404

                class over_hero_limit(EpicException):
                    """
                    This error is returned when the user has too many heroes.
                    *errors.com.epicgames.world_explorers.over_hero_limit*
                    """
                    errorMessage: str = "You have too many heroes in your inventory. Please remove some before " \
                                        "attempting to play this level."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class purchase_limit_exceeded(EpicException):
                    """
                    This error is returned when the user has exceeded the purchase limit.
                    *errors.com.epicgames.world_explorers.purchase_limit_exceeded*

                    Message Vars:
                     - Item (AthenaDance:eid_tourbus)
                     - Quantity (1)
                     - Limit (0)
                    """
                    errorMessage: str = "Unable to purchase {0} x +{1} limit increase. This would exceed the max of {2}"
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class service_not_required(EpicException):
                    """
                    This error is returned when the service is not required.
                    *errors.com.epicgames.world_explorers.service_not_required*
                    """
                    errorMessage: str = "Already joined matchmaking."
                    numericErrorCode: int = 92006
                    originatingService: str = "WEX"

            class xmpp:
                """
                Parent error class for XMPP errors.
                """

                class connection(EpicException):
                    """
                    This error is returned when there is a connection error.
                    *errors.com.epicgames.xmpp.connection*
                    """
                    errorMessage: str = "Unable to connect to XMPP server."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class server_error(EpicException):
                    """
                    This error is returned when there is a server error.
                    *errors.com.epicgames.xmpp.server_error*
                    """
                    errorMessage: str = "XMPP server error."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400

                class timeout(EpicException):
                    """
                    This error is returned when there is a timeout error.
                    *errors.com.epicgames.xmpp.timeout*
                    """
                    errorMessage: str = "XMPP server timeout."
                    numericErrorCode: int = 0
                    originatingService: str = "WEX"
                    statusCode: int = 400


if __name__ == "__main__":
    try:
        raise errors.com.epicgames.server_error()
    except EpicException as e:
        print(e.as_dict())
