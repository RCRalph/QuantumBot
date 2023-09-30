from zoneinfo import ZoneInfo

class TimezoneData:
    name: str
    text: str
    timezone: ZoneInfo

    def __init__(self, name: str, text: str | None = None):
        self.name = name
        self.timezone = ZoneInfo(name)
        self.text = text if text is not None else name
