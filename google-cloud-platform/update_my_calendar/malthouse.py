import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timedelta, datetime, timezone
import google_auth_oauthlib
import cli

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]

def main(data_source):
    with open("credentials.json", "r") as file:
        secrets = json.load(file)

    creds = google_auth_oauthlib.get_user_credentials(
        SCOPES, secrets["installed"]["client_id"], secrets["installed"]["client_secret"]
    )

    with open(data_source, "r") as file:
        performances = json.load(file)

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.now(tz=timezone.utc).isoformat()

        for show in performances:
            isAmandaOnly = True if 'isAmandaOnly' in show else False
            title = f"{show['title']} (AMANDA)" if isAmandaOnly else f"{show['title']}"
    
            o = {
                "colorId": "5",
                "created": now,
                "description": "",
                "end": {
                    "dateTime": show['end'],
                },
                "location": "Malthouse Theatre, The Malthouse, 113 Sturt St, Southbank VIC 3006, Australia",
                "start": {
                    "dateTime": show['start']
                },
                "status": "confirmed",
                "summary": title,
            }

            print(f"Adding: '{show['title']}'...")

            insert_result = (
                service.events()
                .insert(calendarId="primary", body=o)
                .execute()
            )

            print(f"Added: '{insert_result['summary']}'\n")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main(cli.parse_data_source("Add Malthouse Theatre shows to Google Calendar.", ".json"))
