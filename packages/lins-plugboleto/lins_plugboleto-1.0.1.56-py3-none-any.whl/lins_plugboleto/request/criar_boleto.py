
from .base import Base
import json


class CriarBoleto(Base):

    def __init__(self, authorize, environment):

        super(CriarBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, criar_boleto):
        response = None
        uri = '%sboletos/lote' % self.environment.api

        try:
            response = self.send_request("POST", uri, criar_boleto)
            body = response[1]
            body = json.loads(json.dumps(body))
            sucesso = response[0]['_dados']['_sucesso']
            if sucesso:
                criar_boleto.update_return(response[0], body)
        except json.JSONDecodeError as error:
            raise Exception('Problema no retorno da plugboleto: {} - Json inválido: {}'.format(error, response))
        except Exception as error:
            raise Exception('Problema no retorno da plugboleto: {} - Response: {}'.format(error, response))

        return response
