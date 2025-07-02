from entities.country import Country, CountryTranslateData
from enums import LanguageEnum
from pytest import fixture, mark
from repositories.country_repository import CountryRepository


@fixture(scope="function")
def country_repository(async_session):
    return CountryRepository(session=async_session)


class TestCountryRepository:
    @mark.asyncio
    async def test_create_country(
        self,
        country_repository: CountryRepository,
        country: Country = Country(country_id=1),
        country_translate: CountryTranslateData = CountryTranslateData(
            country_id=1,
            name="Test data1",
            language_id=LanguageEnum.RUSSIAN,
        ),
    ):
        result = await country_repository.create_country(country=country, country_translate_data=country_translate)

        assert (country, country_translate) == result

    @mark.asyncio
    async def test_create_country2(
        self,
        country_repository: CountryRepository,
        country: Country = Country(country_id=2),
        country_translate: CountryTranslateData = CountryTranslateData(
            country_id=2,
            name="Test data2",
            language_id=LanguageEnum.RUSSIAN,
        ),
    ):
        result = await country_repository.create_country(country=country, country_translate_data=country_translate)
        assert (country, country_translate) == result
