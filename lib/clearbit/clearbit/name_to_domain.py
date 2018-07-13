from clearbit.resource import Resource
from clearbit.error import (ParamsInvalidError)

class NameToDomain(Resource):
    endpoint = 'https://company.clearbit.com/v1/domains'

    @classmethod
    def find(cls, **options):
        return cls.get('/find', **options)
