class Deadline:
    title = ""
    time_UTC = ""
    times = ""
    announcements = [600, 300, 120]
    description = None

    def __init__(self, title: str, time_UTC: str, times: str):
        self.title = title
        self.time_UTC = time_UTC
        self.times = times
