# class InvalidPasswordError(Exception):
#     """Raised when login fails due to invalid password."""
#     pass
#
#
# # class MissingDataError(Exception):
# #     """Raised when required field data is missing."""
# #     def __init__(self, field_name):
# #         self.message = f"Missing data in required field: {field_name}"
# #         super().__init__(self.message)
#
# # class ElementNotFoundError(Exception):
# #     pass

import pytest
from utils.custom_exceptions import InvalidPasswordError, MissingDataError

def test_login_invalid_password():
    with pytest.raises(InvalidPasswordError):
        Login(
            username="gedehim917@decodewp.com",
            password="WRONG_PASSWORD",
            link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
        )

def test_login_missing_password():
    with pytest.raises(MissingDataError):
        Login(
            username="gedehim917@decodewp.com",
            password="",
            link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
        )

