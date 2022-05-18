import json
from requests import *
from configuracao.conexao import AUTORIZACAO

url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-licenca-premio?limit=200"

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
  url2 = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-licenca-premio/"
  # if i['movimentacoes']:
  #   i['movimentacoes'] = []
  #   i.pop('version')
  #   i.pop('configuracaoLicencaPremio')
  #   payload3 = [
  #     {
  #       "idIntegracao": str(i['id'])+'remove_mov',
  #       "conteudo": {
  #         "id": i['id'],
  #         "movimentacoes": []
  #       }
  #     }
  #   ]
  #   payload3 = json.dumps(payload3)
  #   print(payload3)
  #   response3 = post(url2, headers=headers, data=payload3)
  #   response3 = response3.json()
  #   print(response3)
  #   aguardando = True
  #   while aguardando:
  #     sleep(3)
  #     contador3 +=1
  #     lote = funcoes.lotes(response3['id'])
  #     print(f"\rAGUARDANDO_EXECUCAO tentativa{contador3}", end="")
  #     if lote['situacao'] != 'EXECUTADO':
  #       continue
  #     print(f"\rEXECUTADO tentativa{contador3}")
  #     aguardando = False
  #     for j in range(0, len(lote['retorno'])):
  #       idGerado = lote['retorno'][j]['idGerado']
  #       mensagem = lote['retorno'][j]['mensagem']
  #       if not idGerado:
  #         print(f"\rERRO tentativa{contador3}")
  #         print(
  #           f"Erro no lote {response3['id']}",
  #           mensagem)
  #         exit(1)
  #         continue

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