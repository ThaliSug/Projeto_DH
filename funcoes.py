import pandas as pd
import requests
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')


#--------------------------------------------------------------------------
## Coleta e tratamento dos dados

# Coleta

def coleta_dados_estacao(tipo = 'T', cod=None):
    '''
    Usando o site https://mapas.inmet.gov.br/#  para pesquisar as estações do INMET, sendo:
    ex: 
    
    prâmetros para a função:
    tipo:
    T - Automáticas
    M - Manuais
    ex: default--> tipo ='T'
    e código da estação.
    
    ex: [A701] SAO PAULO - MIRANTE - SP
        cod='A701'
    
    a função **retorna** um dataset com informações da estação, sendo:
    Nome, o código da estação, Latitude, Longitude, situação que se encontra (pane ou operante) 
    e Data de início de operação
    '''
    import pandas as pd
    import requests
    import json
    
    #Para pegar dados das estações automáticas ou manuais:
    url=requests.get(f'https://apitempo.inmet.gov.br/estacoes/{tipo}').json()
    
    #Transforma em DataFrame com todas as estações:
    df=pd.read_json(json.dumps(url))
    
    #Faz um query para selecionar somente a que deseja e seleciona apenas algumas colunas:
    df = df.query(f'CD_ESTACAO=="{cod}"')
    
    return df[['DC_NOME','CD_ESTACAO','VL_LATITUDE','VL_ALTITUDE','VL_LONGITUDE','CD_SITUACAO','DT_INICIO_OPERACAO']]

def coleta_dado(data_inicial = '2020-01-01',data_final = '2021-01-01',cod = 'A701'):
    '''
    Parâmetros: 
    * data_inicial = no formato %Y-%m-%d
    exemplo(default) = '2020-01-01'
    
    * data_final = no formato %Y-%m-%d
    exemplo(default) = '2021-01-01'
    
    * (Código da estação) cod = 'A701'
    ---------------------------------------
    Retorna um dataframe com todos os dados captados de 1 em 1 hora
    da  estação escolhida, pelo período escolhido.
    As colunas são condforme descrito o API:
    
    https://portal.inmet.gov.br/manual/manual-de-uso-da-api-esta%C3%A7%C3%B5es
    
    '''
    url = requests.get(f'https://apitempo.inmet.gov.br/estacao/{data_inicial}/{data_final}/{cod}').json()
    df = pd.read_json(json.dumps(url))
    df.to_csv('Dados/data_raw.csv',sep=';',index=False)
    return df


#### Tratamento -----------------------------------------------------

def HORA_UTC(df):
    '''
    Parâmetro : dataframe
    -------------------------------------------------------------------
    O que faz: Adequa a coluna 'DT_MEDICAO' 
    para ficar {ano-mes-dia hora:min:seg}
    --------------------------------------------------------------------
    Retorna: O head() do dataframe com o formato em datetime com 
    formato descrito
    
    '''
    df.loc[:,'DT_MEDICAO'] =  pd.to_datetime(df.loc[:,'DT_MEDICAO'], format='%Y-%m-%d')
    
    def hora_UTC(df):
        '''Transformando o df['HR_MEDICAO'] que está em UTC para o correspondente para o BRASIL.
        Sendo a hora 0 = 21h.
        Criando uma coluna ['HR'] para esses valores  '''
        hora_br = 0
        HORA=[]

        for hora in df['HR_MEDICAO']:
            if hora/100+21 >= 25:
                hora_br = (hora/100+21)-24
            else:
                hora_br = hora/100+21
            HORA.append(hora_br)
        df.loc[:,'HORA'] = HORA
        df['HORA'] = df['HORA'].astype(int)
    
    # usa a função que tranforma a coluna HR_MEDICAO que está em UTC em formato 24h
    hora_UTC(df)
    
    # Acertando a coluna DT_MEDICAO pra ficar no formato ano-mes-dia hora:min:seg
    df.loc[df["HORA"] == 24, "HORA"] = 0
    df=df.astype({'HORA':'string'})
    df['HORA']=df['HORA'] + ':00:00'
    # df=df.astype({'DT_MEDICAO':'string'})
    # df['DT_MEDICAO']=df['DT_MEDICAO']+ ' '+df['HORA']
    
    # Dropando as colunas auxiliares criadas
    #df.drop('HORA', axis=1, inplace=True)
    df.drop('HR_MEDICAO', axis=1, inplace=True)
    
    #trasformando a timeseries no index
    #df.set_index('DT_MEDICAO', drop=True, inplace=True)                                    
    #df.index = pd.DatetimeIndex(df.index)
    return df.head()

# tratando nulls --------------

def p_null(df):
    """
    Mostra as colunas que tem null e que não tem e suas porcentagens.
    """
    for column in df.columns:
        null = df[column].isnull().sum()
        p = (null/(df.shape[0]))*100
        if df[column].isnull().sum()==0:
            continue
        else:
            print(f'{column}: {p.round(2)}% or {null}nulls',)
    print( )
    
    print('The columns with the most % nulls are:')
    print(((df.isnull().sum()/df.shape[0])*100).sort_values(ascending = False))

def treat_null_RAD(df):
    # Fazendo o tratamento do restante dos nulls com o method=ffill
    df.fillna(method='ffill',inplace=True)
    condiction = df.loc[:,'HORA']>=19.0                   # condição se o horário é mais que 19h
    df.loc[:,'RAD']  = np.where(condiction, 0.0 ,df.loc[:,'RAD_GLO'])
    condiction2 = df.loc[:,'HORA'] <= 5.0                 # condição se o horário é menos que 5h
    df['RAD']  = np.where(condiction2, 0.0 ,df['RAD'])
    df['RAD']  = df['RAD'].apply(lambda x: 0.0 if x<0 else x) # ou se negativo é igual a zero
    #Separa agora somente os que tem radiação >0 pra não afetar a média se trabalhar com dia
    #df = df.loc[df['RAD']>0]
    
    # salva arquivo tratado
    df.to_csv('Dados/data_tratado.csv',sep=';',index=False)
    return p_null(df)
  
def is_constant(df):
    col_constant=[]
    p_col_cte=0
    for column in df.columns:
        if len(df[column].unique())==1:
            col_constant.append(column)
            print(f'{column} is constant.') 
            
        else:
            print(f'{column} OK!')
            
    p_col_cte = (len(col_constant)/len(df.columns))*100        
    print('-=-'*30 )
    print(f'The % of cte column is: {p_col_cte:.3f}% ')
    print(f'The % of not cte columns is: {(100-p_col_cte):.3f}%')
    
def low_var(df, low_variance_threshold=0.001):
    from sklearn.preprocessing import MinMaxScaler
    import pandas as pd
    import numpy as np
    minmax = MinMaxScaler()
    variaveis_numericas_df = df.select_dtypes(exclude=['object'])
    variaveis_numericas_escaladas_df = minmax.fit_transform(variaveis_numericas_df)
    variaveis_numericas_escaladas_df = pd.DataFrame(variaveis_numericas_escaladas_df,
                                                 columns = variaveis_numericas_df.columns)
    listLowVariance = []
    for col in variaveis_numericas_escaladas_df.columns:
        if np.var(variaveis_numericas_escaladas_df[col]) > low_variance_threshold:
            print(f'{col}: {np.var(variaveis_numericas_escaladas_df[col]):.5f}  OK!')
        else:
            print(f'{col} baixa variância: {np.var(variaveis_numericas_escaladas_df[col]):.5f}')
            listLowVariance.append(col)
    print('A(s) coluna(s) com baixa variância: ',listLowVariance)
    return listLowVariance