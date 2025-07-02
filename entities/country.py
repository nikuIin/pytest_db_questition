from pydantic import BaseModel, ConfigDict, Field, field_validator

from enums import LanguageEnum


class Country(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)
    country_id: int = Field(gt=0, le=999)
    flag_id: int | None = None


class CountryTranslateData(BaseModel):
    """The country data, those depends of the language. In the other words,
    the data, thats appears in the different ways in every language.

    :country_id — the id of country
    :language_id — the id of language
    :name — the name of country
    """

    country_id: int = Field(gt=0, le=999)
    language_id: LanguageEnum = LanguageEnum.ENGLISH
    name: str = Field(min_length=1, max_length=255)

    @field_validator("name", mode="before")
    @classmethod
    def capitalize_name(cls, name):
        return name.capitalize()
