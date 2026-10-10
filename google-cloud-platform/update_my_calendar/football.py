import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timedelta, datetime, timezone
import google_auth_oauthlib

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]

GROUNDS = {
    "MCG": "Melbourne Cricket Ground, Yarra Park, Jolimont, Melbourne VIC 3002",
    "MARVEL": "Marvel Stadium, 740 Bourke St, Docklands VIC 3008",
    "GMHBA": "GMHBA Stadium, 370 Moorabool St, South Geelong VIC 3220",
    "WINDY_HILL": "Windy Hill, Cnr Napier & Brewster St, Essendon VIC 3040",
    "IKON_PARK": "Ikon Park, 400 Royal Parade, Carlton North VIC 3054",
    "FOOTSCRAY": "Whitten Oval, 417 Barkly St, Footscray VIC 3011"
}

def main():
    with open("credentials.json", "r") as file:
        secrets = json.load(file)

    creds = google_auth_oauthlib.get_user_credentials(
        SCOPES, secrets["installed"]["client_id"], secrets["installed"]["client_secret"]
    )

    football_matches = []
    # with open("essendon-afl-2026-2.json", "r") as file:
    #     football_matches = json.load(file)

    with open("essendon-aflw-2026.json", "r") as file:
        aflw_matches = json.load(file)
        for match in aflw_matches:
            football_matches.append(match)

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.now(tz=timezone.utc).isoformat()

        for match in football_matches:
            end_time = datetime.fromisoformat(match["start"]) + timedelta(hours=3)

            o = {
                "colorId": "8",
                "created": now,
                "description": f"{match['competition']} Round {match['round']}: {match['home']} vs {match['away']}",
                "end": {
                    "dateTime": end_time.isoformat(),
                },
                "location": GROUNDS[match['venue']],
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
