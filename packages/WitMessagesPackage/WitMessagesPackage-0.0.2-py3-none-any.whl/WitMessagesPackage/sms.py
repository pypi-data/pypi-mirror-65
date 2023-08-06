import os
from requests import post as request_post
from requests import get as request_get
from requests.auth import HTTPBasicAuth
import json
import urllib.parse

from WitMessagesPackage import PhoneNumber


class Infobip(PhoneNumber):
    # https://dev.infobip.com/#programmable-communications/sms/send-sms-message
    def __init__(
        self,
        user=os.environ.get('SMS_INFOBIP_USER'),
        password=os.environ.get('SMS_INFOBIP_PASSWORD')
    ):
        '''
        We can't to use an api key because some clients give us his user and passwords
        for send sms from his accounts
        '''
        self.url = os.environ.get('SMS_INFOBIP_URL')
        self.user = user
        self.password = password

    def send_sms(self, message, from_label, phone_to=None, country='AR'):
        '''
        Send a sms to a group of clients.

        Parameters
        ----------
        : param str       message: Text of the message that will be sent
        : param str       from_label: The company's name, 
                          Represents a sender ID which can be alphanumeric or numeric. 
                          Alphanumeric sender ID length should be between 3 and 11 characters 
                          (Example: CompanyName). Numeric sender ID length should be between 
                          3 and 14 characters.
        : param array     phone_to: An array of numbers to send sms, the numbers must be in 
                          international format (Example: 41793026727)

        Return
        ----------
        successful        Return an object with 'bulkId<Str>' and 'messages<Array>'
        5XX               Return a 'requestError<Dict>'
        '''
        if not phone_to:
            raise Exception('Can not send a sms with empty phone_to')

        destinations = [self.set_number_format(
            phone, country) for phone in phone_to]

        data = {
            'from': from_label,
            'destinations': [
                {'to': phone} for phone in list(filter(('invalid').__ne__, destinations))
            ],
            'text': message
        }

        message = {'messages': [data]}
        response = request_post(
            self.url, json=message,
            auth=HTTPBasicAuth(self.user, self.password))

        if response.status_code == 200:
            return ''
        else:
            return 'invalid'


class Movio(PhoneNumber):
    def __init__(self):
        self.rds_host = os.environ.get('MYSQL_RDS_HOST')

    def send_sms(self, *args, **kwargs):
        raise Exception('This method is not available')


class Kyrabo(PhoneNumber):
    # http://149.56.207.9/app/api
    def __init__(
            self,
            sender_id=os.environ.get('SMS_KYRABO_SENDER_ID'),
            api_key=os.environ.get('SMS_KYRABO_API_KEY')
    ):
        '''
        Parameters
        ----------
        : param str     sender_id: Approved Sender ID
        : param str     api_key: This is to authenticate the service, it can be WitAdvisor's key
                            or a company's key
        '''
        self.url = os.environ.get('SMS_KYRABO_URL')
        self.sender_id = sender_id
        self.api_key = api_key

    def send_sms(self, message, contacts=None, country='AR'):
        '''
        Send a sms to a group of clients.

        Parameters
        ----------
        : param str     message: Url-encoded SMS text. Must be limited to 740 characters.
        : param str     contacts: Contact numbers separated by ','(Comma) sign. 
                            Enter N digit mobile numbers e.g. '69XXXXXX,67XXXXXX,68XXXXXX',
                            Max 1000 Contacts

        Return
        ----------
        '''
        if len(message) > 740:
            raise Exception('Message is too long, max 740 characters')
        if not contacts:
            raise Exception('Can not send a sms with empty contacts')

        destinations = [self.set_number_format(
            phone, country) for phone in contacts.split(';')]

        if len(destinations) > 1000:
            raise Exception(
                'Too many contacts in same request, max 1000 phone\'s numbers')
        if len(destinations) == 0:
            raise Exception('Don\'t have a valid phone number')

        phone_contacts = ';'.join(destinations)
        url = '{base_url}?key={api_key}&type=text&contacts={phone_contacts}&senderid={sender_id}&msg={message}'.format(
            base_url=self.url,
            api_key=self.api_key,
            phone_contacts=phone_contacts,
            sender_id=self.sender_id,
            message=urllib.parse.quote(message)
        )

        response = request_get(url)
        if response.status_code == 200:
            return ''
        else:
            return 'invalid'
