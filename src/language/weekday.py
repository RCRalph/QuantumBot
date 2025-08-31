from datetime import date

from pydantic import BaseModel, ConfigDict


class Weekday(BaseModel):
    model_config = ConfigDict(frozen=True)

    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str

    def to_list(self) -> list[str]:
        return [
            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday,
        ]

    def from_date(self, date_value: date) -> str:
        return self.to_list()[date_value.weekday()]
