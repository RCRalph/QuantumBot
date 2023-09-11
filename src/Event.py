class Event:
    title = ""
    start_UTC = ""
    end_UTC = ""
    times = ""
    announcements = [10]
    description = None

    def __init__(self, title: str, start_UTC: str, end_UTC: str, times: str):
        self.title = title
        self.start_UTC = start_UTC
        self.end_UTC = end_UTC
        self.times = times
