import re
import urllib.request

def handler(event, context):
    ''' Direct Lambda invoke with event props '''

    bodyMsg = 'Invalid request'

    # retrieve a remote weather report for a station if airport code in correct format
    locationCode = event["icao"]
    if locationCode:
        pattern = r"^[A-Z]{4}$"
        if re.match(pattern, locationCode) :
            with urllib.request.urlopen('http://metar.vatsim.net/metar.php?id={}'.format(locationCode)) as f:
                bodyMsg = f.read(300).decode('ascii')
        else :
            bodyMsg = 'Invalid ICAO code'

    # return a Dictionary that can be JSON serialized by Lambda
    return {
        'result': 'METAR for: {} is {}\n'.format(locationCode, bodyMsg)
    }

    