from clearbit.resource import Resource

class Watchlist(Resource):
    endpoint = 'https://watchlist.clearbit.com/v1'

    @classmethod
    def search(cls, **options):
        if 'path' in options:
            path = options.pop('path')
        else:
            path = '/search/all'

        response = cls.post(path, **options)

        return(cls(item) for item in response.json())

class Individual(Watchlist):
    @classmethod
    def search(cls, **options):
        return super(Individual, cls).search(path='/search/individuals', **options)

class Entity(Watchlist):
    @classmethod
    def search(cls, **options):
        return super(Entity, cls).search(path='/search/entities', **options)

class Candidate(Resource):
    endpoint = 'https://watchlist.clearbit.com/v1'

    @classmethod
    def all(cls):
        return cls.get('/candidates')

    @classmethod
    def create(cls, **params):
        response = cls.post('/candidates', params=params)

        return cls(response.json())

    @classmethod
    def find(cls, id):
        return cls.get('/%s' % id)

    def destroy(self):
        return self.__class__.delete('/candidates/%s' % self['id'])
