# QuantumBot
Discord bot for events organized by Quantum AI Foundation

# Available commands
- `!help` - shows available commands
- `!hello` - greets the user
- `!schedule` - shows the schedule for the current day
- `!schedule-full` - shows the schedule of all events

# Required Discord permissions
- View channel
- Send messages
- Embed links
- Attach files
- Add reactions
- Mention @everyone, @here etc.
- Read message history

# Server file configuration
Adding a server into QuantumBot requires adding a file into the `servers` directory. The file has to be formatted as a `.json` file and have the properties listed in the table below:

| Property name | Required | Type | Description |
| :-----: | :-----: | :-----: | :-----: |
| name | yes | text | Name of the event |
| server_id | yes | integer | ID of the Discord server where the event happens |
| announcement_channel_id | yes | integer | ID of the Discord server channel where QuantumBot should make announcements |
| workshop_reaction_channel_id | no | integer | ID of the Discord server channel where QuantumBot should add reactions to messages in order to track progress |
| language | yes | text | Language of the server |
| timezones | yes | array | List of timezones which QuantumBot should use when showing time, more information available under [timezones configuration](#timezones-configuration) |
| schedule | no | array | List of named periods of time that occur during the event, more information available under [schedule configuration](#schedule-configuration) |
| deadlines | no | array | List of deadlines or named times that occur during the event, more information available under [deadlines configuration](#deadlines-configuration) |

## Timezones configuration
Timezones can be configured in one of two ways:

1. Using plain text value, which contains the timezone name. Information on available timezones can be found by running the code below:
    ```py
    from zoneinfo import available_timezones
    available_timezones()
    ```
    It is recommended to use shortcut timezone names (ex. UTC, CET, PDT) instead of longer variants.

2. Using timezone information object, which contains the timezone name and its customizable alias, which QuantumBot will use as the timezone name:
    | Property name | Required | Type | Description |
    | :-----: | :-----: | :-----: | :-----: |
    | name | yes | text | Name of the timezone, ex. UTC, CET, PDT |
    | text | yes | text | Alias used for the timezone, ex. Warsaw, London |

## Schedule configuration
Schedule events are configured using objects with properties:
| Property name | Required | Type | Description |
| :-----: | :-----: | :-----: | :-----: |
| title | yes | text | Title of the schedule event |
| description | no | text | Description of the event, can contain the speaker's name and affiliation |
| start | yes | text (YYYY-MM-DD HH:MM) | Date and time of the start of the event in UTC |
| end | yes | text (YYYY-MM-DD HH:MM) | Date and time of the end of the event in UTC |
| announcements | no | list of integers | Amount of minutes an announcement about the event should be made before its start, by default it's 10 |

## Deadlines configuration
Deadline events are configured using objects with properties:
| Property name | Required | Type | Description |
| :-----: | :-----: | :-----: | :-----: |
| title | yes | text | Title of the deadline |
| description | no | text | Description of the deadline |
| time | yes | text (YYYY-MM-DD HH:MM) | Date and time of the deadline in UTC |
| announcements | no | list of integers | Amount of minutes an announcement about the event should be made before its start, by default it's 10 |
