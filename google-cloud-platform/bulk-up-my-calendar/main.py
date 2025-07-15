import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    football_matches = []
    with open("essendon-afl-2025.json", "r") as file:
        football_matches = json.load(file)

    with open("essendon-aflw-2025.json", "r") as file:
        aflw_matches = json.load(file)
        for match in aflw_matches:
            football_matches.append(match)

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        for match in football_matches:
            o = {
                "colorId": "8",
                "created": now,
                "description": f"{match['competition']} Round {match['round']}: {match['home']} vs {match['away']}",
                "end": {
                    "dateTime": match['end']
                },
                "location": match['venue'],
                "start": {
                    "dateTime": match['start']
                },
                "status": "confirmed",
                "summary": f"{match['competition']}: {match['home_abbr']} vs {match['away_abbr']}",
            }

            print(f"Adding: '{o['summary']}'...")

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
