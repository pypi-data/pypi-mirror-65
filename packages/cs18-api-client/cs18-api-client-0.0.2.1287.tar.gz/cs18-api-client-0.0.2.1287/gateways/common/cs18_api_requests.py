"""
Container for Request object used in cs18-api-client
"""
from enum import Enum


class ProductionEnvironment(Enum):
    BLUE = 'blue'
    GREEN = 'green'


class DebuggingServiceValue(Enum):
    ON = 'on'
    OFF = 'off'


class UserSignupRequest:
    def __init__(self, first_name: str, last_name: str, password: str, secret: str):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.secret = secret


class CreateInvitationsRequest:
    def __init__(
            self,
            emails: [],
            account_role: str,
            reason: str,
            space_name: str,
            space_role: str,
    ):
        self.emails = emails
        self.account_role = account_role
        self.reason = reason
        self.space_name = space_name
        self.space_role = space_role


class CreateAccountRequest:
    def __init__(
            self,
            account_name: str,
            first_name: str,
            last_name: str,
            email: str,
            password: str,
            phone_number: str,
    ):
        self.phone_number = phone_number
        self.password = password
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.account_name = account_name


class UpdateSpaceRequest:
    def __init__(self, name: str):
        self.name = name
