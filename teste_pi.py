import xlwings as xw
import pandas as pd
import requests
import json
from flask import Flask, jsonify, request
#################### Leitura do cronograma de manutenção de tabela do Excel para Dataframe ####################

def ExecutarSimulacaoFid(qryidf, qryap):
    try:
        idCAno = 'Ano'
        idCUg = 'UG'
        idCAtividade = 'Atividade'
        idCDataInicio = 'Data Início'
        idCHoraInicio = 'Hora Início'        
        idCDataFim = 'Data Fim'
        idCHoraFim = 'Hora Fim'
        ifCDuracao = 'Duração'
        ifCForcada = '%Forçada'
        
        if qryidf == "": # rotina sem parametros executado local
            from requests_negotiate_sspi import HttpNegotiateAuth
            wb = xw.Book(__file__.replace('dependenciasXlsC2\Script_SimulaçãoFID_Excel2.py', 'São Manoel_ONS_Simulador.xlsm'))
            sheet = wb.sheets['Calendário de Manutenção']
                
            df = sheet.range('CalendárioManutenção_C2').options(pd.DataFrame, 
                                                        header=0,
                                                        index=False, 
                                                        expand='table',
                                                        ).value

            df.columns = [idCAno, idCUg, idCAtividade, idCDataInicio, idCHoraInicio, idCDataFim, idCHoraFim, ifCDuracao]
            df_forçada = sheet.range('PorcentagemForçadaAno_C1').options(pd.DataFrame, 
                                                        header=0,
                                                        index=False, 
                                                        expand='table',
                                                        ).value

            df_forçada.columns = [idCAno, ifCForcada]
            
            def conversão_data(decimal):
                horas = decimal * 24
                minutos = 60 * (horas % 1)
                data = "%d:%02d" % (horas, minutos)
                return data        

            df[idCHoraInicio] = df[idCHoraInicio].apply(conversão_data)
            df[idCHoraFim] = df[idCHoraFim].apply(conversão_data)

            df[idCDataInicio] = df[idCDataInicio].dt.strftime('%d/%m/%Y')
            df[idCDataFim] = df[idCDataFim].dt.strftime('%d/%m/%Y')
            df[idCAno] = df[idCAno].astype(int)
            
            df_forçada[idCAno] = df_forçada[idCAno].astype(int)        

        else:
            # rotina automatica
            from funcoesgerais.Funcoespi import call_security_method
            idCAno = 'ano'
            idCUg = 'unidade'
            idCAtividade = 'atividades'
            idCDataInicio = 'data_inicio'
            idCHoraInicio = 'hora_inicio'        
            idCDataFim = 'data_fim'
            idCHoraFim = 'hora_fim'
            ifCDuracao = 'duracao'
            ifCForcada = 'per_Ind_forcado'    
            df = pd.read_json(qryap)
            df_forçada = pd.read_json(qryidf)
            
        #################### Leitura do cronograma de manutenção de tabela do Excel para Dataframe ####################

        ##########################################

        #Criação da tabela de horas de referência por UG
        lista_tipos_hora = ['HES', 'HERD', 'HDCE', 'HDF', 'HEDF', 'HDP', 'HEDP']
        lista_fim_ref = ['30-11-2017', '31-12-2017', '28-02-2018', '31-03-2018']    
        lista_df_ref_final_ugs = []
        for ug in range(1,5):
            lista_ug = []
            for tipo_hora in lista_tipos_hora:
                lista_ug.append(f'{tipo_hora}_TempoDiario_UG0{ug}')
                df_ug = pd.DataFrame(lista_ug, columns=[idCUg])
                df_datas_ref_ug = pd.DataFrame(pd.date_range('01-01-2013', lista_fim_ref[ug-1], freq = '1D', ), columns=['Data'])
                df_ref_final = df_ug.merge(df_datas_ref_ug, how='cross')
            lista_df_ref_final_ugs.append(df_ref_final)

        df_ref_final_ugs = pd.concat(lista_df_ref_final_ugs)

        #Preenchimento dos valores de referência por UG
        df_ref_final_ugs['Valor'] = 0

        TEIP_ref = 0.0614100
        TEIFa_ref = 0.0163231

        #Horas de referência HDP
        mask_HDP = df_ref_final_ugs[idCUg].str.contains('HDP')
        df_ref_final_ugs['Valor'] = df_ref_final_ugs['Valor'].where(~mask_HDP, 24*TEIP_ref)
        HDP_ref = df_ref_final_ugs[mask_HDP]['Valor'].min()

        #Horas de referência HDF
        mask_HDF = df_ref_final_ugs[idCUg].str.contains('HDF')
        df_ref_final_ugs['Valor'] = df_ref_final_ugs['Valor'].where(~mask_HDF, (24 - HDP_ref)*TEIFa_ref)
        HDF_ref = df_ref_final_ugs[mask_HDF]['Valor'].min()

        #Horas de referência HES
        mask_HES = df_ref_final_ugs[idCUg].str.contains('HES')
        df_ref_final_ugs['Valor'] = df_ref_final_ugs['Valor'].where(~mask_HES, 24-HDP_ref-HDF_ref)


        #Preenchimento dos valores de referência para a usina
        # df_ref_final_ugs[idCUg] = df_ref_final_ugs[idCUg].apply(lambda x: '_'.join(x.split('_')[0:2]))

        ano = df_ref_final_ugs['Data'].dt.year
        mes = df_ref_final_ugs['Data'].dt.month

        df_ref_final = df_ref_final_ugs.groupby([idCUg, ano, mes])[['Valor']].sum()
        df_ref_final.index.names = [idCUg, idCAno, 'Mês']

        df_ref_final = df_ref_final.pivot_table(values='Valor', index=[idCAno, 'Mês'], columns=idCUg).reset_index()

        ##########################################

        ####Consulta aos webids dos atributos da lista de tipos de hora
        lista_tipos_hora = ['HES', 'HERD', 'HDCE', 'HDF', 'HEDF', 'HDP', 'HEDP']
     
        dict_batch_tipos_hora = {}
        for tipo_hora in lista_tipos_hora:
            for ug in range(1,5):
                dict_batch_tipos_hora[f'{tipo_hora}_TempoDiario_UG0{ug}'] = \
                {
                "Method": "GET",
                "Resource": rf"https://piwebapi.edpbr.com.br/piwebapi/points?path=\\edpbr340\USMA_UG0{ug}_IndDesemp_{tipo_hora}TempoDiario&selectedFields=WebId"
                }
        
        session = requests.session()
           
        headers = {'X-Requested-With': 'XmlHttpRequest'}
        if qryap=="":
          r = session.post('https://piwebapi.edpbr.com.br/piwebapi/batch', json=dict_batch_tipos_hora, headers=headers, auth=HttpNegotiateAuth())                     
        else:
          r = session.post('https://piwebapi.edpbr.com.br/piwebapi/batch', json=dict_batch_tipos_hora, headers=headers, auth=call_security_method('basic', 'PIVISION_SVC', '0#CogES01'))               

        dict_webids = json.loads(r.text)
        
        dict_webids_formatado = {}
       
        # return str(dict_webids)
        for key in dict_webids:
            dict_webids_formatado[key] = dict_webids[key]['Content']['WebId']
           
        #Ordenar as chaves
        dict_webids_formatado = dict(sorted(dict_webids_formatado.items()))
        
        ####Consulta aos webids dos atributos da lista de tipos de hora

        
        #Data de início da janela histórica
        #data = pd.to_datetime(pd.to_datetime('now') - pd.DateOffset(months=60)) 
        #data_dia_1 = data.replace(day=1).strftime('%d/%m/%Y')
        data_inicio_periodo = '01-01-2017' #str(data_dia_1).replace('/','-')

        data_fim_periodo = '*+1mo'  #Para aparecer o mês corrente: '*+1mo' | Para aparecer o mês atual: '*'

        session = requests.session()

        headers = {'X-Requested-With': 'XmlHttpRequest'}
        
        batch_request = {}
        for tag, webid in dict_webids_formatado.items():
            batch_request[tag] = \
                {
            "Method": "GET",
            "Resource": rf"https://piwebapi.edpbr.com.br/piwebapi/streams/{webid}/summary?startTime={data_inicio_periodo}&endTime={data_fim_periodo}&summaryType=Total&summaryDuration=1mo&CalculationBasis=EventWeighted&timezone=UTC"
                }
        
        if qryap=="":
          r = session.post('https://piwebapi.edpbr.com.br/piwebapi/batch', json=batch_request, headers=headers, auth=HttpNegotiateAuth())
        else:
          r = session.post('https://piwebapi.edpbr.com.br/piwebapi/batch', json=batch_request, headers=headers, auth=call_security_method('basic', 'PIVISION_SVC', '0#CogES01'))
          
        
        dicionario = json.loads(r.text)
        
        lista_total = []
        
        indice = 0
        while True:
            try:
                for tipo_hora in dicionario.keys():
                    timestamp = dicionario[tipo_hora]['Content']['Items'][indice]['Value']['Timestamp']
                    valor = dicionario[tipo_hora]['Content']['Items'][indice]['Value']['Value']
                    lista_total.append((tipo_hora, timestamp, valor))

                indice = indice + 1
                
            except:
                break    
        
        df_longo = pd.DataFrame(lista_total, columns=['Tipo de Hora', 'Timestamp', 'Valor'])
        
        df_longo = df_longo.set_index('Timestamp').pivot(columns='Tipo de Hora',values='Valor').div(60*60).reset_index()

        df_longo['Timestamp'] = pd.to_datetime(df_longo['Timestamp']) + pd.DateOffset(months=1) 

        df_longo['Timestamp'] = df_longo['Timestamp'].dt.tz_localize(None) - pd.offsets.Hour(3)
        
        #Remoção dos sufixos _UG para agrupamento dos tempos para a usina
        
        df_usina = df_longo.melt(id_vars='Timestamp')
        
        df_usina = df_usina.pivot_table(index='Timestamp', columns='Tipo de Hora', values='value', aggfunc='sum')

        df_usina = df_usina.reset_index()

        df_usina.insert(0, idCAno, df_usina['Timestamp'].dt.year)

        df_usina.insert(1, 'Mês', df_usina['Timestamp'].dt.month)

        df_usina.drop(['Timestamp'], axis='columns', inplace=True)
        
        ##########################################
        
        ################################ Início Calendário de manutenção ################################ 
        
        df['DataTempo Início'] = pd.to_datetime(df[idCDataInicio] + ' ' + df[idCHoraInicio], dayfirst = True)
        
        df['DataTempo Fim'] = pd.to_datetime(df[idCDataFim] + ' ' + df[idCHoraFim], dayfirst = True)
        
        df = df[[idCUg, idCAtividade, 'DataTempo Início', 'DataTempo Fim']]

        df_melt = df.melt(id_vars=[idCAtividade, idCUg], var_name='Tipo Data', value_name='Data', ignore_index=False).sort_index()
        
        def df_incluir_dias(grupo):
            data_inicio_grupo = grupo['Data'].min().normalize()
            data_fim_grupo = (grupo['Data'].max() + pd.DateOffset(days=1)).normalize()
            data_range_grupo = pd.date_range(data_inicio_grupo, data_fim_grupo, freq = '1D')
            dias_periodo_grupo = pd.DataFrame(data_range_grupo, columns=['Data'])
            df_dias_incluidos_grupo = pd.concat([grupo, dias_periodo_grupo], sort=False).sort_values(['Data'])
            return df_dias_incluidos_grupo

        df_melt_dias_incluidos = df_melt.groupby(df_melt.index).apply(lambda grupo: df_incluir_dias(grupo)).fillna(method='ffill')
       
        df_melt_dias_incluidos[ifCDuracao] = (df_melt_dias_incluidos['Data'].shift(-1) - df_melt_dias_incluidos['Data']).dt.total_seconds()/3600

        #Inclusão do HDP
        df_melt_dias_incluidos_HDP = df_melt_dias_incluidos[df_melt_dias_incluidos['Tipo Data'] == 'DataTempo Início'].reset_index()
        df_melt_dias_incluidos_HDP.drop(['level_0', 'level_1'], axis='columns', inplace=True)

        df_HDP = (df_melt_dias_incluidos_HDP
            .groupby(
                    [
                        df_melt_dias_incluidos_HDP[idCUg],
                        df_melt_dias_incluidos_HDP['Data'].dt.year,
                        df_melt_dias_incluidos_HDP['Data'].dt.month,
                        df_melt_dias_incluidos_HDP['Data'].dt.day,
                    ]
                    )[[ifCDuracao]].sum()
        )
        
        df_HDP.index.names = [idCUg, idCAno, 'Mês', 'Dia']
        df_HDP.columns = ['HDP_TempoDiario']
        df_HDP = df_HDP.reset_index()

        df_HDP = df_HDP.melt(id_vars=[idCUg, idCAno, 'Mês', 'Dia'], var_name='Tipo Hora', value_name='Valor HDP', ignore_index=False).sort_index()

        df_HDP['Tipo Hora'] = df_HDP['Tipo Hora'] + '_' + df_HDP[idCUg]

        df_HDP = df_HDP.fillna(0)

        ################################# Fim Calendário de manutenção ################################ 

        ############################### Início Indisponibilidade Forçada ############################## 


        ################################ Fim Indisponibilidade Forçada ################################ 

        numero_UGs = 4
        df_UGs = pd.DataFrame(['UG0'+str(i) for i in range(1,numero_UGs+1)], columns=[idCUg])

        df_dias_futuros = pd.DataFrame(pd.date_range('today', '2051-01-01', freq = '1D').normalize(), columns=['Data'])

        df_dias_futuros[idCAno] = df_dias_futuros['Data'].dt.year
        df_dias_futuros['Mês'] = df_dias_futuros['Data'].dt.month
        df_dias_futuros['Dia'] = df_dias_futuros['Data'].dt.day

        df_dias_futuros.drop('Data', axis='columns', inplace=True)

        df_dias_futuros_UGs = df_UGs.merge(df_dias_futuros, how='cross')

        df_dias_futuros_UGs = df_dias_futuros_UGs.merge(df_forçada, how='inner')

        df_dias_futuros_UGs = df_dias_futuros_UGs.merge(df_HDP, how='left')

        df_dias_futuros_UGs = df_dias_futuros_UGs.fillna({'Tipo Hora': 'HDP_TempoDiario_' + df_dias_futuros_UGs[idCUg]}).fillna(0)

        df_dias_futuros_UGs['Valor HDF'] = (24 - df_dias_futuros_UGs['Valor HDP'])*df_dias_futuros_UGs[ifCForcada]

        df_dias_futuros_UGs['Tipo Hora_HDF'] = df_dias_futuros_UGs['Tipo Hora'].str.replace('HDP', 'HDF')

        df_dias_futuros_UGs['Valor HES'] = 24 - df_dias_futuros_UGs['Valor HDP'] - df_dias_futuros_UGs['Valor HDF']

        df_dias_futuros_UGs['Tipo Hora_HES'] = df_dias_futuros_UGs['Tipo Hora'].str.replace('HDP', 'HES')

        df_dias_futuros_UGs = df_dias_futuros_UGs.groupby([idCAno, 'Mês', 'Tipo Hora', 'Tipo Hora_HDF', 'Tipo Hora_HES']).agg(
                                                        Hora     = ('Valor HDP','sum'),
                                                        Hora_HDF = ('Valor HDF','sum'),
                                                        Hora_HES = ('Valor HES','sum'),
                                                        ).reset_index()

        df_1 = df_dias_futuros_UGs[[idCAno, 'Mês', 'Tipo Hora', 'Hora']]

        df_2 = df_dias_futuros_UGs[[idCAno, 'Mês', 'Tipo Hora_HDF', 'Hora_HDF']]
        df_2.columns = [idCAno, 'Mês', 'Tipo Hora', 'Hora']

        df_3 = df_dias_futuros_UGs[[idCAno, 'Mês', 'Tipo Hora_HES', 'Hora_HES']]
        df_3.columns = [idCAno, 'Mês', 'Tipo Hora', 'Hora']

        df_dias_futuros_UGs = pd.concat([df_1, df_2, df_3])

        df_dias_futuros_UGs = df_dias_futuros_UGs.pivot(index=[idCAno,'Mês'], columns='Tipo Hora', values='Hora').reset_index()
        
        ##########################################
        
        numero_UGs = 4
        ID_Ref = 0.9232158958

        df_ref = df_ref_final
        df_realizado = df_usina
        df_futuro = df_dias_futuros_UGs


        df_ref.set_index([idCAno,'Mês'], inplace=True)
        df_realizado.set_index([idCAno,'Mês'], inplace=True)
        df_futuro.set_index([idCAno,'Mês'], inplace=True)

        df_usina = df_ref.add(df_realizado, fill_value=0)
        df_usina = df_usina.add(df_futuro, fill_value=0).reset_index()

        df_usina = df_usina.fillna(0)

        #Cálculo do FID por UG e para a Usina
        lista_horas = ['HES','HERD','HDCE','HDF','HEDF','HDP','HEDP']
        lista_horas_indisp = lista_horas[3:]

        UGs = ['UG0'+str(i) for i in range(1,numero_UGs+1)]  #['UG01', 'UG02', ...]

        tipos_horas_indisp_usina = []
        tipos_horas_usina = []

        for UG in UGs:
            #Para as UGs
            tipos_horas_indisp = [f'{hora}_TempoDiario_{unidade}' for hora, unidade in list(zip(lista_horas_indisp, [UG] * numero_UGs))]
            #Para a Usina
            tipos_horas_indisp_usina.extend(tipos_horas_indisp)

            #Para as UGs
            tipos_horas = [f'{hora}_TempoDiario_{unidade}' for hora, unidade in list(zip(lista_horas, [UG] * len(lista_horas)))]
            #Para a Usina
            tipos_horas_usina.extend(tipos_horas)

            #Criação de variável dinamicamente
            #https://stackoverflow.com/a/6181959
            df_usina[f'ID60meses_{UG}'] = (1 - 
                        df_usina[tipos_horas_indisp].sum(axis='columns').rolling(60).sum()
                        /
                        df_usina[tipos_horas].sum(axis='columns').rolling(60).sum()
                        )/ID_Ref 
            
        df_usina['ID60meses_Usina'] = (1 - 
                        df_usina[tipos_horas_indisp_usina].sum(axis='columns').rolling(60).sum()
                        /
                        df_usina[tipos_horas_usina].sum(axis='columns').rolling(60).sum()
                        )/ID_Ref 
    
        #Dataframe com o ID60meses das UGs e da Usina
        df_FID = df_usina[df_usina.columns[0:2].append(df_usina.columns[-5:])]

        df_FID = df_FID.rename(columns={'Mês':'Mes'})
        
        data = pd.to_datetime(dict(year=df_FID[idCAno], month=df_FID['Mes'], day=1))
        df_FID['Timestamp'] = (data + pd.DateOffset(months=1) - pd.DateOffset(days=1)).dt.strftime('%d/%m/%Y %H:%M')
        df_final = df_FID[df_FID[idCAno] >= 2022].loc[:,'ID60meses_Usina']
        tempo_agora = pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')

        if qryidf == "":
            df_FID.to_json(__file__.replace('Script_SimulaçãoFID_Excel2.py',rf'{tempo_agora}_FID_C2.json'), indent=2, orient='records', double_precision=5)
            df_FID.to_csv(__file__.replace('Script_SimulaçãoFID_Excel2.py',rf'{tempo_agora}_FID_C2.csv'), sep=';', decimal=',', encoding='ansi', index=False)
            sheet.range('FID_C2').offset(-1).options(index=False).value = df_final        
        else:
           return df_FID.to_json() 
       
    except Exception as err:
        return str(err)

#if __name__ == "__main__":
 #   ExecutarSimulacaoFid('1', '2')