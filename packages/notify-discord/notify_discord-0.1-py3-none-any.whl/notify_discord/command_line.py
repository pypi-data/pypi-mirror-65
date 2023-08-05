#!/usr/bin/env python
#
# send a message to a discord channel using webhooks
#
# author:   Jean-Luc.Szpyrka@inria.fr
# creation: 10th day after the First Great French Quarantine
#

import sys    as sys
import getopt as getopt

from . import notify

def main():
    message = ''
    webhook = ''
    usage="notify-discord -m <message> -w <webhook>"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hm:w:",["message=","webhook="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-w", "--webhook"):
            webhook = arg

    if ( not message or not webhook) :
        print(usage)
        sys.exit(-1)

    notify(message, webhook)
