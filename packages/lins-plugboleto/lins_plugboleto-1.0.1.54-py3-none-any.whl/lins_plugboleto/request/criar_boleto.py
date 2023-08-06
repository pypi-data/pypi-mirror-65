
from .base import Base
import json


class CriarBoleto(Base):

    def __init__(self, authorize, environment):

        super(CriarBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, criar_boleto):

        uri = '%sboletos/lote' % self.environment.api

        response = self.send_request("POST", uri, criar_boleto)

        try:
            body = response[1]
            body = json.loads(json.dumps(body))
            sucesso = response[0]['_dados']['_sucesso']
            if sucesso:
                criar_boleto.update_return(response[0], body)
        except json.JSONDecodeError as error:
            raise Exception('Problema no retorno da plugboleto: {} - Json inválido: {}'.format(error, response))

        return response
