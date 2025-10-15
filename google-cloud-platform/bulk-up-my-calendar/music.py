import datetime
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned"
]


def get_location(venue):
    if venue == "MELBOURNE RECITAL CENTRE":
        return "Melbourne Recital Centre, 31 Sturt St, Southbank VIC 3006, Australia"

    return "Hamer Hall, 100 St Kilda Rd, Southbank VIC 3004, Australia"


def get_start_time(str, is_summer_time):
    d = datetime.datetime.strptime(str, "%d %B %Y %I:%M %p")
    return f'{d.isoformat()}{"+11:00" if is_summer_time else "+10:00"}'


def get_end_time(start_time):
    end_time = datetime.datetime.fromisoformat(start_time) + datetime.timedelta(hours=2)
    return end_time.isoformat()


def main():
    creds = credentials.retrieve_gcp_credentials(SCOPES)

    mso_performances = []
    with open("mso_concerts_2026.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            is_summer_time = row[3] == "True"
            event = {
                "title": row[0],
                "venue": get_location(row[1]),
                "start": get_start_time(row[2], is_summer_time)
            }
            event["end"] = get_end_time(event["start"])
            mso_performances.append(event)

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        for event in mso_performances:
            o = {
                "colorId": "7",
                "created": now,
                "description": f"MSO Concert. Details to come.",
                "end": {
                    "dateTime": event['end']
                },
                "location": event['venue'],
                "start": {
                    "dateTime": event['start']
                },
                "status": "confirmed",
                "summary": f"MSO: {event['title']}",
                "attendees": [{
                    "email": "mandyquirk@gmail.com",
                    "display": "Amanda Quirk",
                    "responseStatus": "needsAction"
                }]
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
