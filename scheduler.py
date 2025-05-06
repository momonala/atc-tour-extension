import time

import schedule

from main import am_interested, create_or_update_gcal_event, fetch_tour_data


def job():
    tours = fetch_tour_data()
    for tour in tours:
        if am_interested(tour):
            create_or_update_gcal_event(tour)


schedule.every().day.at("10:00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
