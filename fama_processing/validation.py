'''
validation.py

CREATED:   21.01.2021 10:40
EDITED:    21.01.2021 10:40
PROJECT:   fama_processing
AUTHOR:    Noah Kamara (developer@noahkamara.com)
LICENSE:   Mozilla Public License 2.0
COPYRIGHT: Noah Kamara
'''


from pydantic import BaseModel, validator, AnyUrl
from typing import Optional

class UrlValidator(BaseModel):
    """Validator for URLs"""
    url: AnyUrl


class Validation:
    """ Class for Validation """

    class Result:
        """Validation Result

            valid (str) : Whether the Validation was successful
            error (Optional, str) : Reason for the failure   Default: None
        """
        valid: bool
        error: Optional[str] = None

        def __init__(self, valid: bool, error: Optional[str] = None):
            self.valid = valid
            self.error = error

        @staticmethod
        def success() -> 'Validation.Result':
            """Successful Validation

            Returns:
                Validation.Result: Result of the Validation
            """
            return Validation.Result(valid=True, error=None)

        @staticmethod
        def failure(error: str) -> 'Validation.Result':
            """Failed Validation

            Returns:
                Validation.Result: Result of the Validation
            """
            return Validation.Result(valid=False, error=error)

    @classmethod
    def validate_url(cls, string: str) -> 'Validation.Result':
        """ Validates the URL given as String and 
            returns true if it is valid

        Args:
            string (str): URL in string representation

        Returns:
            bool: Validation Result
        """
        try:
            UrlValidator(url=string)
            return Validation.Result.success()
        except ValidationError as e:
            return Validation.Result.failure(str(e))