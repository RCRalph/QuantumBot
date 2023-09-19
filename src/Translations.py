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
            "task": "Task"
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
            "task": "Zadanie"
        },
    }

    @staticmethod
    def get_weekday(language: str, weekday_index: int):
        if language not in Translations.WEEKDAYS:
            raise KeyError(f"Language {language} doesn't exist")
        elif weekday_index not in range(len(Translations.WEEKDAYS[language])):
            raise KeyError(f"Weekday {weekday_index} doesn't exist in {language}")

    @staticmethod
    def get_translation(language: str, key: str):
        if language not in Translations.TRANSLATIONS:
            raise KeyError(f"Language {language} doesn't exist")
        elif key not in Translations.TRANSLATIONS[language]:
            raise KeyError(f"{key} doesn't exist in {language}")

        return Translations.TRANSLATIONS[language][key]

    @staticmethod
    def keys():
        return list(Translations.TRANSLATIONS["EN"].keys())
