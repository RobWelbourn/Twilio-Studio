# Twilio-Studio
Tools for analyzing call flows through IVRs built with Twilio Studio.

## Installation
Clone or unzip this repository into your project directory.  If you're using a [Virtual Environment](https://virtualenv.pypa.io/en/stable/userguide/), do the following in your project directory:
```
python3 -m venv ENV
source ENV/bin/activate
```
Next, install the required Python libraries:
```
pip install -r requirements.txt
```

## steps.py
Creates a CSV file of steps within engagements in a Twilio Studio flow, for the given time period, for the purposes of analyzing paths through an IVR. 

```
usage: steps.py [-h] [--after AFTER] [--before BEFORE] [--tz TZ]
                [--output OUTPUT] [--account ACCOUNT] [--password PASSWORD]
                [--subaccount SUBACCOUNT]
                FLOW

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
```

The resulting output will look something like this:
```
Date/Time,Engagement SID,Contact Address,Step,Event,Next Step
2018-04-08 00:00:10+00:00,FN29b5cf7b979ce3868c1fcde88946b79f,+16175551212,connect_call_to_target,callCompleted,Ended
2018-04-07 23:59:59+00:00,FN29b5cf7b979ce3868c1fcde88946b79f,+16175551212,call_agent,answered,connect_call_to_target
2018-04-07 23:59:52+00:00,FN29b5cf7b979ce3868c1fcde88946b79f,+16175551212,Trigger,incomingRequest,call_agent
```
