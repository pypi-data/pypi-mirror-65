from .request.criar_boleto import CriarBoleto
from .request.busca_boleto import BuscaBoleto
from .request.numero_doc import NumeroDoc


class PlugBoleto(object):

    def __init__(self, authorize, environment):

        self.environment = environment
        self.authorize = authorize

    def criar_boleto(self, criar_boleto):

        request = CriarBoleto(self.authorize, self.environment)

        return request.execute(criar_boleto)

    def gerar_nossonumero(self):
        request = NumeroDoc(None, self.environment)

        return request.execute()

    def consulta_boleto(self, id_integracao):
        request = BuscaBoleto(self.authorize, self.environment)

        return request.execute(id_integracao)

    def link_boleto(self, id_integracao):
        uri = '%sboletos/impressao/%s' % (self.environment.api, id_integracao)

        return uri
