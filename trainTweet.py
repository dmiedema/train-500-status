#!/usr/bin/env python

import subprocess
import argparse

parser = argparse.ArgumentParser(description="Tweet some Train Statuses!")
parser.add_argument("-s", "--station", dest="station", type=str, help="Station Short Code. Ex: 'SLM'")
parser.add_argument("-t", "--train", dest="train", type=int, help="Train Number. Ex: '500'")
parser.add_argument("-d", "--date", dest="date", type=str, help="Date. MM/DD/YYYY")

parser.set_defaults(station=None, train=None, date=None)

args = parser.parse_args()

def main():
    def run_command(cmd_array, shell=False):
        p = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = p.communicate()
        return out

    command = ['phantomjs', 'trainStatus.js']
    if args.station:
        command.append(str(args.station))
    if args.train:
        command.append(str(args.train))
    if args.date:
        command.append(str(args.date))

    print "Executing {}".format(command)
    text = run_command(command)
    tweet = text.split("-" * 3)
    result = run_command(['node', 'twitter.js', tweet[1]])
    print result

if __name__ == "__main__":
    main()

