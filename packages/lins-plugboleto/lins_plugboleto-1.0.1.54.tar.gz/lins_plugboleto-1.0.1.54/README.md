O que há neste pacote?
============
Pacote python da plug boleto, criação de boletos, consulta e endereço de impressão de boleto

Como utilizar esse pacote?
==========================
pip install lins-plugboleto

pip install requests

Como importar as funcionalidades do pacote?
===========================================
from lins_plugboleto import *

Exemplos de Utilização
======================
  * Configurar authorize e enviroment

        config = configurar_ambiente_boleto()

        def configurar_ambiente_boleto():

            env_sandbox = True
            env_boleto = Environment(sandbox=env_sandbox)
            authorize = Authorize('01001001000113', 'f22b97c0c9a3d41ac0a3875aba69e5aa', '01001001000113')
            return PlugBoleto(authorize, env_boleto)

  * Gerar numero de documento

        nosso_numero = config.gerar_nossonumero()

  * Criar Boleto na Plug

        * Objetos e valores obrigatórios a serem enviados para o dicionario
                  #titulo
                    titulo['TituloValor']
                    titulo['TituloDataEmissao']
                    titulo['PrazoVencimento']
                    titulo['TituloLocalPagamento']

                  #cedente
                    cedente['CedenteContaCodigoBanco']
                    cedente['CedenteContaNumero']
                    cedente['CedenteContaNumeroDV']
                    cedente['CedenteConvenioNumero']

                  #mensagem
                    mensagem['TituloMensagem01']
                    mensagem['TituloMensagem02']
                    mensagem['TituloMensagem03']

                  #prazo baixa
                    prazo_baixa

        * Obs :
           Os outros campos são preenchidos através da API-CREDITO conforme cada boleto



     boleto = Boleto(titulo,cedente, mensagem, prazo_baixa)

     retorno = config.criar_boleto(boleto)

  * Consultar boleto

        get = config.consulta_boleto(idtransacao)

  * Impressão boleto

        link = config.link_boleto(idtransacao)

  * Obs : todos os campos enviados devem estar como string

