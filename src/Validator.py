import pytz, datetime

class Validator:
    filename = ""
    content = dict()
    languages = []

    def __init__(self, filename: str, content: dict, languages: list):
        self.filename = filename
        self.content = content
        self.languages = languages

    def show_error(self, message: str):
        print(f"{self.filename}: {message}")
        return False

    def validate_name(self):
        try:
            if type(self.content["name"]) is not str or not len(self.content["name"]):
                return self.show_error("Property 'name' should be a string")
        except KeyError:
            return self.show_error("Missing 'name' property")

        return True

    def validate_server_id(self):
        try:
            if type(self.content["server_id"]) is not int:
                return self.show_error("Property 'server_id' should be an integer")
        except KeyError:
            return self.show_error("Missing 'server_id' property")

        return True

    def validate_announcement_channel_id(self):
        try:
            if type(self.content["announcement_channel_id"]) is not int:
                return self.show_error("Property 'announcement_channel_id' should be an integer")
        except KeyError:
            return self.show_error("Missing 'announcement_channel_id' property")

        return True

    def validate_language(self):
        try:
            if self.content["language"] not in self.languages:
                return self.show_error("Property 'language' is not a valid language")
        except KeyError:
            return self.show_error("Missing 'language' property")

        return True

    def validate_timezones(self):
        try:
            if type(self.content["timezones"]) is not list:
                return self.show_error("Property 'timezones' should be a list")

            if not len(self.content["timezones"]):
                return self.show_error("Property 'timezones' shouldn't be empty")

            if len(set(self.content["timezones"])) != len(self.content["timezones"]):
                return self.show_error("Property 'timezones' should have unique values")

            for i in self.content["timezones"]:
                if type(i) is not str:
                    return self.show_error("Property 'timezones' should be a list of strings")

                try:
                    pytz.timezone(i)
                except pytz.exceptions.UnknownTimeZoneError:
                    return self.show_error(f"'{i}' isn't a valid timezone")
        except KeyError:
            return self.show_error("Missing 'timezones' property")

        return True

    def validate_schedule_title(self, title):
        if type(title) is not str:
            return self.show_error("Schedule title should be a string")
        elif not len(title):
            return self.show_error("Schedule title shouldn't be empty")

        return True

    def validate_schedule_description(self, schedule_item):
        if "description" not in schedule_item:
            return True

        if type(schedule_item["description"]) is not str:
            return self.show_error(f"Schedule {schedule_item['title']} description should be a string")

        return True

    def validate_schedule_time(self, time, title: str):
        if type(time) is not str:
            return self.show_error(f"Schedule {title} start should be a string")
        else:
            try:
                datetime.datetime.strptime(time, self.DATE_FORMAT)
            except ValueError:
                return self.show_error(f"Schedule {title} start should have a valid format")

        return True

    def validate_schedule_announcements(self, schedule_item):
        if "announcements" not in schedule_item:
            return True

        if type(schedule_item["announcements"]) is not list:
            return self.show_error(f"Schedule {schedule_item['title']} announcements should be a list")

        if len(set(schedule_item["announcements"])) != len(schedule_item["announcements"]):
            return self.show_error(f"Schedule {schedule_item['title']} announcements should have unique values")

        for item in schedule_item["announcements"]:
            if type(item) is not int:
                return self.show_error(f"Schedule {schedule_item['title']} announcements should be a list of integers")

        return True

    def validate_schedule(self):
        try:
            if type(self.content["schedule"]) is not list:
                return self.show_error("Schedule should be a list")

            if not len(self.content["schedule"]):
                return self.show_error("Schedule shouldn't be empty")

            for item in self.content["schedule"]:
                for key in ["title", "start", "end"]:
                    if key not in item:
                        return self.show_error(f"Schedule missing {key}")

                if not (
                    self.validate_schedule_title(item["title"])
                    and self.validate_schedule_time(item["start"])
                    and self.validate_schedule_time(item["end"])

                    # Optional properties
                    and self.validate_schedule_description(item)
                    and self.validate_schedule_announcements(item)
                ): return False

                if item["start"] > item["end"]:
                    return self.show_error(f"Schedule {item['title']} start is after end")
        except KeyError:
            self.show_error("Missing 'schedule' property")

        return True

    def validate(self):
        return (
            self.validate_name()
            and self.validate_server_id()
            and self.validate_announcement_channel_id()
            and self.validate_language()
            and self.validate_timezones()
            and self.validate_schedule()
        )
