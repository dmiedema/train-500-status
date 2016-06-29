# train-500-status
Amtrak Train 500 status

## Requirements
- [`nodejs`](https://nodejs.org)
- [`phantomjs`](https://phantomjs.org)

## Example output

```
~/Code/train-500-status master* 8s
[0] ❯ phantomjs trainStatus.js
Station: ALY
Train Number: 500
Date: 06/29/2016
Loaded page in 3966 msec
ALY
Arrived
10 minutes late
6:21 am
Wed, Jun 29 2016
Scheduled Arrival 6:11 am

~/Code/train-500-status master* 8s
[0] ❯ phantomjs trainStatus.js SLM
Station: SLM
Train Number: 500
Date: 06/29/2016
Loaded page in 3983 msec
SLM
Arrived
12 minutes late
6:53 am
Wed, Jun 29 2016
Scheduled Arrival 6:41 am
```
