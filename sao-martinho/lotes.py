from time import sleep
import requests
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


executado = True

while executado:
    sleep(3)
    url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/lote/lotes/611c1c1a967e54000877aaa8"

    payload={}
    headers = {
      'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    if response['situacao'] == "EXECUTADO":
        print('executado')
        executado = False
