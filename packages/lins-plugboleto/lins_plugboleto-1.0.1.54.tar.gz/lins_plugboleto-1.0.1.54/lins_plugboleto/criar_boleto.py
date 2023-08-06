from datetime import datetime, timedelta
from .objectJSON import ObjectJSON


class Boleto(ObjectJSON):

    def __init__(self, titulo, cedente, mensagem, prazo_baixa):
        self.idintegracao = None
        self.situacao = None
        self.body = None
        #sacado
        self.SacadoCPFCNPJ = None
        self.SacadoNome = None
        self.SacadoEnderecoLogradouro = None
        self.SacadoEnderecoNumero = None
        self.SacadoEnderecoBairro = None
        self.SacadoEnderecoCep = None
        self.SacadoEnderecoCidade = None
        self.SacadoEnderecoComplemento = None
        self.SacadoEnderecoPais = None
        self.SacadoEnderecoUf = None
        self.SacadoEmail = None
        self.SacadoTelefone = None
        self.SacadoCelular = None

        #cedente
        self.CedenteContaCodigoBanco = str(cedente['CedenteContaCodigoBanco'])
        self.CedenteContaNumero = str(cedente['CedenteContaNumero'])
        self.CedenteContaNumeroDV = str(cedente['CedenteContaNumeroDV'])
        self.CedenteConvenioNumero = str(cedente['CedenteConvenioNumero'])

        #titulo
        self.TituloNossoNumero = None
        self.TituloNumeroDocumento = None
        self.TituloValor = str(titulo['TituloValor'])
        dataemissao = titulo['TituloDataEmissao'].strftime('%d/%m/%Y')
        self.TituloDataEmissao = dataemissao
        datavencimento = (titulo['TituloDataEmissao'] + timedelta(days=titulo['PrazoVencimento']))
        datavencimento = datavencimento.strftime('%d/%m/%Y')
        self.TituloDataVencimento = datavencimento
        self.TituloAceite = None
        self.TituloDocEspecie = None
        self.TituloLocalPagamento = titulo['TituloLocalPagamento']

        #juros
        self.TituloCodigoJuros = None
        self.TituloDataJuros = None
        self.TituloValorJuros = None

        #multa
        self.TituloCodigoMulta = None
        self.TituloDataMulta = None
        self.TituloValorMultaTaxa = None

        #protesto
        self.TituloCodProtesto = None
        self.TituloPrazoProtesto = None

        #baixa = None
        if (prazo_baixa > 0):
            self.TituloCodBaixaDevolucao = '1'
            self.TituloPrazoBaixa = str(prazo_baixa)

        #mensagens
        self.TituloMensagem01 = str(mensagem['TituloMensagem01'])
        self.TituloMensagem02 = str(mensagem['TituloMensagem02'])
        self.TituloMensagem03 = str(mensagem['TituloMensagem03'])
        self.sacadoravalista = None

        #outros
        self.TituloEmissaoBoleto = None
        self.TituloCategoria = None
        self.TituloPostagemBoleto = None
        self.TituloCodEmissaoBloqueto = None
        self.TituloCodDistribuicaoBloqueto = None
        self.TituloOutrosAcrescimos = None
        self.TituloInformacoesAdicionais = None
        self.TituloInstrucoes = None
        self.TituloParcela = None
        self.TituloVariacaoCarteira = None
        self.TituloCodigoReferencia = None
        self.TituloTipoCobranca = None

    def update_return(self, r, body):
        dados = r.get('_dados') or {}
        sucesso = dados.get('_sucesso') or {}
        self.body = body
        self.idintegracao = sucesso[0]['idintegracao']
        self.situacao = sucesso[0]['situacao']
        self.TituloNumeroDocumento = sucesso[0]['TituloNumeroDocumento']
        self.TituloNossoNumero = sucesso[0]['TituloNossoNumero']
        self.CedenteContaCodigoBanco = sucesso[0]['CedenteContaCodigoBanco']
        self.CedenteContaNumero = sucesso[0]['CedenteContaNumero']
        self.CedenteConvenioNumero = sucesso[0]['CedenteConvenioNumero']