from .company import Company
from .person import Person
from .person_company import PersonCompany

class Enrichment:
    @classmethod
    def find(cls, **options):
        if 'domain' in options:
            return Company.find(**options)
        else:
            return PersonCompany.find(**options)
