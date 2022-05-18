import json
from time import sleep
import requests
import funcoes
import hashlib
from datetime import datetime, timedelta
from configuracao.conexao import AUTORIZACAO


resultado = funcoes.consultar("""
SELECT TOP 1 START AT 1
   	NULLIF(list(DISTINCT IF cmr.tipo_registro = 'periodo-aquisitivo-ferias' THEN cmr.id_gerado ELSE NULL ENDIF),'')             AS id_periodo_cloud,
   	List(IF cmr.tipo_registro = 'periodo-aquisitivo-ferias' THEN pf.i_periodos_ferias ELSE NULL ENDIF)                          AS movimentacao,
   	List(IF cmr.tipo_registro = 'periodo-aquisitivo-ferias' THEN pf.tipo ELSE NULL ENDIF)                                       AS tipo_movimentacao,
   	List(IF cmr.tipo_registro = 'periodo-aquisitivo-ferias' THEN pf.dt_periodo ELSE NULL ENDIF)                                 AS dt_periodo,
   	List(IF cmr.tipo_registro = 'periodo-aquisitivo-ferias' THEN pf.num_dias  ELSE NULL ENDIF)                                  AS num_dias,
   	List(DISTINCT IF cmr.tipo_registro = 'calculo-folha-ferias' THEN cmr.id_gerado ELSE NULL ENDIF) 		                    AS calculoFolhaFerias,
   	List(DISTINCT cmrm.id_gerado)                                                                                               AS id_matricula_cloud
FROM   
   	bethadba.periodos_ferias pf 
	INNER JOIN 
		bethadba.controle_migracao_registro cmr 
	ON (pf.i_entidades = cmr.i_chave_dsk1 AND pf.i_funcionarios = cmr.i_chave_dsk2 AND pf.i_periodos = cmr.i_chave_dsk3)
	INNER JOIN 
		bethadba.controle_migracao_registro cmrm 
	ON (pf.i_entidades = cmrm.i_chave_dsk1 AND pf.i_funcionarios = cmrm.i_chave_dsk2)
WHERE 
	cmr.tipo_registro IN ('periodo-aquisitivo-ferias','calculo-folha-ferias')
	AND cmrm.tipo_registro IN ('matricula')
	AND cmr.id_gerado IN ( 797622 )  
GROUP BY 
	pf.i_entidades, pf.i_funcionarios, pf.i_periodos 
    HAVING id_periodo_cloud IS NOT NULL
ORDER BY 
	pf.i_funcionarios    
""")

contador = 0
contador2 = 0
payload = []
tamanho = len(resultado)
for i in resultado:
    movimentos = i['movimentacao'].split(',')
    tipo_movimentos = i['tipo_movimentacao'].split(',')
    dt_periodos = i['dt_periodo'].split(',')
    num_dias = i['num_dias'].split(',')
    calculoFolhaFerias = i['calculoFolhaFerias'].split(',')
    movimentacaoes = []
    k = 0
    for j in range(len(movimentos)):
        abono = 0.0
        gozo = 0.0
        falta = 0.0
        rescisao = 0.0
        tipo = ""
        ferias = None
        if tipo_movimentos[j] == '1':
            continue
        elif tipo_movimentos[j] == '2':
            tipo = "CONCESSAO"
            gozo = float(num_dias[j])
            if calculoFolhaFerias != ['']:
                if len(calculoFolhaFerias) >= k+1:
                    ferias = {
                        "matricula": {
                            "id": int(i['id_matricula_cloud'])
                        },
                        "calculoFolhaFerias": {
                            "id": int(calculoFolhaFerias[k])
                        },
                        "tipoAfastamento": {
                            "id": 10408
                        },
                        "ato": None,
                        "tipoCalculoFerias": "INDIVIDUAL",
                        "dataPagamento": dt_periodos[j],
                        "dataInicioGozo": dt_periodos[j],
                        "dataFimGozo": str((datetime.strptime(dt_periodos[j], '%Y-%m-%d')+ timedelta(days=float(num_dias[j]))).date()),
                        "diasGozo": gozo,
                        "diasAbono": abono,
                        "descontarFalta": False,
                        "faltasBrutas": falta,
                        "faltasEnquadradas": falta,
                        "faltas": falta,
                        "pagarUmTercoIntegral": False,
                        "coletiva": False,
                        "pagar13SalarioAdiantado": False,
                        "ano13Salario": None,
                        "observacao": None
                    }
                    k += 1
        elif tipo_movimentos[j] == '3':
            tipo = "CONCESSAO"
            abono = float(num_dias[j])
        elif tipo_movimentos[j] == '5':
            tipo = "CANCELAMENTO"
            # data cancelamento
        elif tipo_movimentos[j] == '6':
            tipo = "CONCESSAO"
            rescisao = float(num_dias[j])
        elif tipo_movimentos[j] == '7':
            continue
        if tipo == "CONCESSAO":
            movimentacaoes.append(
                {
                    "tipo": tipo,
                    "dataMovimento": dt_periodos[j]+" 00:00:00.000",
                    "quantidade": float(num_dias[j]),
                    "dataInicioGozo": dt_periodos[j],
                    "dataFimGozo": str((datetime.strptime(dt_periodos[j], '%Y-%m-%d')+ timedelta(days=float(num_dias[j]))).date()),
                    "dataPagamento": dt_periodos[j],
                    "diasAbono": abono,
                    "diasGozo": gozo,
                    "diasFalta": falta,
                    "diasPagosRescisao": rescisao,
                    "ferias": ferias
                }
            )
        else:
            movimentacaoes.append(
                {
                    "tipo": tipo,
                    "dataMovimento": dt_periodos[j] + " 00:00:00.000",
                    "dataCancelamento": dt_periodos[j],
                    "quantidade": float(num_dias[j])
                }
            )

    # fazer md5
    chave = hashlib.md5((i["id_periodo_cloud"]+i["id_matricula_cloud"]).encode()).hexdigest()

    payload.append(
        {
            "idIntegracao": chave,
            "conteudo": {
                "id": int(i['id_periodo_cloud']),
                "matricula": {
                    "id": int(i['id_matricula_cloud'])
                },
                "movimentacoes": movimentacaoes
            }
        }
    )

    contador += 1
    if contador % 100 == 0 or contador == tamanho:
        payload = json.dumps(payload)
        url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias"
        headers = {
            'Authorization': AUTORIZACAO,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        insersao = funcoes.executar(f"""
         INSERT INTO bethadba.controle_migracao_lotes
            (sistema,
             tipo_registro,
             usuario,
             url_consulta,
             status,
             id_lote)
         VALUES      
            (300,
             'movimentacoes',
             'lucas.dornelles',
             'https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias',
             1,
             '{response["id"]}')  
        """)

        payload = []
        contador2 += 1
        print("lote:",contador2)
print("total registros:",contador)

sleep(10)
funcoes.update_lotes('movimentacoes')


