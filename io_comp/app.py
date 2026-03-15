import logging
import argparse
from datetime import timedelta
from io_comp.repository import get_default_repository
from io_comp.service import AvailabilityFinder

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Find mutual availability across calendars.')
    parser.add_argument('--people', nargs='+', default=['Alice','Jack'],
                        help='List of people to find availability for (default: Alice Jack)')
    parser.add_argument('--duration', type=int, default=60,
                        help='Meeting duration in minutes (default: 60)')
    args = parser.parse_args()

    repo = get_default_repository()
    finder = AvailabilityFinder(repo)

    available_slots = finder.find_available_slots(args.people, timedelta(minutes=args.duration))

    for window in available_slots:
        if window.earliest == window.latest:
            logger.info(f"Starting Time of available slots: {window.earliest.strftime('%H:%M')}")
        else:
            logger.info(f"Starting Time of available slots: {window.earliest.strftime('%H:%M')} - {window.latest.strftime('%H:%M')}")


if __name__ == "__main__":
    main()