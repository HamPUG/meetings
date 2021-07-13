import re
import urllib.request

def handler(event, context):
    ''' Proxy Lambda to handle any incoming request to the API '''

    bodyMsg = 'Invalid request'

    # check what /<path> we were asked for
    path = event['path']

    # if one we are expecting
    if path == '/metar':

        # retrieve a remote weather report for a station if airport code in correct format
        locationCode = event["queryStringParameters"]["icao"]
        if locationCode:
            pattern = r"^[A-Z]{4}$"
            if re.match(pattern, locationCode) :
                with urllib.request.urlopen('http://metar.vatsim.net/metar.php?id={}'.format(locationCode)) as f:
                    bodyMsg = f.read(300).decode('ascii')
            else :
                bodyMsg = 'Invalid ICAO code'

    # return a payload formatted the way API gateway expects it
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'API response: {}\n'.format(bodyMsg)
    }

    