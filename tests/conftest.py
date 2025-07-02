from pytest_asyncio import fixture as async_fixture

from config import ModeEnum, app_settings
from postgres_helper import postgres_helper
from tests.test_statements import TEST_STATEMENTS


@async_fixture(scope="function")
async def async_session():
    """Fixture to provide a database session for each test."""
    assert app_settings.app_mode == ModeEnum.TEST

    await postgres_helper.clear_data()
    await postgres_helper.create_tables()
    await postgres_helper.insert_base_data(statements=TEST_STATEMENTS)
    async with postgres_helper.session_factory() as session:
        yield session
        await session.rollback()
