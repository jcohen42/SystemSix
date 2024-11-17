#!/usr/bin/python
"""Functions for getting bus arrival times."""

import logging
from datetime import datetime
from settings import ONEBUSAWAY_API_KEY, ONEBUSAWAY_STOP_IDS
from onebusaway import OnebusawaySDK


logger = logging.getLogger('app')


# Global variables.
client = None

def initialize_oba_client():
    global client

    try:
        client = OnebusawaySDK(api_key=ONEBUSAWAY_API_KEY)
        return True
    except Exception as e:
        logger.critical(e)
        client = None
        return False

def get_bus_schedule(max_number: int):
    """Returns a sorted list of bus arrival times for each stop in a list"""
    global client

    try:
        arrivals = []
        for stop in ONEBUSAWAY_STOP_IDS:
            response = client.arrival_and_departure.list(stop, minutes_before=0, minutes_after=20)
            
            arrivals.extend(response.data.entry.arrivals_and_departures)

        # Sort the array based on arrival time, using predicted times when available
        sorted_arrivals = sorted(arrivals, key=lambda x: x.predicted_arrival_time if x.predicted else x.scheduled_arrival_time)

        logger.info("oba_module.get_events(); got {} entries (capped to {}).".format(
            len(arrivals), max_number))
        
        return sorted_arrivals[:max_number]
    
    except Exception as e:
        logger.critical(e)
        return None

def print_arrival(arr_dep):
    """Helper method to print an arrival"""
    print(f"Route: {arr_dep.route_short_name}")
    print(f"Trip Headsign: {arr_dep.trip_headsign}")
    print(f"Is Predicted: {arr_dep.predicted}")
    print(f"Predicted Arrival Time: {arr_dep.predicted_arrival_time}")
    print(f"Scheduled Arrival Time: {arr_dep.scheduled_arrival_time}")

    now = datetime.now()
    if arr_dep.predicted:
        predicted_time = datetime.fromtimestamp(arr_dep.predicted_arrival_time / 1000)
        min_away = int((predicted_time - now).total_seconds() / 60)
        print(f"Predicted time: {min_away}min")
    else:
        scheduled_time = datetime.fromtimestamp(arr_dep.scheduled_arrival_time / 1000)
        min_away = int((scheduled_time - now).total_seconds() / 60)
        print(f"Scheduled time: {min_away}min")
    print("")
    
def main():
    """Run program if called directly."""
    initialize_oba_client()

    current_time = client.current_time.retrieve()
    print("Got time from OBA: " + str(current_time.data.entry.readable_time))

    arrival_times = get_bus_schedule()
    for arrival in arrival_times:
        print_arrival(arrival)

if __name__ == "__main__":
    main()