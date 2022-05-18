import requests
import json
from configuracao.conexao import AUTORIZACAO
import funcoes

consulta = funcoes.consultar("""
select 300 as sistema, 
                 'averbacao-matricula' as tipo_registro,
                 id = bethadba.dbf_get_id_gerado(sistema , tipo_registro,  chave_dsk1, chave_dsk2),
                 chave_dsk1 = funcionarios.i_entidades, 
                 chave_dsk2 = funcionarios.i_funcionarios, 
                 matricula = bethadba.dbf_get_id_gerado(sistema , 'matricula',  chave_dsk1, chave_dsk2),
                 periodoInicial = funcionarios.dt_admissao,
                 periodoFinal = if funcionarios.tipo_func = 'A' then
                                   (select top 1 if trab_dia_resc = 'N' then 
                                              date(days(dfinaux,-1)) 
                                           else 
                                              dfinaux 
                                           endif 
                                      from bethadba.rescisoes_autonomo 
                                     where rescisoes_autonomo.i_entidades = funcionarios.i_entidades and 
                                           rescisoes_autonomo.i_funcionarios = funcionarios.i_funcionarios and 
                                           rescisoes_autonomo.dt_rescisao = (select max(r.dt_rescisao) 
                                                                               from bethadba.rescisoes_autonomo r 
                                                                              where r.i_entidades = rescisoes_autonomo.i_entidades and 
                                                                                    r.i_funcionarios = rescisoes_autonomo.i_funcionarios ))
                                else
                                   (select top 1 if trab_dia_resc = 'N' then 
                                              date(days(dfinaux,-1)) 
                                           else 
                                              dfinaux 
                                           endif 
                                      from bethadba.rescisoes 
                                     where rescisoes.i_entidades = funcionarios.i_entidades and 
                                           rescisoes.i_funcionarios = funcionarios.i_funcionarios and 
                                           rescisoes.dt_rescisao = (select max(r.dt_rescisao) 
                                                                      from bethadba.rescisoes r , 
                                                                           bethadba.motivos_resc mr
                                                                     where r.i_motivos_resc = mr.i_motivos_resc and 
                                                                           r.i_entidades = rescisoes.i_entidades and 
                                                                           r.i_funcionarios = rescisoes.i_funcionarios and 
                                                                           r.dt_canc_resc is null and
                                                                           (mr.dispensados <> 4 or r.i_rescisoes = 1)))
                                  endif,
       descricao = null,
       justificativa = null,
       tipoAverbacao = 'MATRICULA',
       ato = null,
       /*Para conversão, utilizar os campos até aqui*/
       dfinaux   = if bethadba.dbf_getulttipoafast(funcionarios.i_entidades,funcionarios.i_funcionarios,'S') = 8 then 
                      if funcionarios.tipo_func = 'A' then
                         (select max(dt_rescisao) 
                            from bethadba.rescisoes_autonomo 
                           where rescisoes_autonomo.i_entidades = funcionarios.i_entidades and 
                                 rescisoes_autonomo.i_funcionarios = funcionarios.i_funcionarios)
                      else
                        (select max(dt_rescisao) 
                           from bethadba.rescisoes 
                            where rescisoes.i_entidades = funcionarios.i_entidades and 
                                  rescisoes.i_funcionarios = funcionarios.i_funcionarios and 
                                  rescisoes.dt_rescisao = (select max(r.dt_rescisao) 
                                                                      from bethadba.rescisoes r , 
                                                                           bethadba.motivos_resc mr
                                                                     where r.i_motivos_resc = mr.i_motivos_resc and 
                                                                           r.i_entidades = rescisoes.i_entidades and 
                                                                           r.i_funcionarios = rescisoes.i_funcionarios and 
                                                                           r.dt_canc_resc is null and
                                                                           (mr.dispensados <> 4 or r.i_rescisoes = 1))) 
                      endif
                    else 
                        null 
                    endif, 
       totdias   = days(funcionarios.dt_admissao,ifnull(periodoFinal,(if today() > funcionarios.dt_admissao then today() else null endif),periodoFinal)) + 1
       ,
       (select list(tab.contagemTempo)
                          from (
                        select contagemTempo = 'ADICIONAL',
                               entidade = ff.i_entidades, 
                               funcionario = ff.i_funcionarios
                          from bethadba.funcionarios as ff
                         where ff.conta_adicional = 'S' or
                               (exists (select 1 
                                          from bethadba.adic_funcs
                                         where adic_funcs.i_funcionarios = ff.i_funcionarios
                                           and adic_funcs.i_entidades = ff.i_entidades
                                           and adic_funcs.proc_averbacoes = 'S') 
                                   and bethadba.dbf_gettipoafast(1 ,ff.i_entidades,ff.i_funcionarios, date('2999-12-31') ) <> 8)
                        union all 
                        select contagemTempo = 'TEMPO_DE_SERVICO',
                               entidade = ff.i_entidades, 
                               funcionario = ff.i_funcionarios
                          from bethadba.funcionarios as ff
                         where ff.conta_temposerv = 'S'
                        union all 
                        select contagemTempo = 'LICENCA_PREMIO',
                               entidade = ff.i_entidades, 
                               funcionario = ff.i_funcionarios
                          from bethadba.funcionarios as ff
                         where ff.conta_licpremio = 'S'
                        union all 
                        select contagemTempo = 'TEMPO_DE_CARREIRA',
                               entidade = ff.i_entidades, 
                               funcionario = ff.i_funcionarios
                          from bethadba.funcionarios as ff
                         where ff.conta_tempocarreira = 'S') as tab
                         where tab.entidade = funcionarios.i_entidades and tab.funcionario = funcionarios.i_funcionarios) as contagemTempo
   FROM bethadba.funcionarios, 
        bethadba.hist_cargos
  WHERE funcionarios.tipo_func = 'F' and 
        hist_cargos.i_entidades = funcionarios.i_entidades AND
        hist_cargos.i_funcionarios = funcionarios.i_funcionarios AND
        hist_cargos.dt_alteracoes = bethadba.dbf_getdatahiscar(funcionarios.i_entidades,funcionarios.i_funcionarios,datetime('2999-12-31 23:59:59')) and 
        NOT EXISTS(SELECT top 1 1 FROM bethadba.estagios 
                    WHERE estagios.i_entidades = funcionarios.i_entidades AND 
                          estagios.i_funcionarios = funcionarios.i_funcionarios) AND
        not (funcionarios.tipo_func = 'A' and funcionarios.conselheiro_tutelar = 'N') and 
        (funcionarios.conta_adicional = 'S' or funcionarios.conta_licpremio = 'S' or 
         funcionarios.conta_temposerv = 'S' or funcionarios.conta_tempocarreira = 'S')              
and (  bethadba.dbf_get_situacao_registro(sistema, tipo_registro, chave_dsk1, chave_dsk2) in (5,3)) and matricula is not null
""")
payload=[]
contador = 0
contador2 = 0
tamanho = len(consulta)
print(tamanho)
for i in consulta:
    final = None
    if 'periodoFinal' in i and i['periodoFinal'] is not None:
        final = i['periodoFinal'].strftime("%Y-%m-%d")
    payload.append(
        {
            "idIntegracao": "sla",
            "conteudo": {
                "ato": None,
                "descricao": None,
                "justificativa": None,
                "periodoInicial": i['periodoInicial'].strftime("%Y-%m-%d"),
                "periodoFinal": final,
                "tipoAverbacao": "MATRICULA",
                "matricula": {
                    "id": i['matricula']
                },
                "tipoMovimentacaoAdicional": None,
                "contagemTempo": i['contagemTempo'].split(',')
            }
        }
    )


    contador += 1
    if contador % 100 == 0 or contador == tamanho:
        url = f"https://pessoal.cloud.betha.com.br/service-layer/v1/api/averbacao-matricula/"
        headers = {
            'Authorization': AUTORIZACAO,
            'content-type': 'application/json'
        }
        payload = json.dumps(payload)
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        payload = []
        contador2 += 1
        print("lote:", contador2,response.json())
print("total registros:", contador)
