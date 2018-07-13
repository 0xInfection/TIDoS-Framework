from clearbit.resource import Resource

class Prospector(Resource):
    endpoint = 'https://prospector.clearbit.com/v1'

    @classmethod
    def search(cls, **options):
        return cls.get('/people/search', **options)

    @property
    def email(self):
      return self.getEmailResponse()['email']

    @property
    def verified(self):
      return self.getEmailResponse()['verified']

    email_response = None

    def getEmailResponse(self):
      if (self.email_response):
          return self.email_response

      self.email_response = self.get('/people/%s/email' % self['id'])
      return self.email_response
