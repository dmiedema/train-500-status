#!/usr/bin/env python

import pytest
import mock
import status
import fixtures
import os
import twitter

os.environ['TWITTER_CONSUMER_KEY']        = 'TEST_TWITTER_CONSUMER_KEY'
os.environ['TWITTER_CONSUMER_SECRET']     = 'TEST_TWITTER_CONSUMER_SECRET'
os.environ['TWITTER_ACCESS_TOKEN_KEY']    = 'TEST_TWITTER_ACCESS_TOKEN_KEY'
os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = 'TEST_TWITTER_ACCESS_TOKEN_SECRET'

def test_convert_to_date():
    date = status.convert_to_datetime(fixtures.time_string)
    assert date is not None

def test_extract_json_segment():
    assert status.extract_segment_json(fixtures.valid_json) is not None
    assert status.extract_segment_json(fixtures.invalid_json) is not None
    assert status.extract_segment_json(fixtures.canceled_json) is not None

def test_build_post_from_json():
    valid_json    = status.extract_segment_json(fixtures.valid_json)
    invalid_json  = status.extract_segment_json(fixtures.invalid_json)
    canceled_json = status.extract_segment_json(fixtures.canceled_json)

    assert status.build_post_from_json(valid_json) is not None
    assert status.build_post_from_json(invalid_json) is not None
    assert status.build_post_from_json(canceled_json) is not None


def test_post_to_twtter():
    api = status.post_to_twitter('Test Post', verbose=True, dry_run=True)
    assert api is not None

def test_post_on_not_dryrun(mocker):
    mocker.patch('twitter.Api.PostUpdate')
    update = 'Test Post'
    api = status.post_to_twitter(update)
    assert api is not None
    twitter.Api.PostUpdate.assert_called_once_with(update)

def test_extract_segment_invalid_json():
    assert status.extract_segment_json({}) is None

def test_parse_args_missing_required():
    try:
        status.parse_arguments([])
    except:
        assert True

def test_parse_args_full_set():
    args = status.parse_arguments(['--station', 'xyz', '--train', '500', '--date', '2016-01-01', '--verbose', '--dry-run'])
    assert args.date    == '2016-01-01'
    assert args.verbose is True
    assert args.train   == 500
    assert args.station == 'xyz'
    assert args.dry_run is True


def test_build_request_no_args_is_none():
    assert status.build_request() is None

def test_build_request():
    date = '2016-01-01'
    station = 'XYZ'
    train = 1234
    request = status.build_request(station=station,
                                   train=train,
                                   date=date)
    params  = request['params']
    headers = request['headers']
    url     = request['url']

    assert params   is not None
    assert headers  is not None
    assert url      is not None

    assert params['dateTime']    == date
    assert params['trainNumber'] == str(train)
    assert params['origin']      == station.upper()

    assert headers['User-Agent'] is not None
    assert headers['Content-Type'] == 'application/json'


