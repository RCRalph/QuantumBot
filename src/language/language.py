from enum import Enum

from language.language_configuration import LanguageConfiguration


class Language(Enum):
    EN = LanguageConfiguration.from_iso_639("en")
    PL = LanguageConfiguration.from_iso_639("pl")
