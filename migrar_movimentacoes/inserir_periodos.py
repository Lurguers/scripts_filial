import funcoes
import requests
from configuracao.conexao import AUTORIZACAO


hasNext = True
offset = 0
limit = 50
page = 1
while hasNext:
    url = f"https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias?limit={limit}&offset={offset}"

    payload = {}
    headers = {
        'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    offset = limit * page
    page += 1
    hasNext = response['hasNext']
    sqls = """"""
    for i in response['content']:
        sqls += f"""
            INSERT INTO bethadba.controle_migracao_registro
            SELECT 
                    300,
                    'periodo_aquisitivo',
                    hash('300'+'periodo_aquisitivo'+i_chave_dsk1+i_chave_dsk2+'{i['dataInicial']}'+'{i['dataFinal']}','md5'),
                    'Periodos aquisitivos gerados',
                    {i['id']} ,
                    i_chave_dsk1,
                    i_chave_dsk2,
                    '{i['dataInicial']}',
                    '{i['dataFinal']}',
                    null,
                    
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null                    
            FROM bethadba.controle_migracao_registro
            WHERE id_gerado = '{i['matricula']['id']}'
              AND tipo_registro = 'matricula';
        """
    funcoes.executar(sqls)
    print("inserido", page)
