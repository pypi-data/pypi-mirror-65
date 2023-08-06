import phonenumbers


class PhoneNumber(object):

    def set_number_format(self, number, country):
        formatnumber = number.replace('/\D/', '')
        formatnumber = formatnumber.replace('/[^0-9]+/', '')
        formatnumber = formatnumber.replace(' ', '')

        # Si no tiene 10 caracteres como minimo lo mando como invalido y a la mierda
        if len(formatnumber) > 9:
            country = country.upper()
            if country == 'AR':
                # En el caso q sea de bsas y no traiga la caracteristica lo
                # agrego de una 1540842004
                if len(formatnumber) == 10 and str(formatnumber[0: 2]) == '15':
                    formatnumber = "11" + formatnumber

                formatnumber = formatnumber.replace('/^549/', '54')
                formatnumber = formatnumber.replace('/^054/', '54')
            elif country == 'MX':
                formatnumber = formatnumber.replace('/^52/', '52')
                formatnumber = formatnumber.replace('/^052/', '52')
            elif country == 'CL':
                formatnumber = formatnumber.replace('/^56/', '56')
                formatnumber = formatnumber.replace('/^056/', '56')
            elif country == 'PY':
                formatnumber = formatnumber.replace('/^59/', '59')
                formatnumber = formatnumber.replace('/^059/', '59')

            try:
                parsed_number = phonenumbers.parse(formatnumber, country)
            except phonenumbers.phonenumberutil.NumberParseException:
                return 'invalid'
            else:
                if phonenumbers.is_possible_number(parsed_number):
                    E164_number = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164)
                else:
                    return 'invalid'

                if country == 'AR':
                    formattedNumber = E164_number.replace('+549', '+54')

                return formattedNumber
        else:
            return 'invalid'
