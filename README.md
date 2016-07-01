# train-500-status
Amtrak Train 500 status

## Requirements
- python
- pip
- Twitter tokens as ENV variables

## Usage

Run `./status.py --help` for instructions

## Example Output

```
~/Code/train-500-status master* 8s
[1] ❯ ./status.py --station=slm --train=500 --date=2016-06-30 --verbose
{"Content-Type": "application/json", "User-Agent": "AmtrakMobileRider/20160511.1521 CFNetwork/711.1.16 Darwin/14.0.0"}
{"origin": "SLM", "appType": "IOS", "dateTime": "2016-06-30", "versionNumber": "2.2.7", "type": "A", "trainNumber": "500"}
{u'originPostedDepartureDateTime': u'2016-06-30T06:52:00', u'appType': None, u'destinationStatusComment': None, u'arrivalDateTime': None, u'duration': None, u'departureStationCode': None, u'destinationScheduledArrivalDateTime': u'2016-06-30T06:41:00', u'rooms': None, u'seats': None, u'authenticationToken': None, u'additionalInfo': None, u'durationMinutes': 0, u'departureDateTimeInUTC': None, u'displayRoomNumbers': False, u'isBus': None, u'arrivalStationCode': None, u'serviceMessage': None, u'classCodeQuantity': None, u'segmentServiceStatus': u'false', u'amenities': None, u'ancillary': None, u'crossBorder': None, u'departureDateTime': None, u'classCode': None, u'companyName': None, u'destinationEstimatedArrivalDateTime': None, u'versionNumber': None, u'originEstimatedDepartureDateTime': None, u'isAlternative': None, u'serviceStatus': None, u'trainNumber': u'500', u'originStatusComment': None, u'originScheduledDepartureDateTime': u'2016-06-30T06:41:00', u'destinationStationCode': u'SLM', u'destinationPostedArrivalDateTime': u'2016-06-30T06:52:00', u'arrivalStationName': None, u'compartments': None, u'originStationCode': u'SLM', u'routeName': u'Amtrak Cascades', u'departureStationName': None, u'isRestrictive': None}
SLM
500
Arrived: 06:52 AM 11 min Late
Scheduled: 06:41 AM
Departed: 06:52 AM 11 min Late
Scheduled: 06:41 AM
Thu, Jun 30, 2016
126
    
```
