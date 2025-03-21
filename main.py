from datetime import datetime, date
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from joblib import Memory

from datamodels import TourInfo, print_color
from gservices import create_or_update_gcal_event


disk_memory = Memory("cache")

discount = 0.10

excluded_countries = [
    "Syria",
    "Mauritania",
    "Iraq",
    "Socotra",
    "Venezuela",
    "Russian Caucasus",
    "Arctic Russia",
    "Venezuela",
    "Somaliland",
    "Yemen",
    "Kazakhstan",
]

countries = [
    "Eritrea",
    "Mauritania",
    "Libya",
    "Iraq",
    "Syria",
    "Turkmenistan",
    "Pakistan",
    "Kazakhstan",
    "Venezuela",
    "Russian Caucasus",
    "Arctic Russia",
    "Yemen",
    "Somaliland",
    "Socotra",
    "Eritrea + Somaliland",
    "Yemen + Socotra",
]


@disk_memory.cache()
def cached_get_tour(_cache_key: datetime = date.today()):
    url = "https://expeditions.againstthecompass.com/tours/"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def fetch_tour_data() -> list[TourInfo]:
    tour_page_text = cached_get_tour()
    soup = BeautifulSoup(tour_page_text, "html.parser")
    tour_entries = soup.find_all("div", class_="col mb-5")

    parsed_tours = []
    for entry in tour_entries:

        # Extract country from the tour name
        tour_name_elem = entry.find("h3", class_="tour-name")
        tour_name = tour_name_elem.get_text(strip=True)
        country = None
        for possible_country in countries:
            if possible_country in tour_name:
                country = possible_country
                break
        if not country:
            print(f"No country found for {tour_name=}\n{entry}")
            continue

        # Extract tour leader
        leader_container = entry.find("i", class_="fa-solid fa-user me-3")
        leader = leader_container.find_next_sibling(string=True).strip()

        # Extract dates
        date_container = entry.find("i", class_="fa-regular fa-calendar me-3")
        date_text = date_container.find_next_sibling(string=True).strip()
        start_date, end_date = convert_to_datetimes(date_text)

        # Extract price
        price_container = entry.find("i", class_="fa-solid fa-euro-sign me-3")
        if not price_container:
            price_container = entry.find("i", class_="fa-solid fa-dollar-sign me-3")
        price_text = price_container.find_next_sibling(string=True).strip()
        price = int(price_text)

        # Extract number of days
        days_container = entry.find("i", class_="fa-solid fa-sun me-3")
        days = days_container.find_next_sibling(string=True).strip()
        days = int(days.split(" ")[0])

        # Extract availability
        is_sold_out = (
            entry.find("div", class_="ribbon")
            and "sold out"
            in entry.find("div", class_="ribbon").get_text(strip=True).lower()
        )
        is_waiting_list = (
            entry.find("button", class_="btn-sold-out")
            and "waiting list"
            in entry.find("button", class_="btn-sold-out").get_text(strip=True).lower()
        )
        is_available = not (is_sold_out or is_waiting_list)

        tour_info = TourInfo(
            country=country,
            leader=leader,
            days=days,
            start_date=start_date,
            end_date=end_date,
            price=price,
            discount=int(price * (1 - discount)),
            is_available=is_available,
        )
        pretty_print_tour_single_line(tour_info)
        parsed_tours.append(tour_info)

    return parsed_tours


def convert_to_datetimes(date_range):
    # Remove extra spaces and handle dash or space-dash
    date_range = date_range.replace(" - ", "-")
    dates, year = date_range.split(",")
    year = int(year.strip())

    start_date_str, end_date_str = dates.split("-")

    # Parse the start date
    month_to_num_mapping = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    start_month, start_day = start_date_str.split()
    try:
        end_month, end_day = end_date_str.split()
    except ValueError:
        end_month, end_day = start_month, end_date_str

    start_month = month_to_num_mapping[start_month]
    start_day = int(start_day)
    year = int(year)

    end_month = month_to_num_mapping[end_month]
    end_day = int(end_day)

    # Create datetime objects
    berlin_tz = ZoneInfo("Europe/Berlin")
    start_date = datetime(year, start_month, start_day, tzinfo=berlin_tz)
    end_date = datetime(year, end_month, end_day, tzinfo=berlin_tz)
    end_date = end_date.replace(hour=23, minute=59, second=0, microsecond=0)

    return start_date, end_date


def am_interested(tour_info: TourInfo):
    return all(
        [
            tour_info.is_available,
            tour_info.country not in excluded_countries,
        ]
    )


def pretty_print_tour_single_line(tour_info: TourInfo):
    start_date_str = tour_info.start_date.strftime("%d %b %Y")
    end_date_str = tour_info.end_date.strftime("%d %b %Y")

    if "Oriol" in tour_info.leader and am_interested(tour_info):
        line_color = "green"
    elif am_interested(tour_info):
        line_color = "yellow"
    else:
        line_color = "red"

    print_color(
        f"{tour_info.country:<20} {tour_info.leader:<20} {tour_info.days:<5} {start_date_str:<15} {end_date_str:<15} {tour_info.price:<8} {tour_info.discount:<10} {'Yes' if tour_info.is_available else 'No':<10}",  # noqa
        line_color,
    )


def print_title_row():
    print(
        f"{'Country':<20} {'Leader':<20} {'Days':<5} {'Start Date':<15} {'End Date':<15} {'Price':<8} {'Discount':<10} {'Available':<10}"  # noqa
    )
    print("-" * 110)


if __name__ == "__main__":
    print_title_row()
    tours = fetch_tour_data()
    print("-" * 110)
    for tour in tours:
        if am_interested(tour):
            create_or_update_gcal_event(tour)
