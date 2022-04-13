import pandas as pd
import os, os.path


def kraken(fileinput, taxonomiclevel):
    # Leitura inicial de dados
    df_data = pd.read_csv(fileinput, header=None, low_memory=False, sep='\t')
    
    # ----------------------------------------------------------------------
    # Dataframe #1 - Porcentagens totais
    # ----------------------------------------------------------------------
    
    # Cabecalho para cada coluna para o output KRAKEN 1 E KRAKEN 2.

    # Info0 se refere a PORCENTAGEM
    # Info1 se refere ao numero de Reads correspondentes a taxonomia
    # Info2 se refere ao numero de Reads correspondentes DIRETAS a taxonomia
    # Info3 se refere ao filo, reino, etc...
    # Info4 se refere ao ID do NCBI
    # Info5 se refere ao nome cientifico.

    df_data.columns = ['Info0', 'Info1', 'Info2', 'Info3', 'Info4', 'Info5']
    df_data_reads = df_data[['Info5', 'Info1']].copy()
    df_data_reads = df_data_reads.rename(columns={'Info1': 'Info2', 'Info5': 'Info1'}, inplace=False)

    # Separa somente os correspondentes a filo, reino, etc...
    df_data2 = df_data.loc[df_data['Info3'] == taxonomiclevel.upper()]

    # Retira espacamento da output KRAKEN
    df_data2 = df_data2.replace(' ', '', regex=True)

    # Novo dataframe somente com dados de nome e numero de reads (Info1)
    output_df = df_data2[['Info5', 'Info0']].copy()

    # Substituição dos cabecalhos para melhor visualizacao no D3.JS
    # Segue a logica (Original:Saida_D3JS)

    output_df = output_df.rename(columns={'Info0': 'Info2', 'Info5': 'Info1'}, inplace=False)

    # Pega apenas os 10 com maior numero de reads.
    output_df_out = output_df.nlargest(10, 'Info2')

    # Transforma o dataframe para dicionário que será exportado como JSON para o D3JS
    dfd3 = output_df_out.to_dict('r')

    # -----------------------------------------------------------------
    # Retira maior porcentagem para ser parametro de tamanho do gráfico
    maxpercent = output_df_out['Info2'].iloc[0]
    # -----------------------------------------------------------------
    
    # -----------------------------------------------------------------
    # Dataframe #2 - READS Individuais
    # -----------------------------------------------------------------
    # Novo dataframe somente com dados de nome e numero de reads (Info1)
    output_df_2 = df_data2[['Info5', 'Info1']].copy()
    
    # Sorting de valores do maior para o menor e faz copia
    output_df_2 = output_df_2.sort_values(['Info1'], ascending=[False])
    output_df_2_somar = output_df_2.copy()
    
    # Cria novo dataframe com os 10 primeiros
    output_df_2 = output_df_2.nlargest(10, columns=['Info1'])
    
    # Cria um dataframe sem os 10 primeiros
    output_df_2_somar = output_df_2_somar.iloc[10:]
    
    # Pega todas as reads das linhas que estão abaixo
    total = output_df_2_somar['Info1'].sum()

    # Pega o numero de reads total 
    total_reads = df_data_reads['Info2'].sum()

    # Cria uma linha nova para adicionar os outros
    others_col = {'Info5':'Others', 'Info1':total}

    # Adiciona a nova linha no dataframe
    output_df_2 = output_df_2.append(others_col, ignore_index=True)

    # Renomeando as colunas para o modelo exemplo do D3.js
    # Quando possivel corrigir os nomes das variaveis no D3.JS para dar melhor clareza ao código
    output_df_2 = output_df_2.rename(columns={'Info1': 'Sample', 'Info5': 'State'}, inplace=False)
    # -----------------------------------------------------------------
  
    # -----------------------------------------------------------------
    # Retira maior porcentagem para ser parametro de tamanho do gráfico
    maxreads = output_df_2['Sample'].iloc[0]
    # -----------------------------------------------------------------
    
    # Faz gira o dataframe e cria um dataframe com coluna e linhas trocadas para a entrada no D3.js
    output_df_2 = output_df_2.transpose()
    # Transforma a index para coluna
    output_df_2.columns = output_df_2.iloc[0]
    # Retira coluna de index bugada
    output_df_2 = output_df_2.iloc[1:]
    # Define uma nova index e faz o resto (melhorar documentação)
    output_df_2['State'] = output_df_2.index
    output_df_2 = output_df_2.iloc[:, ::-1]

    # Nesse ponto o código vai salvar um CSV para exportar para o D3JS
    # Pelo D3.js v3 ter uma sintaxe diferente do D3.v4+
    
    # Conta arquivos para segurança

    DIR = './static/csv'
    filecount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    
    # Salva os arquivos para csv
    output_df_2.to_csv(rf'./static/csv/SaidaOutput{filecount}.csv', index=False, header=True)
    # Pega o nome do arquivo para mandar pro d3js
    dfd3_2 = f'/static/csv/SaidaOutput{filecount}.csv'

    return dfd3, dfd3_2, maxpercent, maxreads, total_reads

def clark(fileinput):
    # Leitura inicial de dados
    df_data = pd.read_csv(fileinput, low_memory=False, sep=',')

    # Adiciona cabecalho para cada coluna para o output Clark.

    # Info0 se refere ao Nome
    # Info1 se refere ao TaxID
    # Info2 se refere a linhagem
    # Info3 se refere ao numero de reads correspondentes a taxonomia
    # Info4 se refere a proporção em % sobre o numero de sequencias totais.
    # Info5 se refere a proporção de % em sequencias classificadas

    df_data.columns = ['Info0', 'Info1', 'Info2', 'Info3', 'Info4', 'Info5']
    # ----------------------------------------------------------------------
    # Dataframe #1 - Porcentagens
    # ----------------------------------------------------------------------
    # Novo dataframe somente com dados de nome e numero de reads (Info1)
    output_df = df_data[['Info0', 'Info5']].copy()

    # Substituição dos cabecalhos para melhor visualizacao no D3.JS
    # Segue a logica (Original:Saida_D3JS)
    output_df = output_df.rename(columns={'Info5': 'Info2', 'Info0': 'Info1'}, inplace=False)

    # Se deleta uma linha do final do arquivo do CLARK
    output_df = output_df[:-1]
    
    # É necessária a conversão de uma tabela pra numérica
    output_df["Info2"] = output_df["Info2"].apply(pd.to_numeric)

    # Pega apenas os 10 com maior numero de porcentagem.
    output_df_out = output_df.nlargest(10, 'Info2')
    
    # Retira maior porcentagem para ser parametro de tamanho do gráfico
    maxpercent = output_df_out['Info2'].iloc[0]
    
    # Transforma o dataframe para dicionário que será exportado como JSON para o D3JS
    dfd3 = output_df_out.to_dict('r')

    # -----------------------------------------------------------------
    # Dataframe #2 - READS Individuais
    # -----------------------------------------------------------------
    # Novo dataframe somente com dados de nome e numero de reads (Info1)
    output_df_2 = df_data[['Info0', 'Info3']].copy()
    
    # Sorting de valores do maior para o menor e faz copia
    output_df_2 = output_df_2.sort_values(['Info3'], ascending=[False])
    output_df_2_somar = output_df_2.copy()
    
    # Cria novo dataframe com os 10 primeiros
    output_df_2 = output_df_2.nlargest(10, columns=['Info3'])
    
    # Cria um dataframe sem os 10 primeiros
    output_df_2_somar = output_df_2_somar.iloc[10:]
    
    # Pega todas as reads das linhas que estão abaixo
    total = output_df_2_somar['Info3'].sum()

    # Soma o total de reads no arquivo
    total_reads = output_df_2['Info3'].sum()

    # Cria uma linha nova para adicionar os outros
    others_col = {'Info0':'Others', 'Info3':total}

    # Adiciona a nova linha no dataframe
    output_df_2 = output_df_2.append(others_col, ignore_index=True)

    # Renomeando as colunas para o modelo exemplo do D3.js
    # Quando possivel corrigir os nomes das variaveis no D3.JS para dar melhor clareza ao código
    output_df_2 = output_df_2.rename(columns={'Info3': 'Sample', 'Info0': 'State'}, inplace=False)
    # -----------------------------------------------------------------
  
    # -----------------------------------------------------------------
    # Retira maior porcentagem para ser parametro de tamanho do gráfico
    maxreads = output_df_2['Sample'].iloc[0]
    # -----------------------------------------------------------------
    
    # Faz gira o dataframe e cria um dataframe com coluna e linhas trocadas para a entrada no D3.js
    output_df_2 = output_df_2.transpose()
    # Transforma a index para coluna
    output_df_2.columns = output_df_2.iloc[0]
    # Retira coluna de index bugada
    output_df_2 = output_df_2.iloc[1:]
    # Define uma nova index e faz o resto (melhorar documentação)
    output_df_2['State'] = output_df_2.index
    output_df_2 = output_df_2.iloc[:, ::-1]

    # Nesse ponto o código vai salvar um CSV para exportar para o D3JS
    # Pelo D3.js v3 ter uma sintaxe diferente do D3.v4+
    
    # Conta arquivos para segurança

    DIR = './static/csv'
    filecount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    
    # Salva os arquivos para csv
    output_df_2.to_csv(rf'./static/csv/SaidaOutput{filecount}.csv', index=False, header=True)
    # Pega o nome do arquivo para mandar pro d3js
    dfd3_2 = f'/static/csv/SaidaOutput{filecount}.csv'
    
    return dfd3, dfd3_2, maxpercent, maxreads, total_reads


# DESCONSIDERAR METAMAPS, É NECESSÁRIO ATUALIZAR.
def metamaps(fileinput, taxonomiclevel):
    # Leitura inicial de dados
    df_data = pd.read_csv(fileinput, header=None, low_memory=False, sep='\t')

    # Adiciona cabecalho para cada coluna para o output Metamaps.

    # Info0 se refere ao Nome
    # Info1 se refere ao TaxID
    # Info2 se refere ao filo, reino, etc...
    # Info3 se refere ao tamanho do genoma
    # Info4 se refere ao numero de reads correspondentes a taxonomia
    # Info5 se refere ao numero de reads correspondentes DIRETAS a taxonomia
    # Info6 Abundancia

    df_data.columns = ['Info0', 'Info1', 'Info2', 'Info3', 'Info4', 'Info5', 'Info6']

    # Separa somente os correspondentes a filo, reino, etc...
    df_data2 = df_data.loc[df_data['Info2'] == taxonomiclevel.lower()]

    # Novo dataframe somente com dados de nome e numero de reads (Info1)
    output_df = df_data2[['Info0', 'Info4']].copy()

    # Substituição dos cabecalhos para melhor visualizacao no D3.JS
    output_df = output_df.rename(columns={'Info4': 'Info2', 'Info0': 'Info1'}, inplace=False)

    # Descomentar codigo para girar o dataframe caso for necessario em outra formatacao de visualizacao
    # output_df = output_df.transpose()

    # Pega apenas os 10 com maior numero de porcentagem. (Esse comando precisa ser adaptado ao metamaps)
    # output_df_out = output_df.nlargest(30, 'Sample')

    # Caso a output seja girada, substituir Index por true e header por false
    print(output_df)
    dfd3 = output_df.to_dict('r')
    
    return dfd3