from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from language.embed import Embed
from language.message import Message
from language.weekday import Weekday


class LanguageConfiguration(BaseModel):
    CONFIG_DIRECTORY: ClassVar[Path] = Path.cwd() / "config" / "languages"

    model_config = ConfigDict(frozen=True)

    weekday: Weekday
    message: Message
    embed: Embed

    @classmethod
    def from_iso_639(cls, iso_639: str) -> "LanguageConfiguration":
        config_path = cls.CONFIG_DIRECTORY / f"{iso_639.lower()}.json"
        return cls.model_validate_json(config_path.read_bytes())
