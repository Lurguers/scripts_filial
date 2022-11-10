
import csv

contador = 0
total = 0
for i in open('../../Área de Trabalho/04-11.csv'):
    lista = i.split(',')
    print(i)

    if contador != 0:
        exit()
    contador += 1
    if 'entidade.id' in lista[11] and '32' in lista[11] and 'exercicio.ano' in lista[11] and '2021' in lista[11]:
        print(i.split('filter=')[1].split('&')[0])
        # contador += 1
        # total += int(lista[7])
# print('contador', contador)
# print('total', total)
# print('média', total/contador)
#
# import requests
# import json
#
# tipos = ['fontes-dinamicas','scripts']
# lista = []
# for j in tipos:
#     hasNext = True
#     limit = 100
#     offset = 0
#     while hasNext:
#
#         url = f"https://plataforma-scripts.betha.cloud/scripts/v1/api/{j}/pesquisa"
#
#         payload = json.dumps({
#             "offset": offset,
#             "limit": limit,
#             "filter": ""
#         })
#         headers = {
#           'Authorization': 'Bearer b59ac966-ee23-4fbe-8e2e-42f4a4b6c4c1',
#           'User-Access': '83USJGkt2jt5GHI70m94aDqr-yppq8GTrdYe-tgcUvY=',
#           'Content-Type': 'application/json'
#         }
#
#         response = requests.request("POST", url, headers=headers, data=payload)
#         # print(response)
#         response = response.json()
#         hasNext = response['hasNext']
#         offset = offset + limit
#         for i in response['content']:
#
#             url = f"https://plataforma-scripts.betha.cloud/scripts/v1/api/{j}/{i['id']}"
#
#             payload = {}
#
#             response2 = requests.request("GET", url, headers=headers, data=payload)
#             response2 = response2.json()
#             if 'movimentacaoBalanceteMensalDespesa' in response2['revisao']['codigoFonte']:
#
#                 response3 = requests.request("GET", url+'/flexibilizacao', headers=headers, data=payload)
#
#                 if response3.content == b'':
#                     lista.append([response2['id'], response2['titulo']])
#                 else:
#                     response3 = response3.json()
#                     if response3['entidadeOrigemId'] != 3890:
#                         lista.append([response2['id'], response2['titulo']])
#
# for j in lista:
#     print('lista['+str(j[0])+'] = "'+j[1]+'"')
