import json
from requests import *
from configuracao.conexao import AUTORIZACAO


url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/movimento-periodo-aquisitivo-licenca-premio?limit=200"

payload={}
headers = {
  'Authorization': AUTORIZACAO,
  'content-type': 'application/json'
}
payload2 = []
response = get(url, headers=headers, data=payload)
response = response.json()
contador = 0
contador2 = 0
tamanho = len(response['content'])
print(tamanho)
contador3 = 0
for i in response['content']:
  url2 = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/movimento-periodo-aquisitivo-licenca-premio?force=true"
  payload2.append(
    {
      "idGerado": str(i['id']),
      "conteudo": {
        "id": int(i['id'])
      }
    }
  )
  contador += 1
  if contador % 100 == 0 or contador == tamanho:
    payload2 = json.dumps(payload2)
    response2 = delete(url2, headers=headers, data=payload2)
    # response2 = requests.request("DEL", url2, headers=headers, data=payload2)
    print(response2.json())
    print(payload2)
    payload2 = []
    contador2 += 1
    print("lote:", contador2)
print("total registros:", contador)