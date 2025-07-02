"""
The file contains the test data for database.
This file have been creating like the db/dependencies/base_statements.py file.
"""

from sqlalchemy import insert

from enums import LanguageEnum
from models import Country, Language
from statement import Statement
from tests.constants import (
    BELARUS_ID,
    RUSSIA_ID,
)

# Tuple of insert statements for initial **test** data loading
TEST_STATEMENTS: tuple[Statement, ...] = (
    Statement(
        description="Insert language 'ru'",
        statement=insert(Language),
        data={"language_id": LanguageEnum.RUSSIAN, "name": "Russian"},
        check_query=lambda session: session.query(Language).filter_by(country_id=LanguageEnum.RUSSIAN).first(),
    ),
    Statement(
        description="Insert country 'Russia'",
        statement=insert(Country),
        data={"country_id": RUSSIA_ID},
        check_query=lambda session: session.query(Country).filter_by(country_id=RUSSIA_ID).first(),
    ),
    Statement(
        description="Insert country 'Belarus'",
        statement=insert(Country),
        data={"country_id": BELARUS_ID},
        check_query=lambda session: session.query(Country).filter_by(country_id=BELARUS_ID).first(),
    ),
)


def get_test_statements() -> tuple[Statement, ...]:
    """
    Return the base statements for database configuration (for first startup)
    """
    return TEST_STATEMENTS
