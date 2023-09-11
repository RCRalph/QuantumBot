import os, json, datetime
from src.Validator import Validator
from src.Formats import Formats
from src.Translations import Translations
from src.Server import Server

class Servers:
    DIRECTORY = "servers"
    servers: dict[int, Server] = {}

    def __init__(self):
        files = [item for item in os.listdir(self.DIRECTORY) if self.is_json_file(item)]

        invalid_servers, successful_servers = [], []
        for filename in files:
            with open(f"{self.DIRECTORY}/{filename}") as file:
                content = json.load(file)

                if not Validator(file, content, Translations.keys()):
                    invalid_servers.append(filename)
                else:
                    self.servers[content["server_id"]] = Server(content)
                    successful_servers.append(content["name"])

        # Summary
        if successful_servers:
            print("Successfully loaded the following servers:", ", ".join(sorted(successful_servers)))

        if invalid_servers:
            print("Invalid schedule files:", ", ".join(sorted(invalid_servers)))

    def is_json_file(self, filename: str):
        if not (filename.endswith(".json") and os.path.isfile(f"{self.DIRECTORY}/{filename}")):
            return False

        with open(f"{self.DIRECTORY}/{filename}") as file:
            try:
                json.load(file)
                return True
            except:
                print(f"Invalid formatting of file {filename}, should be a JSON file.")
                return False

    def check_for_announcements(self):
        result: list[dict] = []
        current_datetime = datetime.datetime.now(datetime.timezone.utc)

        for server_id in self.servers:
            for date in self.servers[server_id].schedule:
                for event in self.servers[server_id].schedule[date]:
                    for i in event.announcements:
                        timestamp = current_datetime + datetime.timedelta(minutes = i)

                        if timestamp.strftime(Formats.DATETIME) == event.start_UTC:
                            result.append({
                                "server_id": server_id,
                                "channel_id": self.servers[server_id].announcement_channel_id,
                                "name": f"{event.title}: {event.times}" if event.description is not None else event.title,
                                "value": event.description if event.description is not None else event.times
                            })

        return result
