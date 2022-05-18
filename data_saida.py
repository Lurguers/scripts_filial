import requests
import json
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


url = "https://folha.betha.cloud/folha/api/matricula/listagem-matricula?ativos=false&filter=cargo.id+in+(271669)&limit=50&offset=0&selecaoAvancada=id+in+(11168)&sort="

payload={}
headers = {
    'Authorization': TOKENUSER,
    'User-Access': ACCESSUSER
  }

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
conta =0

for i in response['content']:

  url2 = f"https://folha.betha.cloud/folha/api/folha/listagem-folhas?filter=((numero+%3D+%22{i['numero']}%22))+and+(((tipoProcessamento+%3D+%22RESCISAO%22+and+subTipoProcessamento+%3D+%22INTEGRAL%22)))"

  response2 = requests.request("GET", url2, headers=headers, data=payload)
  response2 = response2.json()

  url3 = f"https://folha.betha.cloud/folha/api/calculo-folha/{response2['content'][0]['calculo']['id']}"
  response3 = requests.request("GET", url3, headers=headers, data=payload)
  response3 = response3.json()

  url4 = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/rescisao/"

  payload2 = json.dumps([
    {
      "conteudo": {
        "data": response3['dataRescisao'],
        "saldoFgts": response3['calculoFolhaMatriculas'][0]['saldoFgts'],
        "fgtsMesAnterior": response3['calculoFolhaMatriculas'][0]['fgtsMesAnterior'],
        "ato": None,
        "matricula": {
          "id": response3['calculoFolhaMatriculas'][0]['matricula']['id'],
        },
        "avisoPrevio": response3['avisoPrevio'],
        "motivoRescisao": {
          "id": response3['motivoRescisao']['id']
        }
      }
    }
  ])
  headers2 = {
    'Authorization': AUTORIZACAO,
    'Content-Type': 'application/json'
  }
  print(payload2)
  response = requests.request("POST", url4, headers=headers2, data=payload2)
  # conta +=1
  print(response.text)
# print(conta)
