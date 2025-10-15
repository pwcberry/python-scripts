import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]

def main():
    creds = credentials.retrieve_gcp_credentials(SCOPES)

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
