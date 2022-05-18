import json
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


import requests
from time import sleep

url = "https://folha.betha.cloud/folha/api/folha/listagem-folhas?filter=(numero = \"2088\")"

payload={}
headers = {
  'Authorization': TOKENUSER,
  'User-Access': ACCESSUSER
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
contador = 0
contador2 = 0
calculos = []
calculosDecimo = []
folhas = []
for i in response['content']:
  mandar = False
  if i['tipoProcessamento'] == "MENSAL":
    sleep(3)
    url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/{i['calculo']['id']}"

    headers = {
      'Authorization': AUTORIZACAO,
      'Content-Type': 'application/json'
    }
    response2 = requests.request("GET", url, headers=headers, data=payload)
    response2 = response2.json()
    for k in response2['calculoFolhaMatriculas']:
      k.pop('version')
      k.pop('id')
      if k['matricula']['id'] == 2816733:
        calculos.append(response2['id'])
        # mandar = True
        # k['matricula']['id'] = 2816733
    # if mandar:
    #   contador+=1
    #   response2['conversao']= True
    #   payload2 = json.dumps([{
    #     "conteudo": response2
    #   }])
    #   print(payload2)
    #   url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/"
    #   headers = {
    #     'Authorization': 'Bearer 4ff07b6b-1160-4981-8bba-a9765e460e6f',
    #     'Content-Type': 'application/json'
    #   }
    #   response3 = requests.request("POST", url, headers=headers, data=payload2)
    #   response3 = response3.json()
    #   print(f"{contador} calculo",response3)
  elif i['tipoProcessamento'] == "DECIMO_TERCEIRO_SALARIO":
    sleep(3)
    url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-decimo-terceiro/{i['calculo']['id']}"
    headers = {
      'Authorization': AUTORIZACAO,
      'Content-Type': 'application/json'
    }

    response2 = requests.request("GET", url, headers=headers, data=payload)
    response2 = response2.json()
    for k in response2['calculoFolhaMatriculas']:
      k.pop('version')
      if k['matricula']['id'] == 2816733:
        calculosDecimo.append(response2['id'])
        # mandar = True
        # k['matricula']['id'] = 4870416
    # if mandar:
    #   contador+=1
    #   response2['conversao'] = True
    #   payload2 = json.dumps([{
    #     "conteudo": response2
    #   }])
    #   print(payload2)
    #   url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-decimo-terceiro/"
    #   headers = {
    #     'Authorization': AUTORIZACAO,
    #     'Content-Type': 'application/json'
    #   }
    #   response3 = requests.request("POST", url, headers=headers, data=payload2)
    #   response3 = response3.json()
    #   print(f"{contador} calculo",response3)
  if i['matricula']['id'] == 2816733:
    folhas.append(i['id'])
    # contador2 +=1
    # payload3 = json.dumps([{
    #   "conteudo": {
    #     "id":i["id"],
    #     "matricula":{
    #       "id": 2816733
    #     }
    #   }
    # }])
    # print(payload3)
    # url = f"https://pessoal.betha.cloud/service-layer/v1/api/folha/"
    # headers = {
    #   'Authorization': AUTORIZACAO,
    #   'Content-Type': 'application/json'
    # }
    # response4 = requests.request("POST", url, headers=headers, data=payload3)
    # response4 = response4.json()
    # print(f"{contador} folha", response4)
print(calculos)
print(calculosDecimo)
print(folhas)