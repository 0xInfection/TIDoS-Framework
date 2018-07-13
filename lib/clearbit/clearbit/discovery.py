from clearbit.resource import Resource

class Discovery(Resource):
    endpoint = 'https://discovery.clearbit.com/v1'

    @classmethod
    def search(cls, **options):
        response = cls.post('/companies/search', **options)
        return(response.json())
