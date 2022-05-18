import pyodbc
import json
import requests
from time import sleep
from hashlib import md5
from configuracao.conexao import conectar, executar, consultar, AUTORIZACAO


def lotes(id: str) -> json:
    url2 = f'https://pessoal.cloud.betha.com.br/service-layer/v1/api/lote/lotes/{id}'
    payload2 = {}
    headers2 = {
        'Authorization': AUTORIZACAO
    }
    response2 = requests.request("GET", url2, headers=headers2, data=payload2)
    return response2.json()


def update_lotes(tipo: str):
    consulta = consultar(
        f"""SELECT * FROM bethadba.controle_migracao_lotes cml WHERE tipo_registro = '{tipo}' AND Status = 1""")
    for l in consulta:
        aguardando = True
        while aguardando:
            sleep(3)
            lote = lotes(l['id_lote'])
            if lote['situacao'] != 'EXECUTADO':
                continue
            aguardando = False
            for j in range(0, len(lote['retorno'])):
                idGerado = lote['retorno'][j]['idGerado']
                mensagem = lote['retorno'][j]['mensagem']
                if not idGerado:
                    print(f"Erro no lote {l['id_lote']} e seq {l['i_sequencial']} no id {idGerado} e chave {lote['retorno'][j]['idIntegracao']}",mensagem)
                    continue
        executar(f"""UPDATE bethadba.controle_migracao_lotes SET Status = 3 WHERE i_sequencial = {l['i_sequencial']}""")
        print(f"Lote {l['id_lote']} e seq {l['i_sequencial']} inserido com sucesso!")

def encurtar(*lista_chave):
    texto = ''
    hash_chave = None
    try:
        for chave in lista_chave:
            texto += str(chave)
        hash_chave = md5(texto.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f'\n* Erro durante a execução da função "encurtar" {e}')
    finally:
        return hash_chave