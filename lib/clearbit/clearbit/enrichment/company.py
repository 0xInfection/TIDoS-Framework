from clearbit.resource import Resource
from clearbit.error import ParamsInvalidError

class Company(Resource):
    endpoint = 'https://company.clearbit.com/v2/companies'

    @classmethod
    def find(cls, **options):
        if 'domain' in options:
            url = '/find'
        elif 'id' in options:
            url = '/' + options.pop('id')
        else:
            raise ParamsInvalidError('Invalid values')

        return cls.get(url, **options)

    def flag(self, **attrs):
        return self.post('/%s/flag' % self['id'], **attrs)
