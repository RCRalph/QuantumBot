class Event:
    title: str
    start_UTC: str
    end_UTC: str
    times: str
    announcements: list[int]
    description: str | None

    def __init__(
        self,
        title: str,
        start_UTC: str,
        end_UTC: str,
        times: str,
        announcements: list[int],
        description: str | None
    ):
        self.title = title
        self.start_UTC = start_UTC
        self.end_UTC = end_UTC
        self.times = times
        self.announcements = announcements
        self.description = description
