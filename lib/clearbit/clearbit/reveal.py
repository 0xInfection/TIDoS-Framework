from clearbit.resource import Resource
from clearbit.error import (ParamsInvalidError)

class Reveal(Resource):
    endpoint = 'https://reveal.clearbit.com/v1/companies'

    @classmethod
    def find(cls, **options):
        return cls.get('/find', **options)
