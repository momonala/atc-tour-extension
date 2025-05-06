import time

import schedule
import logging
from main import am_interested, create_or_update_gcal_event, fetch_tour_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def job():
    logger.info("Fetching tours...")
    tours = fetch_tour_data()
    logger.info(f"Found {len(tours)} tours")
    for tour in tours:
        if am_interested(tour):
            create_or_update_gcal_event(tour)


if __name__ == "__main__":
    schedule.every().day.at("10:00").do(job)
    logger.info("Init scheduler!")
    while True:
        schedule.run_pending()
        time.sleep(1)
