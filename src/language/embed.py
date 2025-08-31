from pydantic import BaseModel, ConfigDict


class Embed(BaseModel):
    model_config = ConfigDict(frozen=True)

    reminder: str
    schedule: str
    schedule_today: str
    schedule_empty: str
    schedule_today_empty: str
    available_commands: str
    help: str
    help_description: str
    hello_description: str
    schedule_description: str
    schedule_full_description: str
    task: str
    test: str
