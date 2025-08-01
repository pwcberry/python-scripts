from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def fetch_colors():
    creds = credentials.retrieve_gcp_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        colors_result = service.colors().get().execute()
        colors = colors_result.get("event", [])

        if not colors:
            print("No colors found.")
        else:
            print(colors)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    fetch_colors()
