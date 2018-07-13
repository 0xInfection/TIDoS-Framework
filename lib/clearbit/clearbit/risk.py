from clearbit.resource import Resource

class Risk(Resource):
    endpoint = 'https://risk.clearbit.com/v1'

    @classmethod
    def calculate(cls, **options):
        response = cls.post('/calculate', **options)
        return(response)

    @classmethod
    def flag(cls, **options):
        response = cls.post('/flag', **options)
        return(response)
