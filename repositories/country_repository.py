from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession

from entities.country import Country, CountryTranslateData
from enums import LanguageEnum
from models import Country as CountryModel
from models import CountryTranslate as CountryTranslateModel
from postgres_helper import postgres_helper


class CountryDBError(Exception):
    """The error ralated to the error with country data in the database."""

    def __init__(
        self,
        message="The error of adding country to the database.",
    ):
        super().__init__(message)


class CountryIntegrityError(Exception):
    """The error occures with attempt to adding
    the country_data or country_translate_dataa wich
    already exists in the database or trying adding the
    depends-data those doesn't exists.
    """

    def __init__(self, message="The integrity error of country data."):
        super().__init__(message)


class CountryDoesNotExistsError(Exception):
    """
    The error occures, while the country wasn't
    exists in the DB
    """

    def __init__(
        self,
        message=("Country with this data doesn't exists."),
    ):
        super().__init__(message)


class CountryRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.__session = session

    async def create_country(
        self,
        country: Country,
        country_translate_data: CountryTranslateData,
    ) -> tuple[Country, CountryTranslateData]:
        """
        Create country model
        (the country data thats doesn't depends of lagnuage)
        """

        country_model = CountryModel(**country.model_dump())
        country_translate_model = CountryTranslateModel(**country_translate_data.model_dump())

        # === main logic ===
        try:
            async with self.__session as session:
                session.add_all((country_model, country_translate_model))
                await session.commit()

            return country, country_translate_data

        # === errors handling ===
        except IntegrityError as error:
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):  # type: ignore
                if "flag" in str(error):
                    # TODO: поменять ошибку на FlagNotExistsError
                    raise CountryIntegrityError(
                        "Can't create country, because the flag" + f" with id {country.flag_id} does't exists."
                    ) from error

                elif "language" in str(error):
                    # TODO: поменять ошибку на LangugeNotExistsError
                    raise CountryIntegrityError(
                        "Can't create country, because the"
                        + f" language {country_translate_data.language_id}"
                        + " does't exists."
                    ) from error

            elif isinstance(error.orig.__cause__, UniqueViolationError):  # type: ignore
                if "name" in str(error):
                    raise CountryIntegrityError(
                        f"Country with name '{country_translate_model.name}'" + " already exists."
                    ) from error

                raise CountryIntegrityError(f"Country with id {country.country_id} already exists.") from error

            raise CountryIntegrityError("Country integrity error. Try to change creation data") from error

        except (DBAPIError, OSError) as error:
            raise CountryDBError from error

    async def create_translate_country_data(
        self,
        country_translate_data: CountryTranslateData,
    ) -> CountryTranslateData:
        """Insert the translate of country.
        The client can add translate only for already exists country"""

        country_translate_model = CountryTranslateModel(**country_translate_data.model_dump())

        # === main logic ===
        try:
            async with self.__session as session:
                session.add(country_translate_model)
                await session.commit()

            return country_translate_data

        # === errors handling ===
        except IntegrityError as error:
            # TODO: разграничить ошибки
            raise CountryIntegrityError from error

        except DBAPIError as error:
            raise CountryDBError from error

    async def is_country_exists(self, country_id: int) -> bool:
        select_stmt = text(
            """
            select true
            from country
            where country_id = :country_id
            """
        )

        try:
            # === main logic ==
            async with self.__session as session:
                result = await session.execute(select_stmt, params={"country_id": country_id})

            return bool(result.one_or_none())

        except DBAPIError as error:
            raise CountryDBError from error

    async def get_country_data(
        self,
        country_id: int,
        language_id: LanguageEnum = LanguageEnum.DEFAULT_LANGUAGE,
    ) -> tuple[Country, CountryTranslateData]:
        """Get country and country_translate data.
        If each of one does't exists raise CountryDoesNotExists exception"""

        select_stmt = text(
            """
            select
              c.country_id,
              f.flag_url,
              ct.name,
              l.language_id
            from country c
            join country_translate ct using(country_id)
            join language l using(language_id)
            join flag f on c.flag_id=f.flag_id
            where country_id=:country_id
                  and language_id = :language_id;
            """
        )
        try:
            # === main logic ===
            async with self.__session as session:
                result = await session.execute(
                    select_stmt,
                    params={
                        "country_id": country_id,
                        "language_id": language_id,
                    },
                )
                await session.commit()

            result = result.mappings().one()

            country = Country(**result)
            country_translate_data = CountryTranslateData(**result)

            return country, country_translate_data

        # === errors handling ===
        except NoResultFound as error:
            raise CountryDoesNotExistsError from error

        except IntegrityError as error:
            raise CountryIntegrityError from error

        except DBAPIError as error:
            raise CountryDBError from error


def country_repository_dependency(
    session: AsyncSession = Depends(postgres_helper.session_dependency),
):
    return CountryRepository(session=session)
