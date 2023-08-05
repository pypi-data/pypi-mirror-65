
from .base import Base

class BuscaBoleto(Base):

    def __init__(self, authorize, environment):

        super(BuscaBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, id_integracao):

        uri = '%sboletos?IdIntegracao=%s' % (self.environment.api, id_integracao)

        return self.send_request("GET", uri)
