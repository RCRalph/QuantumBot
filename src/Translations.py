class Translations:
    WEEKDAYS = {
        "EN": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ],
        "PL": [
            "Poniedziałek",
            "Wtorek",
            "Środa",
            "Czwartek",
            "Piątek",
            "Sobota",
            "Niedziela"
        ]
    }

    TRANSLATIONS = {
        "EN": {
            "reminder": "Reminder!",
            "schedule": "Schedule",
            "schedule-today": "Today's schedule",
            "schedule-empty": "Schedule is empty",
            "schedule-today-empty": "Today's schedule is empty!",
            "available-commands": "Available commands",
            "help": "Help",
            "help-description": "Show available commands",
            "hello-description": "Greet the user",
            "schedule-description": "Show today's schedule",
            "schedule-full-description": "Show full schedule",
            "task": "Task",
            "test": "If you can see this message and it's in the expected language, that means the configuration is correct!",
            "deadlines": "Deadlines",
            "deadlines-empty": "Deadlines are empty",
        },
        "PL": {
            "reminder": "Przypomnienie!",
            "schedule": "Harmonogram",
            "schedule-today": "Dzisiejszy harmonogram",
            "schedule-empty": "Harmonogram jest pusty",
            "schedule-today-empty": "Dzisiejszy harmonogram jest pusty!",
            "available-commands": "Dostępne polecenia",
            "help": "Pomoc",
            "help-description": "Pokaż dostępne polecenia",
            "hello-description": "Powitaj użytkownika",
            "schedule-description": "Pokaż dzisiejszy harmonogram",
            "schedule-full-description": "Pokaż pełny harmonogram",
            "task": "Zadanie",
            "test": "Jeśli widzisz tę wiadomość oraz jest ona w oczekiwanym języku, to znaczy że konfiguracja jest poprawna!",
            "deadlines": "Terminy",
            "deadlines-empty": "Terminy są puste",
        },
    }

    language = "EN"

    def __init__(self, language: str):
        if language not in self.languages():
            raise KeyError(f"Language {language} doesn't exist")

        self.language = language

    @staticmethod
    def languages():
        return list(Translations.WEEKDAYS.keys())

    def keys(self):
        return list(Translations.TRANSLATIONS[self.language].keys())

    def get_weekday(self, weekday_index: int):
        if weekday_index not in range(len(Translations.WEEKDAYS[self.language])):
            raise KeyError(f"Weekday {weekday_index} doesn't exist in {self.language}")

        return Translations.WEEKDAYS[self.language][weekday_index]

    def get_translation(self, key: str):
        if key not in Translations.TRANSLATIONS[self.language]:
            raise KeyError(f"{key} doesn't exist in {self.language}")

        return Translations.TRANSLATIONS[self.language][key]
