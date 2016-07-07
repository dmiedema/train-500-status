#!/usr/bin/env python

import pytest
import status
import fixtures
import os

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

