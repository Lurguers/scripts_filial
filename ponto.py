import json
from datetime import datetime
from json import dumps

from dotenv import load_dotenv
from requests import get, post
from os.path import join, dirname
from os import getenv

load_dotenv(join(dirname(__file__), '.env'))
USUARIO = getenv("USUARIO")
AUTORIZACAO = getenv("AUTORIZACAO")
if not (AUTORIZACAO.lower().startswith('bearer')):
    AUTORIZACAO = f'bearer {AUTORIZACAO}'


def buscar():
    try:
        proximo = True
        limite = 500
        pagina = 0
        dado = []
        while proximo:
            print(f'\r- Realizando busca na página {pagina + 1}', end='')
            requisicao = get(url='https://pontual.betha.cloud/pontual/api/pessoal/matriculas/',
                             params={
                                 'offset': pagina * limite,
                                 'limit': limite
                             },
                             headers={
                                 'Authorization': AUTORIZACAO,
                                 'User-access': USUARIO
                             })
            if requisicao.ok:
                json = requisicao.json()
                for conteudo in json['content']:
                    dado.append(conteudo)
                proximo = json['hasNext']
                pagina += 1
            else:
                raise Exception(requisicao.json())
        print('\n- Busca de página(s) finalizada')
        f = open("colaborador.json", "w", encoding="utf-8")
        dado = sorted(dado, key=lambda k: k['id'], reverse=False)
        f.write(dumps(dado, indent=4, sort_keys=True, ensure_ascii=False))
        f.close()
    except Exception as e:
        print(f'\n* Erro durante a execução da função "buscar" {e}')


def solicitacao(marcacao):
    try:
        for m in marcacao:
            for h in m['marcacao']:
                s = {
                    "requerente": {
                        "id": 1611
                    },
                    "funcaoRemocao": None,
                    "dataHoraMarcacaoRemocao": None,
                    "tipo": "INCLUSAO",
                    "dataHoraMarcacao": f"{m['data']} {h}",
                    "funcao": {
                        "id": 3
                    },
                    "motivo": "Esquecimento"
                }
                # print(s)
                requisicao = post(url='https://pontual.betha.cloud/pontual/api/admin/solicitacoes',
                                  data=dumps(s),
                                  headers={
                                      'Authorization': AUTORIZACAO,
                                      'User-access': USUARIO,
                                      'Content-type': 'application/json',
                                  })
                if requisicao.ok:
                    json = requisicao.json()
                    print(f"Marcação inserida com sucesso - {m['data']} {h}")
                    # print(json)
                else:
                    raise Exception(requisicao.json())
        print('\n- Envio finalizado')
    except Exception as e:
        print(f'\n* Erro durante a execução da função "solicitacao" {e}')


def pegar_aniver():
    f = open("equipe.txt", "r", encoding="utf-8")
    line = f.read()
    line = json.loads(line)
    contador =0
    c = open("colaborador.json", "r", encoding="utf-8")
    linec = c.read()
    linec = json.loads(linec)
    lista = []
    for i in line:

        # print(i['nome'])
        for j in linec:

            if j['pessoa']['nome'].strip().upper() == i['nome_completo'].strip().upper() and {'nome':i['nome_completo'], 'nasc':datetime.strptime(j['pessoa']['dataNascimento'],"%Y-%m-%d").replace(year =2022).strftime('%d/%m/%Y')} not in lista:
                lista.append({'nome':i['nome_completo'], 'nasc':datetime.strptime(j['pessoa']['dataNascimento'],"%Y-%m-%d").replace(year =2022).strftime('%d/%m/%Y')})
                contador +=1
    lista.sort(key=lambda x: x["nasc"])
    for k in lista:
        print(k['nome']+',',k['nasc'])




if __name__ == '__main__':
    # buscar()
    pegar_aniver()
    # solicitacao([
    #     # {'data': '2021-12-06', 'marcacao': ['12:10','13:15', '17:50']},
    #     # {'data': '2021-12-07', 'marcacao': ['08:05', '12:10', '13:20', '17:50']},
    #     # {'data': '2021-12-08', 'marcacao': ['08:00', '12:10', '13:20', '17:50']},
    #     # {'data': '2021-12-09', 'marcacao': ['07:55', '12:00', '13:05', '18:30']},
    #     # {'data': '2021-12-10', 'marcacao': ['08:00', '12:00', '13:05', '17:50']},
    #     # {'data': '2021-12-13', 'marcacao': ['08:05', '12:00', '13:05', '17:35']},
    #     # {'data': '2021-12-14', 'marcacao': ['08:05', '12:10', '13:15', '17:50']},
    #     # {'data': '2021-12-15', 'marcacao': ['08:15', '12:00', '13:05', '18:10']},
    #     # {'data': '2021-12-16', 'marcacao': ['08:10', '12:05', '13:10', '18:00']},
    #     # {'data': '2021-12-17', 'marcacao': ['08:00', '12:00', '13:05', '17:42']}
    # ])

