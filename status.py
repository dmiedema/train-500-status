#!/usr/bin/env python

import argparse
import requests
import json
import os
import twitter
from datetime import datetime

parser = argparse.ArgumentParser(description="Train Status Fetcher")
parser.add_argument("-s", "--station", dest="station", type=str, required=True, help="Station Short Code. Ex: 'SLM'")
parser.add_argument('-t', '--train', dest='train', type=int, required=True, help='Train Number. Ex: 500')
parser.add_argument('-d', '--date', dest='date', type=str, required=True, help='Date. YYYY-MM-DD')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose, debugging output')
parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='Skip posting to twitter')

parser.set_defaults(station=None, train=None, date=None, verbose=False, dry_run=False)

args = parser.parse_args()

def convert_to_datetime(s):
    if s:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    return None

def main():
    headers = {
        'User-Agent': 'AmtrakMobileRider/20160511.1521 CFNetwork/711.1.16 Darwin/14.0.0',
        'Content-Type': 'application/json',
    }
    params = {
        'appType': 'IOS',
        'type': 'A',
        'dateTime': args.date,
        'trainNumber': str(args.train),
        'versionNumber': '2.2.7',
        'origin': args.station.upper(),
    }
    if args.verbose:
        print json.dumps(headers)
        print json.dumps(params)

    r = requests.post('https://services.amtrak.com/Rider/TrainStatus', headers=headers, json=params)
    j = r.json()
    if args.verbose:
        print '--- Begin JSON Response ---'
        print j
        print '--- End JSON Response ---'

    info = j['journeys'][0]['segments'][0]

    disruption_message = None
    if info['destinationStatusComment'] is not None:
        disruption_message = info['destinationStatusComment']

    if args.verbose:
        print '--- Begin info[journeys][0][segments][0] ---'
        print info
        print '--- End info[journeys][0][segments][0] ---'

    station_short_code  = info['originStationCode']
    scheduled_arrival   = convert_to_datetime(info['destinationScheduledArrivalDateTime'])
    actual_arrival      = disruption_message or convert_to_datetime(info['destinationPostedArrivalDateTime'])
    scheduled_departure = convert_to_datetime(info['originScheduledDepartureDateTime'])
    actual_departure    = disruption_message or convert_to_datetime(info['originPostedDepartureDateTime'])
    route_name          = info['routeName']
    train_number        = info['trainNumber']
    stop_duration       = info['durationMinutes']

    time_format_string = '%I:%M %p'
    actual_arrival_string = ''
    scheduled_arrival_string = scheduled_arrival.strftime(time_format_string)

    arrival_offset_string = ""
    if actual_arrival and disruption_message is None:
        arrival_offset = (scheduled_arrival - actual_arrival).total_seconds() / 60
        actual_arrival_string = actual_arrival.strftime(time_format_string)
        if arrival_offset > 0:
            arrival_offset_string = "{} min Early".format(abs(int(arrival_offset)))
        else:
            arrival_offset_string = "{} min Late".format(abs(int(arrival_offset)))
    else:
        arrival_offset_string = disruption_message.upper()

    actual_departure_string = ''
    scheduled_departure_string = scheduled_departure.strftime(time_format_string)

    departure_offset_string = ""
    if actual_departure and disruption_message is None:
        departure_offset = (scheduled_departure - actual_departure).total_seconds() / 60
        actual_departure_string = actual_departure.strftime(time_format_string)
        if departure_offset > 0:
            departure_offset_string = "{} min Early".format(abs(int(departure_offset)))
        else:
            departure_offset_string = "{} min Late".format(abs(int(departure_offset)))
    else:
        departure_offset_string = disruption_message.upper()

    current_date = scheduled_arrival.strftime('%a, %b %d, %Y')
    """ Format
    Station
    Arrived Time
    Scheduled Arrival
    Departed Time
    Scheduled Departure
    Date
    """
    update = """{station}
{train}
Arrived: {actual_arrival_time} {arrival_offset}
Scheduled: {scheduled_arrival_time}
Departed: {actual_departure_time} {departure_offset}
Scheduled: {scheduled_departure_time}
{date}""".format(
    station=station_short_code,
    train=train_number,
    actual_arrival_time=actual_arrival_string, arrival_offset=arrival_offset_string,
    scheduled_arrival_time=scheduled_arrival_string,
    actual_departure_time=actual_departure_string, departure_offset=departure_offset_string,
    scheduled_departure_time=scheduled_departure_string,
    date=current_date,
)

    if args.verbose:
        print update
        print "Post Length: {}".format(len(update))

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    if not args.dry_run:
        status = api.PostUpdate(update)
        if args.verbose:
            print status

    if args.verbose:
        print api

if __name__ == '__main__':
    main()

