import requests
import json
import hashlib
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


periodos = [838672, 838670, 838667, 838665, 838662, 838664, 810191, 810190, 810188, 810186, 810164, 810149, 810172, 810145, 810156, 810168, 810160, 810189, 810187, 810185, 810184, 810155, 810167, 810144, 810148, 810159, 810163, 810171, 810152, 810183, 810181, 810180, 810175, 810166, 810162, 810170, 810158, 810143, 810151, 810147, 810154, 810176, 810174, 838676, 838666, 838661, 810157, 810153, 810142, 810169, 838674, 838675, 810161, 810146, 810165, 810150, 838659, 838679, 810173, 838673, 810141, 810140, 838663, 810133, 810126, 810130, 810106, 810122, 810102, 810118, 810110, 810114, 810137, 838681, 810136, 810132, 810125, 810101, 810117, 810129, 810109, 810113, 810121, 810105, 810134, 838680, 810131, 838669, 810108, 810128, 810112, 810124, 810104, 810100, 810116, 810120, 838677, 838671, 838668, 810099, 810111, 810123, 810107, 810115, 810103, 810119, 810127, 838658, 838657, 810098, 810062]
contador = 0
contador2 = 0
tamanho = len(periodos)
payload = []
for i in periodos:
    chave = hashlib.md5(str(i).encode()).hexdigest()
    payload.append(
        {
            "idGerado": f"{i}",
            "conteudo": {
                "id": i
            }
        }
    )

    contador += 1
    if contador % 100 == 0 or contador == tamanho:
        payload = json.dumps(payload)
        print(payload)
        url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias"

        headers = {
            'Authorization': AUTORIZACAO,
            'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        response = response.json()
        print(response)

        payload = []
        contador2 += 1
        print("lote:", contador2)
print("total registros:", contador)