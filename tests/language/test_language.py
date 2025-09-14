import pytest

from language.language import Language
from language.language_configuration import LanguageConfiguration


class TestLanguage:
    @pytest.mark.parametrize("language", list(Language))
    def test_value_correctness(self, language: Language) -> None:
        # Assert
        assert language.config == LanguageConfiguration.from_iso_639(language)

    def test_value_uniqueness(self) -> None:
        # Assert
        assert len(Language) == len(set(Language))
