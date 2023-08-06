import sendgrid
import os


class Sengrid:
    # https://github.com/sendgrid/sendgrid-python/blob/master/examples/mail/mail.py
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))

    def send_plane_email(self, from_email, to_email, message):
        '''
        Send an email to a group of clients with custom params.
        All email's objects have a name and an email fields.

        Parameters
        ----------
        : param str                     from_email: output email
        : param list                    to_email: a list of clients who going to receibe the email
        : param str                     message: the message to send

        Return
        ----------
        A sengrid's response, we can check status_code, body and headers.
        If the emails was successful then sengrid return ''
        '''
        if type(to_email) != list:
            raise Exception(
                'You need to set an array of emails to send messages')

        data = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': to_email
                        }
                    ],
                    'subject': 'Sending with SendGrid is Fun'
                }
            ],
            'from': {
                'email': from_email
            },
            'content': [
                {
                    'type': 'text/plain',
                    'value': message
                }
            ]
        }
        return self.sg.client.mail.send.post(request_body=data)

    def send_custom_email(self, **kwargs):
        '''
        Send an email to a group of clients with custom params.
        All email's objects have a name and an email fields.

        Parameters
        ----------
        : param str                     from_name: The name of our client
        : param str                     from_email: The email of our client
        : param <email's objects>       reply_to: Who is going to reply the emails
        : param str                     subject: The subject of the email
        : param str                     html: The content of the email
        : param list<email's objects>   to_email: List of end clients emails
        : param list<email's objects>   with_bcc: Who will receive a blind copy

        Return
        ----------
        A sengrid's response, we can check status_code, body and headers.
        If the emails was successful then sengrid return ''
        '''
        if not kwargs.get('to_email') or type(kwargs.get('to_email')) != list:
            raise Exception(
                'You need to set a list of emails to send messages')

        data = {
            'personalizations': [
                {
                    'to': kwargs.get('to_email', []),
                    'subject': kwargs.get('subject', '')
                }
            ],
            'from': {
                'email': kwargs.get('from_email', ''),
                'name': kwargs.get('from_name', '')
            },
            'reply_to': kwargs.get('reply_to', {}),
            'content': [
                {
                    'type': 'text/html',
                    'value': kwargs.get('html', '')
                }
            ]
        }
        if kwargs.get('with_bcc'):
            data['personalizations'][0]['bcc'] = kwargs.get('with_bcc', [])

        return self.sg.client.mail.send.post(request_body=data)
