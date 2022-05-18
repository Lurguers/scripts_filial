import requests
import json
import hashlib
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


periodos = [838670, 838664, 838665, 838672, 838667, 838678, 838662, 810191, 810190, 810188, 810186, 810149, 810168, 810172, 810145, 810156, 810164, 810160, 810189, 810187, 810185, 810184, 810155, 810148, 810144, 810159, 810167, 810152, 810163, 810171, 810183, 810181, 810180, 810175, 810158, 810166, 810170, 810154, 810162, 810147, 810151, 810143, 810176, 810174, 838659, 810165, 838674, 810142, 810153, 838675, 810169, 810161, 810146, 838676, 810173, 838679, 810150, 838661, 838666, 838673, 810157, 810141, 810140, 838663, 810133, 810130, 810126, 810110, 810114, 810118, 810106, 810102, 810122, 810137, 838681, 810136, 810132, 810101, 810109, 810113, 810129, 810125, 810117, 810105, 810121, 810134, 838680, 810131, 810124, 838669, 810100, 810128, 810104, 810112, 810108, 810116, 810120, 838677, 838671, 810099, 810123, 810103, 810119, 810115, 810111, 810107, 838668, 810127, 838658, 838657, 810098, 810062]
contador = 0
contador2 = 0
tamanho = len(periodos)
payload = []
for i in periodos:
    chave = hashlib.md5(str(i).encode()).hexdigest()
    payload.append(
        {
            "idIntegracao": chave,
            "conteudo": {
                "id": i,
                "situacao": "QUITADO"
            }
        }
    )

    contador += 1
    if contador % 100 == 0 or contador == tamanho:
        payload = json.dumps(payload)
        url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias"

        headers = {
            'Authorization': TOKENUSER,
            'Content-Type': ACCESSUSER
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        print(response)

        payload = []
        contador2 += 1
        print("lote:", contador2)
print("total registros:", contador)