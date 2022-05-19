import requests
import json
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


url = "https://folha.betha.cloud/folha/api/matricula/listagem-matricula?filter=(rescisao.data+is+null+and+situacao+in+(%22DEMITIDO%22))&limit=1000&offset=0&sort=rescisao.data+desc"

payload={}
headers = {
    'Authorization': TOKENUSER,
    'User-Access': ACCESSUSER
  }

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
conta =0
contador =0
tamanho = len(response['content'])
ids = []
for i in response['content']:
  if i['rescisao.data'] is not None:
    conta += 1
    continue
  contador += 1
  # print(i['numero'])
  url2 = f"https://folha.betha.cloud/folha/api/afastamento?filter=((matricula.codigo.numero+%3D+%22{i['numero']}%22))+and+(decorrente+in+(%22RESCISAO%22))&limit=20&offset=0&sort="
  # print(url2)
  response2 = requests.request("GET", url2, headers=headers, data=payload)
  response2 = response2.json()
  if len(response2['content']) == 0:
    conta += 1
    continue
  for j in response2['content']:
    # print(j['matricula']['descricao'], str(i['numero']))
    if j['matricula']['descricao'] != str(i['numero']):
      conta += 1
      continue

    url4 = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/rescisao/"

    payload2 = json.dumps([
      {
        "conteudo": {
          "data": j['inicioAfastamento'],
          "saldoFgts": 0,
          "fgtsMesAnterior": False,
          "ato": None,
          "matricula": {
            "id": j['matricula']['id'],
          },
          "avisoPrevio": None,
          "motivoRescisao": {
            "id": 13770 # alterar
          }
        }
      }
    ])
    headers2 = {
      'Authorization': AUTORIZACAO,
      'Content-Type': 'application/json'
    }

    print(f"\rFazendo {contador}/{tamanho}",payload2, end="")
    response = requests.request("POST", url4, headers=headers2, data=payload2)
    response = response.json()
    ids.append(response['id'])
print('\n')
print('ids:',ids)
print(conta)
