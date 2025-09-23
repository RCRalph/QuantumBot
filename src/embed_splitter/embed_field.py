from pydantic import BaseModel, ConfigDict, Field


class EmbedField(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    value: str
    inline: bool = Field(default=False)

    def __len__(self) -> int:
        return len(self.name) + len(self.value)
