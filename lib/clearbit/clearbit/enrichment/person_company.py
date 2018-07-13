from clearbit.resource import Resource
from clearbit.error import (ParamsInvalidError)

class PersonCompany(Resource):
    endpoint = 'https://person.clearbit.com/v2/combined'

    @classmethod
    def find(cls, **options):
        if 'email' in options:
            url = '/find'
        else:
            raise ParamsInvalidError('Invalid values')

        return cls.get(url, **options)
