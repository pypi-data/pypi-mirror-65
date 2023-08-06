from requests import post
import os
import json

from WitMessagesPackage import Sengrid, PhoneNumber


class WhatsApp(PhoneNumber):
    # https://botmakeradmin.github.io/docs/es/#/messages-api
    def __init__(
        self,
        output_phone=os.environ.get('WHATSAPP_PHONE_NUMBER'),
        token=os.environ.get('WHATSAPP_TOKEN'),
        country='AR'
    ):
        self.output_phone = output_phone
        self.token = token
        self.country = country
        self.text_url = os.environ.get('WHATSAPP_TEXT_URL')
        self.template_url = os.environ.get('WHATSAPP_TEMPLATE_URL')

    def __insufficient_credit_email(self):
        '''
        Send an email to WitAdvisor's admin to notify
        '''
        sengrid = Sengrid()
        return sengrid.send_plane_email(
            os.environ.get('WHATSAPP_NOT_CREDIT_EMAIL').split(';')[0],
            os.environ.get('WHATSAPP_NOT_CREDIT_EMAIL').split(';'),
            'Insufficient credit to send WhatsApp\'s messages'
        )

    def send_template(self, user_phone, template_id, client_name, link):
        # r = wa.send_message('3512022065', 'Probando', 'sura_inicia_1', 'Di Costa Francisco Miguel', 'http://www.google.com.ar')
        '''
        Send a whatsapp's message to an user.

        Parameters
        ----------
        : param str                     user_phone: Client's phone
        : param str                     template_id: Template's id
        : param str                     client_name: Client's name
        : param str                     link: A link to replace on template

        Return
        ----------
        Successful -> 200 with {"id": "id_del_mensaje"} then return de id
        Error -> Some erros are
            200 with {'id': None, 'problems': {'code': code of error, 'message': message of error}}
            http code 403 - Forbidden -> We need to send an email to admin
                {
                  "error": {
                    "code": 101,
                    "message": "Insufficient credit"
                  }
                }
            Other errors -> invalid
        '''
        phone = self.set_number_format(user_phone, country=self.country)
        if phone == 'invalid':
            return 'Invalid phone\'s number'

        data = {
            'chatPlatform': 'whatsapp',
            'chatChannelNumber': self.output_phone,
            'platformContactId': user_phone,
            'ruleNameOrId': template_id,
            'params': {
                "NombreContacto": client_name,
                'Encuesta': link
            }
        }
        headers = {
            'access-token': self.token
        }

        response = post(self.template_url, json=data, headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
            if content.get('id'):
                return content.get('id')
            else:
                return 'Invalid ' + content.get('problems').get('message')
        else:
            if content.get('error').get('code') == 101:
                self.__insufficient_credit_email()
            return 'Invalid ' + content.get('error').get('message')

    def send_message(self, user_phone, message, template_id, client_name, link):
        '''
        Send a whatsapp's message to an user.

        Parameters
        ----------
        : param str                     user_phone: Client's phone
        : param str                     message: Message to send
        : param str                     template_id: Template's id, we use it if whatsapp 
                                            return code [201, 306]
        : param str                     client_name: Client's name
        : param str                     link: A link to replace on template

        Return
        ----------
        Successful -> 200 with {"id": "id_del_mensaje"} then return de id
        Error -> Some erros are
            200 with {'id': None, 'problems': {'code': code of error, 'message': message of error}}
            http code 403 - Forbidden -> We need to send an email to admin
                {
                  "error": {
                    "code": 101,
                    "message": "Insufficient credit"
                  }
                }
            Other errors -> invalid
        '''

        phone = self.set_number_format(user_phone, country=self.country)
        if phone == 'invalid':
            return 'Invalid phone\'s number'

        data = {
            'chatPlatform': 'whatsapp',
            'chatChannelNumber': self.output_phone,
            'platformContactId': phone,
            'messageText': message
        }
        headers = {
            'access-token': self.token
        }

        response = post(self.text_url, json=data, headers=headers)
        content = json.loads(response.content)
        if response.status_code == 200:
            if content.get('id'):
                return content.get('id')
            elif content.get('problems') and content.get('problems').get('code') in [201, 306]:
                return self.send_template(phone, template_id, client_name, link)
            else:
                return 'Invalid ' + content.get('problems').get('message')
        else:
            code = content.get('error').get('code')
            if code == 101:
                self.__insufficient_credit_email()
            return 'Invalid ' + content.get('error').get('message')
