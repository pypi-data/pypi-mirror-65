import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
#sys.path.append('C:\\Users\\coliveira\\OneDrive\\Coding\\Python\\MFToolbox\\')
from mftoolbox import constants, funcs


def ultimo_pregao(_ativo):
    """
    Busca no site IBOVX a data do último pregão para um ativo

    :param _ativo: código do ativo
    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """

    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=1'
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    try:
        if _tabela[20].text == 'Nº Negócios':
            posicao = 21
        else:
            posicao = 19
        return  (datetime.strptime(_tabela[posicao].text, '%d/%m/%Y'),_tabela[posicao].text)
    except:
        return (None, None)

def cotacao(_ativo, _data):
    """
    Busca no site IBOVX a cotação do ativo na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _ativo: código do ativo
    :param _data: data da cotação

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes(_ativo, **kwargs):
    """
    Busca no site IBOVX a cotação do ativo na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _ativo: código do ativo
    :param data_inicio: data da primeira cotação, defautl = 01/01/2019
    :param pregoes: quantidade de pregoes retornados = 300

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes_historicas(ativo, **kwargs):
    '''
    Carrega as cotações históricas de um ativo

    Args:
        ativo: ticker do ativo
        **kwargs:
            pregoes: quantidade de pregões retornados
            data_inicio: data do pregão mais antigo a ser retornado. Se não houve pregão nesta data, retorna o primeiro
                        pregão após esta data

    Returns:
        caso não seja passado o ticker do ativo (independentemente dos outros parâmetros):
            mensagem: Ativo não pode ser ''.
        caso o argumento data_inicio não seja uma data válida (e não tenha acontecido as situação acima):
            mensagem: Data 'DD/MM/YYYY' é inválida.
        se forem passados ambos os argumentos, vale o número de pregões
        se não for passado nenhum argumento, serão retornados os dados do último pregão

        lista de tuples com os seguintes dados:
            ativo
            data da cotação
            variação de preço percentual
            variação de preço em valor
            cotação
            preço de abertura
            preço mínimo
            preço máximo
            volume financeiro (ordem de grandeza)
            número de negócios


    '''

    if ativo == '':
        return "Ativo não pode ser ''"
    __param = {}
    for __item in kwargs:
        __param[__item.upper()] = kwargs[__item]
    try:
        pregoes = __param['PREGOES']
        __modo_pregoes = True
    except KeyError:
        # data_inicio = datetime.strptime('01/01/2019', '%d/%m/%Y')
        pregoes = 0
        __modo_pregoes = False
    try:
        data_inicio = __param['DATA_INICIO']
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
    except (KeyError, ValueError):
        if not __modo_pregoes and len(__param) > 0:
            return "Data '" + data_inicio + "' é inválida."
        else:
            data_inicio = ''
            __modo_pregao = True

    if pregoes == 0 and data_inicio == '':
        pregoes = 1
        __modo_pregoes = True
    elif pregoes == 0 and data_inicio != '':
        pregoes = (datetime.now() - data_inicio).days
        __modo_pregoes = False

    __url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + ativo + '&qtdpregoes=' + str(pregoes)
    __r = requests.get(__url, headers=constants.Header.header)
    __soup = BeautifulSoup(__r.text, 'lxml')
    if __soup.text.find('Papel não encontrado ou sem histórico.') >= 0:
        return "Ativo '" + ativo.upper() + "' não encontrado."
    __tabela = __soup.find_all('td')
    __i = len(__tabela)
    __cotacoes = []
    if __tabela[20].text == 'Nº Negócios':
        __incremento = 9
    else:
        __incremento = 7

    while __i >= 0:
        try:
            __data = datetime.strptime(__tabela[__i - __incremento + 0].text, '%d/%m/%Y')
        except ValueError:
            break
        __variacao_perc = funcs.num_ptb2us(__tabela[__i - __incremento + 1].text)
        __variacao_num = funcs.num_ptb2us(__tabela[__i - __incremento + 2].text)
        __cotacao = funcs.num_ptb2us(__tabela[__i - __incremento + 3].text)
        __abertura = funcs.num_ptb2us(__tabela[__i - __incremento + 4].text)
        __minimo = funcs.num_ptb2us(__tabela[__i - __incremento + 5].text)
        __maximo = funcs.num_ptb2us(__tabela[__i - __incremento + 6].text)
        __volumme = funcs.num_ptb2us(__tabela[__i - __incremento + 7].text)
        __negocios = funcs.num_ptb2us(__tabela[__i - __incremento + 8].text)
        if __tabela[__i - __incremento - 1].text.find('bannerresponsivoabaixomenu') > 0:
            __skip = 1
        else:
            __skip = 0
        __cotacoes.append((ativo, __data, __variacao_perc, __variacao_num, __cotacao, __abertura, __minimo, __maximo,
                           __volumme, __negocios))

        __i = __i - __incremento - __skip

    __cotacoes_final = []
    __cotacoes = sorted(__cotacoes, key=lambda x: x[1], reverse=True)
    # __cotacoes.sort(key=takeDate, reverse = True)
    if __modo_pregoes:
        __pregoes_carregados = len(__cotacoes)
        for __id, __linha in enumerate(__cotacoes):
            if __id < pregoes:
                __cotacoes_final.append(__linha)
    else:
        for __linha in __cotacoes:
            if __linha[1] >= data_inicio:
                __cotacoes_final.append(__linha)

    # return "Modo pregões = " + str(__modo_pregoes), "Quantidade de registros = " + str(len(__cotacoes_final)), "Parêmetro pregões = " + str(pregoes), "Última data dos registros = " + str(__cotacoes_final[len(__cotacoes_final)-1][1]), "Parâmetro data de início = " + str(data_inicio)
    return __cotacoes_final