import os
import json
import xmltodict
import requests

CREDIENTIALS = [
    'KEY',
    'PASSWORD',
    'ACCOUNT_NUMBER',
    'METER_NUMBER'
]

SANDBOX_CREDIENTIALS = [
    'SANDBOX_KEY',
    'SANDBOX_PASSWORD',
    'SANDBOX_ACCOUNT_NUMBER',
    'SANDBOX_METER_NUMBER'
]


def track(event, *_):
    data = json.loads(event['body'])
    errors = process_keys(data['sandbox'])
    request = Request(data['track_no'], data['sandbox'], data['lang'])
    response = request.send()
    content = xmltodict.parse(response.content)
    body = content['SOAP-ENV:Envelope']['SOAP-ENV:Body']

    processed_body = {
        'success': response.status_code == 200,
        'sandbox': data['sandbox'],
        'data': body
    }
    if not errors:
        processed_return = json.dumps(processed_body)
    else:
        processed_return = errors

    return {
        'isBase64Encoded': False,
        'statusCode': 200 if not errors else 400,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': processed_return
    }


def process_keys(sandbox):
    errors = []
    if not sandbox:
        map(lambda env: errors.insert('%s KEY IS MISSING' %
                                      env) if os.environ[env] else False, CREDIENTIALS)
    else:
        map(lambda env: errors.insert('%s KEY IS MISSING' % env)
            if os.environ[env] else False, SANDBOX_CREDIENTIALS)
    return errors


class Request:
    def __init__(self, track_no, sandbox, lang):
        self.track_no = track_no
        self.lang = lang
        self.sandbox = sandbox
        self.request_url = 'https://wsbeta.fedex.com:443/web-services/track' if self.sandbox else 'https://ws.fedex.com:443/web-services/track'  # pylint: disable=line-too-long

    def send(self):
        response = requests.post(
            self.request_url, data=self.get_request_body())
        if response.status_code != 200:
            raise 'ServiceError'
        return response

    def get_language_code(self):
        return {
            'language_code': 'FR' if self.lang.lower() == 'fr' else 'EN',
            'locale_code': 'CA' if self.lang.lower() == 'fr' else 'US'
        }

    def get_request_body(self):
        key = os.environ['KEY'] if not self.sandbox else os.environ['SANDBOX_KEY']
        password = os.environ['PASSWORD'] if not self.sandbox else os.environ['SANDBOX_PASSWORD']
        account_number = os.environ['ACCOUNT_NUMBER'] if not self.sandbox else os.environ[
            'SANDBOX_ACCOUNT_NUMBER']
        meter_number = os.environ['METER_NUMBER'] if not self.sandbox else os.environ[
            'SANDBOX_METER_NUMBER']
        language = self.get_language_code()
        language_code = language['language_code']
        locale_code = language['locale_code']
        return f'''
      <soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
                xmlns:v16='http://fedex.com/ws/track/v16'>
                    <soapenv:Header/>
                    <soapenv:Body>
                    <v16:TrackRequest>
                    <v16:WebAuthenticationDetail>
                    <v16:UserCredential>
                    <v16:Key>{key}</v16:Key>
                        <v16:Password>{password}</v16:Password>
                        </v16:UserCredential>
                        </v16:WebAuthenticationDetail>
                        <v16:ClientDetail>
                        <v16:AccountNumber>{account_number}</v16:AccountNumber>
                        <v16:MeterNumber>{meter_number}</v16:MeterNumber>
                        </v16:ClientDetail>
                        <v16:TransactionDetail>
                        <v16:CustomerTransactionId>Track By Number_v16</v16:CustomerTransactionId>
                        <v16:Localization>
                        <v16:LanguageCode>{language_code}</v16:LanguageCode>
                        <v16:LocaleCode>{locale_code}</v16:LocaleCode>
                        </v16:Localization>
                        </v16:TransactionDetail>
                        <v16:Version>
                        <v16:ServiceId>trck</v16:ServiceId>
                        <v16:Major>16</v16:Major>
                        <v16:Intermediate>0</v16:Intermediate>
                        <v16:Minor>0</v16:Minor>
                        </v16:Version>
                        <v16:SelectionDetails>
                        <v16:CarrierCode>FDXE</v16:CarrierCode>
                        <v16:PackageIdentifier>
                        <v16:Type>TRACKING_NUMBER_OR_DOORTAG</v16:Type>
                        <v16:Value>{self.track_no}</v16:Value>
                        </v16:PackageIdentifier>
                        <v16:PagingDetail>
                        <v16:NumberOfResultsPerPage>1</v16:NumberOfResultsPerPage>
                        </v16:PagingDetail>
                        </v16:SelectionDetails>
                        <v16:ProcessingOptions>INCLUDE_DETAILED_SCANS</v16:ProcessingOptions>
                        </v16:TrackRequest>
                        </soapenv:Body>
                    </soapenv:Envelope>
    '''
