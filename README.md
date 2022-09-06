# QuantumBot
Discord bot for hackathons and workshops organized by Quantum AI Foundation

# Required Discord permissions
- View channel
- Send messages
- Embed links
- Attach files
- Add reactions
- Mention @everyone, @here etc.
- Read message history

# Schedule file information
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