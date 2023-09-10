class Translations:
    TRANSLATIONS = {
        "EN": {
            "weekdays": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ],
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
        },
        "PL": {
            "weekdays": [
                "poniedziałek",
                "wtorek",
                "środa",
                "czwartek",
                "piątek",
                "sobota",
                "niedziela"
            ],
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
        },
    }

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
