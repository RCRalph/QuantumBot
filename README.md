# QuantumBot
Discord bot for events organized by Quantum AI Foundation

# Available commands
- `!help` - shows available commands
- `!hello` - greets the user
- `!agenda` - shows the agenda for the current day
- `!agenda-full` - shows the agenda of all events

## Required Discord permissions
- View channel
- Send messages
- Embed links
- Attach files
- Add reactions
- Mention @everyone, @here etc.
- Read message history

## Schedule file information
```js
{
    "server_id": // ID of target server
    "channel_id": // ID of target channel
    "timezones": [ /* Target time zone codes, ex. UTC, CET */ ],
    "schedule": [
        {
            "title": // Announcement title
            "start": // Announcement start day and time in UTC, ex. 1970-01-01 01:00
            "end": // Announcement end day and time in UTC, ex. 1970-01-01 01:00
        }
    ]
}
```