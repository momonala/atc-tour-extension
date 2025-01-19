import json
import os

import country_converter as coco
import pycountry
from googleapiclient.discovery import build  # noqa

from datamodels import TourInfo, print_color
from values import CALENDAR_ID, credentials

# Authenticate and build services
calendar_service = build("calendar", "v3", credentials=credentials)
gcal_client = calendar_service.events()
cc = coco.CountryConverter()

CACHE_FILE = "event_cache.json"


def load_calenar_event_cache() -> dict[str, str]:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_calendar_event_cache(cache: dict[str, str]):
    with open(CACHE_FILE, "w") as f:
        f.write(json.dumps(cache, indent=4, sort_keys=True))


def extract_country(country_name: str) -> pycountry.db.Country:
    """Extract extract_country from HTTP response"""
    iso3 = cc.convert(country_name, to="ISO3")
    return pycountry.countries.get(alpha_3=iso3)


def create_or_update_gcal_event(tour_info: TourInfo) -> str:
    cache = load_calenar_event_cache()
    tour_hash = str(hash(tour_info))

    pycountry_obj = extract_country(tour_info.country)
    event_description = f"{pycountry_obj.flag} ATC {tour_info.country} with {tour_info.leader}! | €{tour_info.discount} | {tour_info.days} days"  # noqa
    event = {
        "summary": event_description,
        "start": {
            "dateTime": tour_info.start_date.isoformat(),
            "timeZone": "Europe/Berlin",
        },
        "end": {
            "dateTime": tour_info.end_date.isoformat(),
            "timeZone": "Europe/Berlin",
        },
        "description": event_description,
    }

    existing_event_id = cache.get(tour_hash)
    if not existing_event_id:
        event = gcal_client.insert(calendarId=CALENDAR_ID, body=event).execute()
        print_color(
            f"{'📅 Created new event!:':<20} {event_description:<60} ID {event['']}",
            "green",
        )
        cache[tour_hash] = event["id"]
        save_calendar_event_cache(cache)
    else:
        if not tour_info.is_available:
            # Delete the existing event if tour no longer available
            gcal_client.delete(
                calendarId=CALENDAR_ID, eventId=existing_event_id
            ).execute()
            print_color(
                f"{'📅 Deleted event:':<20} {event_description:<60} ID {existing_event_id}. No longer available.",
                "red",
            )
        else:
            event = gcal_client.update(
                calendarId=CALENDAR_ID, eventId=existing_event_id, body=event
            ).execute()
            print_color(
                f"{'📅 Updated event:':<20} {event_description:<60} ID {event['id']}",
                "yellow",
            )
    return event["id"]
