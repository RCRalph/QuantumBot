from enum import StrEnum
from functools import cached_property

from language.language_configuration import LanguageConfiguration


class Language(StrEnum):
    EN = "EN"
    PL = "PL"

    @cached_property
    def config(self) -> LanguageConfiguration:
        return LanguageConfiguration.from_iso_639(self)
