import json
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER, APPCONTEXT
import requests

offset = 0
limit = 20
pagina = 0
hasNext = True
contador = 0
while hasNext:
    url = f"https://saude.cloud.betha.com.br/saude/api/conveniosProcedimentos?filter=(convenio.id+in(10)+)&limit={limit}&offset={offset}"
    payload={}
    headers = {
      'user-access': ACCESSUSER,
      'authorization': TOKENUSER,
      'app-context': APPCONTEXT,
      'Content-Type': 'application/json'
    }


    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    pagina += 1
    offset = pagina * limit
    hasNext = response['hasNext']
    # hasNext = False
    for i in response['content']:
        contador += 1
        if i['acrescimo'] == 15.0:
            i.update(
                {
                "convenio": {
                    "id": 10,
                    "descricao": "SUS",
                    "version": 0
                },
                "tipoConvenioProcedimento": {
                    "id": 4626,
                    "classificacaoPai": None,
                    "nome": "Procedimento",
                    "tipoClassificacao": "TIPO_CONVENIO_PROCEDIMENTO",
                    "atributo1": "PROCEDIMENTO",
                    "atributo2": None,
                    "atributo3": None,
                    "atributo4": None
                },
                "tabela": i['procedimento']['tabela']
            })
            i['acrescimo'] = 30.0
            i['procedimento'].pop('tabela')

            url2 = "https://saude.cloud.betha.com.br/saude/api/conveniosProcedimentos"

            payload2 = json.dumps(i)

            response2 = requests.request("PUT", url2, headers=headers, data=payload2)
            # print(response2)
        print(f"\r Procedimento {contador}",end="")

