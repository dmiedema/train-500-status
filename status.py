#!/usr/bin/env python

import argparse
import requests
import json
import os
import twitter
from datetime import datetime

def convert_to_datetime(s):
    if s:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    return None

def post_to_twitter(post, verbose=False, dry_run=False):
    if verbose:
        print post
        print "Post Length: {}".format(len(post))

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    if not dry_run:
        status = api.PostUpdate(post)
        if verbose:
            print status

    if verbose:
        print api

    return api

def extract_segment_json(json, verbose=False):
    if verbose:
        print json
    try:
        return json['journeys'][0]['segments'][0]
    except:
        return None

def build_post_from_json(json, verbose=False):
    disruption_message = None
    if json['destinationStatusComment'] is not None:
        disruption_message = json['destinationStatusComment']

    if verbose:
        print '--- Begin info[journeys][0][segments][0] ---'
        print json
        print '--- End info[journeys][0][segments][0] ---'

    station_short_code  = json['originStationCode']
    scheduled_arrival   = convert_to_datetime(json['destinationScheduledArrivalDateTime'])
    actual_arrival      = disruption_message or convert_to_datetime(json['destinationPostedArrivalDateTime'])
    scheduled_departure = convert_to_datetime(json['originScheduledDepartureDateTime'])
    actual_departure    = disruption_message or convert_to_datetime(json['originPostedDepartureDateTime'])
    route_name          = json['routeName']
    train_number        = json['trainNumber']
    stop_duration       = json['durationMinutes']

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
    elif disruption_message:
        arrival_offset_string = disruption_message.upper()
    else:
        arrival_offset_string = 'unknown'.upper()

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
    elif disruption_message:
        departure_offset_string = disruption_message.upper()
    else:
        departure_offset_string = 'unknown'.upper()

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
    return update

def main():
    parser = argparse.ArgumentParser(description="Train Status Fetcher")
    parser.add_argument("-s", "--station", dest="station", type=str, required=True, help="Station Short Code. Ex: 'SLM'")
    parser.add_argument('-t', '--train', dest='train', type=int, required=True, help='Train Number. Ex: 500')
    parser.add_argument('-d', '--date', dest='date', type=str, required=True, help='Date. YYYY-MM-DD')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose, debugging output')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='Skip posting to twitter')

    parser.set_defaults(station=None, train=None, date=None, verbose=False, dry_run=False)

    args = parser.parse_args()

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

    info = extract_segment_json(j)
    if not info:
        print '[ERROR] - Failure to extract segment json'
        print "--- BEGIN FAILING JSON ---"
        print j
        print "--- END FAILING JSON ---"
        return

    update = build_post_from_json(info, verbose=args.verbose)
    if not update:
        print '[ERROR] - Failed to build post'
        print "--- BEGIN FAILING JSON ---"
        print info
        print "--- END FAILING JSON ---"
        return

    post_to_twitter(update, verbose=args.verbose, dry_run=args.dry_run)

if __name__ == '__main__':
    main()

