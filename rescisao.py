import requests
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


hasNext = True
limit = 1000
offset = 0
contador = 0
contador2 =0

while hasNext:

    url = f"https://pessoal.cloud.betha.com.br/service-layer/v1/api/rescisao?limit={limit}&offset={offset}"

    payload={}
    headers = {
      'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    hasNext = response['hasNext']
    contador +=1
    offset = contador * limit

    for i in response['content']:
        contador2 += 1
        print(f"\r {contador2}/{response['total']}",end="")
        # if i['matricula']['id'] == 7499682:
        if i['matricula']['id'] == 7444992:
            print('achou',i)



