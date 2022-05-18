import json

import requests
from configuracao.conexao import AUTORIZACAO


payload={}
headers = {
  'Authorization': AUTORIZACAO
}
hasNext= True
contador = 0
limit =99
offset =000
lista =[]
while hasNext:
    url = f"https://educacao.betha.cloud/service-layer/v2/api/turma-tipos-avaliacoes?offset={offset}&limit={limit}"
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    hasNext = response['hasNext']
    contador += 1
    offset += limit
    print(f"\r{contador}/{round(response['total']/limit)}",end ="")
    for i in response['content']:
        if i['turma']['id'] == 11267481:
            # print('turma')
            if i['itemEducacional']['descricao'] == 'Língua Alemã':
                lista.append(i)
print('\n')
print(lista)
#
for l in lista:
    url = "https://educacao.betha.cloud/service-layer/v2/api/turma-tipos-avaliacoes/"


    payload = json.dumps([
        {
            "idIntegracao": f"{l['id']}",
            "conteudo": {
                "id": l['id']
            }
        }
    ])
    print(payload)
    headers = {
        'Authorization': AUTORIZACAO,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)