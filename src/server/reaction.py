from pydantic import BaseModel, ConfigDict


class Reaction(BaseModel):
    model_config = ConfigDict(frozen=True)

    prompt_text: str
    emojis: list[str]
