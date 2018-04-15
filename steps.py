#!/usr/bin/env python3

"""
usage: steps.py [-h] [--after AFTER] [--before BEFORE] [--tz TZ]
                [--output OUTPUT] [--account ACCOUNT] [--password PASSWORD]
                [--subaccount SUBACCOUNT]
                FLOW

Creates a CSV file of steps within engagements in a Twilio Studio flow, for
the given time period, for the purposes of analyzing paths through an IVR. 

positional arguments:
  FLOW                  Flow SID

optional arguments:
  -h, --help            show this help message and exit
  --after AFTER         yyyy-mm-dd [HH:MM[:SS]]; time defaults to 00:00:00
                        (default: None)
  --before BEFORE, -b BEFORE
                        yyyy-mm-dd [HH:MM[:SS]]; time defaults to 00:00:00
                        (default: None)
  --tz TZ, -t TZ        Time zone name (default: UTC)
  --output OUTPUT, -o OUTPUT
                        Output file; defaults to terminal (default: None)
  --account ACCOUNT, -a ACCOUNT
                        Account SID; if not given, value of environment
                        variable TWILIO_ACCOUNT_SID (default: None)
  --password PASSWORD, -p PASSWORD
                        Auth token; if not given, value of environment
                        variable TWILIO_AUTH_TOKEN (default: None)
  --subaccount SUBACCOUNT, -s SUBACCOUNT
                        If present, subaccount to use (default: None)
"""


import os
import sys
from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
import begin
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


def get_datetime(dt_string, tz):
    """Converts a date/time string into a datetime object with the given time zone."""
    try:
        dt = datetime.strptime(dt_string, '%Y-%m-%d')
    except ValueError:
        try:
            dt = datetime.strptime(dt_string, '%Y-%m-%d %H:%M')
        except ValueError:
            dt = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
    
    return tz.localize(dt)


@begin.start
def main(
        flow:       "Flow SID",
        after:      "yyyy-mm-dd [HH:MM[:SS]]; time defaults to 00:00:00" = None,
        before:     "yyyy-mm-dd [HH:MM[:SS]]; time defaults to 00:00:00" = None,
        tz:         "Time zone name" = "UTC",
        output:     "Output file; defaults to terminal" = None,
        account:    "Account SID; if not given, value of environment variable TWILIO_ACCOUNT_SID" = None,
        password:   "Auth token; if not given, value of environment variable TWILIO_AUTH_TOKEN" = None,
        subaccount: "If present, subaccount to use" = None
    ):
    """
    Creates a CSV file of steps within engagements in a Twilio Studio flow, for the given time period,
    for the purposes of analyzing paths through an IVR. 
    """
    if not flow:
        sys.exit("Error: no Flow SID")

    try:
        account = account or os.environ['TWILIO_ACCOUNT_SID']
        password = password or os.environ['TWILIO_AUTH_TOKEN']
    except KeyError:
        sys.exit("Error: missing environment variable TWILIO_ACCOUNT_SID and/or TWILIO_AUTH_TOKEN")

    try:
        tz = timezone(tz)
    except UnknownTimeZoneError:
        sys.exit("Invalid timezone: {}".format(tz))
    
    try:
        after = get_datetime(after, tz) if after else None
    except ValueError:
        sys.exit("Invalid date/time: {}".format(after))

    try:
        before = get_datetime(before, tz) if before else None
    except ValueError:
        sys.exit("Invalid date/time: {}".format(before))

    if after and before and after > before:
        sys.exit("Error: end date/time is before start date/time")

    client = Client(account, password, subaccount)

    # Grab the flow instance.
    try:
        flow = client.studio.flows.get(flow).fetch()
    except TwilioRestException:
        sys.exit("Error: unable to get Flow {}".format(flow))

    def in_range(engagement):
        """Does the engagement fall between after and before?"""
        if after and engagement.date_created < after:
            return False
        if before and engagement.date_created >= before:
            return False
        return True
        
    engagements = filter(in_range, flow.engagements.list())

    output = open(output, 'w') if output else sys.stdout
    print("Date/Time,Engagement SID,Contact Address,Step,Event,Next Step", file=output)

    for engagement in engagements:
        steps = engagement.steps.list()
        for step in steps:
            print("{},{},{},{},{},{}".format(
                step.date_created,
                engagement.sid,
                engagement.contact_channel_address,
                step.transitioned_from,
                step.name,
                step.transitioned_to
            ), file=output)

    output.close()
