import pytz, datetime, json, os
from src.Translations import Translations
from src.Formats import Formats

class Validator:
    filename: str
    content: dict
    languages = Translations.languages()

    def __init__(self, filename: str, content: dict):
        self.filename = filename
        self.content = content

    @staticmethod
    def is_json_file(directory: str, filename: str):
        if not (filename.endswith(".json") and os.path.isfile(f"{directory}/{filename}")):
            return False

        with open(f"{directory}/{filename}") as file:
            try:
                json.load(file)
                return True
            except:
                print(f"Invalid formatting of file {filename}, should be a JSON file.")
                return False

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

    def validate_workshop_reaction_channel_id(self):
        if "workshop_reaction_channel_id" not in self.content:
            return True

        if type(self.content["workshop_reaction_channel_id"]) is not int:
            return self.show_error("Property 'workshop_reaction_channel_id' should be an integer")

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

    def validate_title(self, title):
        if type(title) is not str:
            return self.show_error("Title should be a string")
        elif not len(title):
            return self.show_error("Title shouldn't be empty")

        return True

    def validate_description(self, item: dict):
        if "description" not in item:
            return True

        if type(item["description"]) is not str:
            return self.show_error(f"Description of {item['title']} should be a string")

        return True

    def validate_time(self, time, title: str):
        if type(time) is not str:
            return self.show_error(f"Time of {title} should be a string")

        try:
            datetime.datetime.strptime(time, Formats.DATETIME)
        except ValueError:
            return self.show_error(f"Time of {title} should have a valid format")

        return True

    def validate_announcements(self, item: dict):
        if "announcements" not in item:
            return True

        if type(item["announcements"]) is not list:
            return self.show_error(f"Announcements of {item['title']} should be a list")

        if len(set(item["announcements"])) != len(item["announcements"]):
            return self.show_error(f"Announcements of {item['title']} should have unique values")

        for i in item["announcements"]:
            if type(i) is not int:
                return self.show_error(f"Announcements of {item['title']} should be a list of integers")

        return True

    def validate_schedule(self):
        if "schedule" not in self.content:
            return True

        if type(self.content["schedule"]) is not list:
            return self.show_error("Schedule should be a list")

        for item in self.content["schedule"]:
            for key in ["title", "start", "end"]:
                if key not in item:
                    return self.show_error(f"Schedule missing {key}")

            if not (
                self.validate_title(item["title"])
                and self.validate_time(item["start"], item["title"])
                and self.validate_time(item["end"], item["title"])

                # Optional properties
                and self.validate_description(item)
                and self.validate_announcements(item)
            ): return False

            if item["start"] > item["end"]:
                return self.show_error(f"Schedule {item['title']} start is after end")

        return True

    def validate_deadlines(self):
        if "deadlines" not in self.content:
            return True

        if type(self.content["deadlines"]) is not list:
            return self.show_error("Deadlines should be a list")

        for item in self.content["deadlines"]:
            for key in ["title", "time"]:
                if key not in item:
                    return self.show_error(f"Deadline missing {key}")

            if not (
                self.validate_title(item["title"])
                and self.validate_time(item["time"], item["title"])

                # Optional properties
                and self.validate_description(item)
                and self.validate_announcements(item)
            ): return False

        return True

    def validate(self):
        return (
            self.validate_name()
            and self.validate_server_id()
            and self.validate_announcement_channel_id()
            and self.validate_language()
            and self.validate_timezones()
            and self.validate_schedule()
            and self.validate_deadlines()
        )
