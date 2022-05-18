import requests
import json
from configuracao.conexao import AUTORIZACAO


headers = {
      'Authorization': AUTORIZACAO,
      'Content-Type': 'application/json'
    }
hasNext = True
limit = 100
offset = 0
contador = 0
contador2 = 0
enviar = []
ids = []
while hasNext:
    url = f"https://pessoal.betha.cloud/service-layer/v1/api/historico-matricula?offset={offset}&limit={limit}"

    payload={}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    offset += limit
    total = response['total']
    hasNext = response['hasNext']
    # hasNext = False
    for i in response['content']:
        contador +=1

        if 'registraPonto' in i and i['registraPonto']:
            i.pop('version')
            i['registraPonto'] = None
            enviar.append({
                "idIntegracao": "sla",
                "conteudo": i
            })
        if contador == len(response['content']):
            contador = 0
            if len(enviar)>0:
                contador2 +=1
                url = "https://pessoal.betha.cloud/service-layer/v1/api/historico-matricula/"
                payload = json.dumps(enviar)
                enviar = []
                response = requests.request("POST", url, headers=headers, data=payload)
                response = response.json()
                ids.append(response['id'])
                print(f"\r Lotes Enviados: {contador2}",end="")
print("\n")
print(ids)
