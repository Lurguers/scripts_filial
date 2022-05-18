import time
import json
from hashlib import md5
from configuracao.conexao import AUTORIZACAO
import requests
import funcoes

start = time.time()

resultado = funcoes.consultar("""
                       SELECT 
   i_competencias,
   i_funcionarios AS funcionario,
   List((SELECT controle_migracao_registro.id_gerado
         FROM   bethadba.controle_migracao_registro
         WHERE  controle_migracao_registro.i_chave_dsk1 = i_eventos
                AND controle_migracao_registro.tipo_registro =
                    'configuracao-evento')) as eventosId,
   List(vlr_inf) as vlr_inf,
   List(vlr_calc) as vlr_calc,
   List(tipo_pd) as tipo_pd,
   List(compoe_liq) as compoe_liq,
   (SELECT controle_migracao_registro.id_gerado
    FROM   bethadba.controle_migracao_registro
    WHERE  controle_migracao_registro.i_chave_dsk2 =
           bethadba.movimentos.i_funcionarios
           AND controle_migracao_registro.tipo_registro = 'matricula') as matricula,
   (case 
   		when mov_resc = 'S' then 15
   		else i_tipos_proc
   	end) as i_tipos_proc,
   List(COALESCE((SELECT controle_migracao_registro.i_chave_dsk2
         FROM   bethadba.controle_migracao_registro
         WHERE  controle_migracao_registro.i_chave_dsk1 = i_eventos
                AND controle_migracao_registro.tipo_registro =
                    'configuracao-evento'),'null')) as eventosCla,
    (SELECT id_gerado from bethadba.controle_migracao_registro cmr where hash_chave_dsk = hash('300'||'folha'||cast(matricula as varchar)||LEFT(i_competencias,7)||(case i_tipos_proc when 15 then 'RESCISAO' when 11 then 'MENSAL'  when 80 then 'FERIAS'  when 52 then 'DECIMO_TERCEIRO_SALARIO' end), 'md5')) AS idFolha
    
FROM   bethadba.movimentos
WHERE  i_competencias in ('2009-01-01') and i_tipos_proc in (15,11) and idFolha is null
GROUP  BY i_competencias,
          i_funcionarios,
          i_tipos_proc,
          mov_resc
ORDER  BY i_competencias;
                        """)

end = time.time()
print("tempo SQL:", "{:.2f}".format((end - start)/60), "min")
print("total de registros SQL:", len(resultado))
contador = 0
enviar = []
ids = []
headers = {
    'Authorization': AUTORIZACAO,
    'Content-Type': 'application/json'
}
# for i in resultado:
#
#     tipoProc = ""
#     if i['i_tipos_proc'] == 15:
#         tipoProc = "RESCISAO"
#         url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-rescisao/"
#     elif i['i_tipos_proc'] == 11:
#         tipoProc = "MENSAL"
#         url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/"
#     elif i['i_tipos_proc'] == 80:
#         tipoProc = "FERIAS"
#         url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-ferias/"
#     elif i['i_tipos_proc'] == 52:
#         tipoProc = "DECIMO_TERCEIRO_SALARIO"
#         url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-decimo-terceiro/"
#     #
#     # url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/"
#     #
#     # payload = json.dumps([
#     #     {
#     #         "conteudo": {
#     #             "tipoProcessamento": tipoProc,
#     #             "subTipoProcessamento": "INTEGRAL",
#     #             "dataAgendamento": None,
#     #             "dataPagamento": i['i_competencias'].strftime("%Y-%m-28"),
#     #             "tipoVinculacaoMatricula": "TEMPORAL",
#     #             "calculoFolhaMatriculas": [
#     #                 {
#     #                     "matricula": {
#     #                         "id": i['matricula']
#     #                     },
#     #                     "saldoFgts": None,
#     #                     "fgtsMesAnterior": False,
#     #                     "periodos": []
#     #                 }
#     #             ],
#     #             "conversao": True,
#     #             "competencia": i['i_competencias'].strftime("%Y-%m")
#     #         }
#     #     }
#     # ])
#
#     # response = requests.request("POST", url, headers=headers, data=payload)
#     # response = response.json()
#     #
#     # print(f'----------Calculo da matricula {i["funcionario"]} na comp {i["i_competencias"]} e proc {tipoProc}----------')
#     #
#     # resultLotes = funcoes.lotes(response["id"])
#     # while resultLotes["situacao"] != "EXECUTADO":
#     #     resultLotes = funcoes.lotes(response["id"])
#     #     time.sleep(1)
#     #
#     # print(f'Situação inserção do calculo: {resultLotes["situacao"]}')
#     #
#     # if resultLotes["retorno"][0]["mensagem"] is not None:
#     #     print(payload)
#     #     print(f'Erro ou imprevisto no calculo: {resultLotes["retorno"]}')
#     #     exit(1)
#     #
#     # print(f'Id gerado calculo: {resultLotes["retorno"][0]["idGerado"]}, Lote: {response["id"]}')
#     url = "https://pessoal.betha.cloud/service-layer/v1/api/folha/"
#     eventos = i['eventosId'].split(',')
#     eventosVlrInf = i['vlr_inf'].split(',')
#     eventosVlrCalc = i['vlr_calc'].split(',')
#     eventosTipo = i['tipo_pd'].split(',')
#     eventosCompoeLiq = i['compoe_liq'].split(',')
#     eventosClass = i['eventosCla'].split(',')
#     bruto = 0.00
#     desconto = 0.00
#     liquido = 0.00
#     tipo = ''
#     jsonEventos = []
#     for j in range(len(eventos)):
#         if eventosTipo[j] == 'P' and eventosCompoeLiq[j] == 'S':
#             bruto += float(eventosVlrCalc[j])
#             tipo = 'VENCIMENTO'
#         elif eventosTipo[j] == 'D' and eventosCompoeLiq[j] == 'S':
#             desconto += float(eventosVlrCalc[j])
#             tipo = 'DESCONTO'
#         elif eventosTipo[j] == 'D' and eventosCompoeLiq[j] == 'N':
#             tipo = 'INFORMATIVO_MENOS'
#         elif eventosTipo[j] == 'P' and eventosCompoeLiq[j] == 'N':
#             tipo = 'INFORMATIVO_MAIS'
#
#         classi = 'NENHUMA'
#         if eventosClass[0] != '':
#             classi = eventosClass[j]
#
#         jsonEventos.append({
#             "configuracao": {
#                 "id": int(eventos[j])
#             },
#             "tipo": tipo,
#             "referencia": float(eventosVlrInf[j]),
#             "valor": float(eventosVlrCalc[j]),
#             "classificacaoEvento": classi,
#             "lancamentoVariavel": False,
#             "pagamentosFerias": [],
#             "rateioDependentes": []
#         })
#     liquido = bruto - desconto
#
#     enviar.append(
#         {
#             "idIntegracao": funcoes.encurtar('300','folha',i['matricula'],i['i_competencias'].strftime("%Y-%m"),tipoProc),
#             "conteudo": {
#                 "calculo": None,
#                 "tipoProcessamento": tipoProc,
#                 "subTipoProcessamento": "INTEGRAL",
#                 "matricula": {
#                     "id": i['matricula']
#                 },
#                 "competencia": i['i_competencias'].strftime("%Y-%m"),
#                 "folhaPagamento": True,
#                 "totalBruto": "{:.2f}".format(bruto),
#                 "totalDesconto": "{:.2f}".format(desconto),
#                 "totalLiquido": "{:.2f}".format(liquido),
#                 "dataFechamento": i['i_competencias'].strftime("%Y-%m-28"),
#                 "dataPagamento": i['i_competencias'].strftime("%Y-%m-28"),
#                 "dataLiberacao": None,
#                 "dataCalculo": i['i_competencias'].strftime("%Y-%m-28"),
#                 "situacao": "FECHADA",
#                 "eventos": jsonEventos
#             }
#         }
#     )
#     # print(payload)
#     # quit(15)
#     contador += 1
#     funcoes.executar(f"""INSERT INTO bethadba.controle_migracao_registro (sistema, tipo_registro, id_gerado,hash_chave_dsk, i_chave_dsk1,i_chave_dsk2,i_chave_dsk3)
#                                         VALUES (300,'folha',null,'{funcoes.encurtar('300','folha',i['matricula'],i['i_competencias'].strftime("%Y-%m"),tipoProc)}','{i['matricula']}','{i['i_competencias'].strftime("%Y-%m")}','{tipoProc}');""")
#     if contador % 100 == 0 or contador == len(resultado):
#         payload = json.dumps(enviar)
#         enviar = []
#         response = requests.request("POST", url, headers=headers, data=payload)
#         response = response.json()
#         ids.append(response['id'])
#         print(f"\r Folhas enviadas: {contador}/{len(resultado)}", end="")

print("\n")
ids =['61d78b0578fae3000ccbdb45']
print(ids)
print("\n")

contador = 0
for lote in ids:

    url2 = f'https://pessoal.cloud.betha.com.br/service-layer/v1/api/lote/lotes/{lote}'

    payload = {}

    response = requests.request("GET", url2, headers=headers, data=payload)
    response = response.json()


    for i in response['retorno']:
        contador+=1
        print(f"\rLotes executados: {contador}/{len(resultado)}", end="")
        if i['situacao'] != 'EXECUTADO':
            print("erro", i)
            continue
        funcoes.executar(f"""UPDATE bethadba.controle_migracao_registro set id_gerado ={i['idGerado']} where hash_chave_dsk = '{i['idIntegracao']}';""")
# folhas de 01/02/03/ abdon do tipo ferias integral com calculo de mensal integral
end = time.time()
print("tempo total:", "{:.2f}".format((end - start)/60), "min")
print("total enviado:", contador)
