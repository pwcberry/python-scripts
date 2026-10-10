import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timedelta, datetime, timezone
import google_auth_oauthlib

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]

def main():
    with open("credentials.json", "r") as file:
        secrets = json.load(file)

    creds = google_auth_oauthlib.get_user_credentials(
        SCOPES, secrets["installed"]["client_id"], secrets["installed"]["client_secret"]
    )

    performances = []

    with open("malthouse-2027.json", "r") as file:
        malthouse = json.load(file)
        for show in malthouse:
            performances.append(show)

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
    main()
