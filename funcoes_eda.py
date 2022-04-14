import pandas as pd
import warnings
warnings.filterwarnings('ignore')


#--------------------------------------------------------------------------
## Coleta e tratamento dos dados

# Mostra as correlações

import matplotlib.pyplot as plt 
import seaborn as sns
def correlacao(df):
    """
    Mostra as correlacoes.
    """
    lista_correlacoes = ['spearman','pearson']
    for lista in lista_correlacoes:
        corr = df.drop(columns=["DC_NOME", "UF","CD_ESTACAO","RAD_GLO","VL_LONGITUDE","VL_LATITUDE","DT_MEDICAO"]).corr(method = lista)
        print(lista)
        display(corr.corr()['RAD'].sort_values(ascending=True))
        #plt.figure(dpi=1000)
        #sns.heatmap(corr, robust=True, linewidths=.1, square=True)
        #plt.title('Correlação de ' + lista)
        #plt.show()

#Soma dos função dos meses
        
import seaborn as sns
#mudar rad para float
def EDA(df, cols):
    df['RAD'] = df['RAD'].astype(float)
    for col in cols:
        sns.barplot(x='MES', y=col, data=df, estimator=sum, ec='black', ci=None).set_title(f'{col} em função dos Meses')
        ax.grid(axis='y')
        plt.show()       


# Histograma

def EDA_HIST(df, cols):
    for col in cols:
        sns.histplot(data = df[col].loc[(df[col] > 0)], kde = True).set_title(f'SÃO PAULO - MIRANTE - {col}')
        ax.grid(axis='y')
        plt.show()   

# Plot

def EDA_PLOT(df, cols):
    for col in cols:
        df.plot(x='HORA', y=col, style='b.', figsize=(15,5))
        df.groupby('HORA')[col].agg('mean').plot(legend=True, colormap='Reds_r')
        plt.title('SAO PAULO - MIRANTE')
        plt.ylabel(col)
        plt.show() 

#BoxPlot meses

def EDA_boxplot(df, cols):    
    ts=df[['DT_MEDICAO','RAD','UMD_INS','CHUVA']]
    ts=ts.groupby('DT_MEDICAO').agg({'RAD':'sum','CHUVA':'sum','UMD_INS':'mean'})
    ts['month_name'] = ts.index.month_name()
    for col in cols:
        fig, ax = plt.subplots(figsize = (12, 8))
        sns.boxplot(y = ts[col], x = ts['month_name'], ax = ax).set_title(f'Boxplot de - {col}')

#box Plot Anos

def EDA_boxplot_year(ts, cols):    
    ts=df[['DT_MEDICAO','RAD','UMD_INS','CHUVA']]
    ts=ts.groupby('DT_MEDICAO')['RAD','UMD_INS','CHUVA'].sum()
    ts['year_name'] = ts.index.year
    for col in cols:
        fig, ax = plt.subplots(figsize = (12, 8))
        sns.boxplot(y = ts[col], x = ts['year_name'], ax = ax).set_title(f'Boxplot de - {col}')

        
#---------------------------------------------------------------------------------------

def corr_triangle(df):
    '''
    Cria uma matrix de correlação entre as features da df dada, em formato de triangulo.
    ---------------------------------------------------------------
    parâmetro: dataframe que quer ver a correlação
    ---------------------------------------------------------------
    Retorna: Um heatmap em formato triangular das correlações entre as
    features da dataframe informada.
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    plt.figure(figsize=(20, 10))
    # define the mask to set the values in the upper triangle to True
    mask = np.triu(np.ones_like(df.corr(), dtype=bool))
    heatmap = sns.heatmap(df.corr(),mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Triangle Correlation Heatmap', fontdict={'fontsize':18}, pad=16);
    
def graf_tempo_dia(df,coluna_data,target, xlabel='Data da medição[dia]',ylabel='Radiação[KJ/m²]',step = 30):
    
    import matplotlib.pyplot as plt 
    df_dia = df.groupby([coluna_data],as_index=False).mean() 
    plt.figure(facecolor='#f9f9f9',edgecolor= '#4a646c',figsize=(20,5))
    plt.plot(df_dia[coluna_data] , df_dia[target],'o-',color='#0099cb')#
    plt.xlabel(xlabel,fontsize= 15)
    plt.ylabel(ylabel,fontsize=16)
    plt.axhline(df[target].mean(),c = '#ff4040',label=f'{target}_média')
    plt.grid(True, 'both','both')
    plt.xticks(df_dia.iloc[range(0,df_dia.shape[0],step),0],rotation=90)
    plt.legend(fontsize=15);
    
def box_tempo_for(df,figsize=(15,5),coluna_data ='data',
            colunas = None,
            xlabel = 'Anos',
            palette = None ):
    '''
    A função faz boxplot de uma lista de colunas tendo como o eixo x o tempo.
    ---------------------------------------------------------------------------
    parâmetro: dataframe, tamanho da figura, a coluna que tem o tempo(será o eixo x), 
    lista com as colunas pra fazer o loop, label do eixo x(normalmente Anos - default), e 
    paleta de cores.
    ----------------------------------------------------------------------------
    Retorna vários boxplot conforme a lista dada ao longo do tempo
    '''
    for col in colunas:
        figsize = figsize
        title = f'Variação de {col} ao longo do Ano '
        fig, ax = plt.subplots(figsize = figsize)
        sns.boxplot(x=coluna_data ,y=col,data = df, ax = ax,palette = palette )
        ax.set(title = title, xlabel = xlabel, ylabel = f'{col}')
        plt.grid(True, 'both','both');
        
def box_plot(df,
             figsize=(10,4),
             x = None,
             y = None):
    '''
    Parâmetros: 
    df=dataframe,
    figsize = tamanho da figura
    x = variaveis categóricas
    y = variaveis numéricas
    -------------------------------------------
    Retorna boxplot das var numéricas separadas pelas
    categóricas.
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    xlabel = f'{x}'
    ylabel = f'{y}'
    title = f'Variação de {ylabel} por {xlabel}'
    
    fig, ax = plt.subplots(figsize = figsize)
    sns.boxplot(x=x ,y=y ,data=df, linewidth=1.5, ax = ax)
    ax.set(title = title, xlabel = xlabel, ylabel = ylabel)
    #plt.grid(True, 'both','both');
    
# função para gerar um histograma a partir de uma variável do data frame
def gerar_histograma(data_frame,
                     variavel, 
                     bins = 30,
                     color = 'purple',
                     #xlabel = xlabel,
                     ylabel = 'Frequência',
                     titulo = 'Histograma',
                     fontsize = 16,
                     fontweight = 'bold',
                     figsize = (8,5)
                    ):
    '''
    Gera um histograma: frequencia de vezes a variável dada repetiu.
    É possível fazer um for. É só colocar:
    for var in lista_variaveis_quantitativa:
        gerar_histograma(df, var)
    
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    xlabel = f'{variavel}'
    fig, ax = plt.subplots(figsize = figsize)
    sns.histplot(data_frame[variavel], bins = bins, color = color, kde = True)
    ax.set(xlabel = xlabel, ylabel = ylabel)
    ax.set_title(titulo, fontsize = fontsize, fontweight = fontweight)
    plt.grid(True, 'both','both');
    
# função para gerar um histograma a partir de uma variável do data frame
def gerar_histograma(data_frame,
                     variavel, 
                     bins = 30,
                     color = 'purple',
                     #xlabel = xlabel,
                     ylabel = 'Frequência',
                     titulo = 'Histograma',
                     fontsize = 16,
                     fontweight = 'bold',
                     figsize = (8,5)
                    ):
    '''
    Gera um histograma: frequencia de vezes a variável dada repetiu.
    É possível fazer um for. É só colocar:
    for var in lista_variaveis_quantitativa:
        gerar_histograma(df, var)
    
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    xlabel = f'{variavel}'
    fig, ax = plt.subplots(figsize = figsize)
    sns.histplot(data_frame[variavel], bins = bins, color = color, kde = True)
    ax.set(xlabel = xlabel, ylabel = ylabel)
    ax.set_title(titulo, fontsize = fontsize, fontweight = fontweight)
    plt.grid(True, 'both','both');
    
def gerar_Log_histograma(data_frame,
                     variavel, 
                     bins = 30,
                     color = 'purple', 
                     fontsize = 16,
                     fontweight = 'bold',
                     figsize = (8,5)
                    ):
    '''
    Gera um histograma: frequencia de vezes a variável dada repetiu.
    É possível fazer um for. É só colocar:
    for var in lista_variaveis_quantitativa:
        gerar_histograma(df, var)
    
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    xlabel = f'{variavel}'
    ylabel = 'Frequência'
    titulo = f'Histograma de Log{variavel}'
    fig, ax = plt.subplots(figsize = figsize)
    sns.histplot(np.log(data_frame[variavel]+1), bins = bins, color = color, kde = True)
    ax.set(xlabel = xlabel, ylabel = ylabel)
    ax.set_title(titulo, fontsize = fontsize, fontweight = fontweight)
    plt.grid(True, 'both','both');

 
 
def graficos_subplot(df_dia ,ano_incial=2011,ano_final=2021, xlabel = 'Data da medição[dia]'):
    '''
    df_dia_(Estação);
    ano_incial = 2011
    ano_incial = 2021
    '''
    import matplotlib.pyplot as plt
    
    ## Para formatação das Legendas 
    name_city = 'São Paulo '    #df_dia['cidade'][0]
    name_estation = 'A701'      #df_dia['estacao'][0]
    
    # Seleciona dias
    ano_incial = ano_incial
    ano_final = ano_final

    anos = range(ano_incial,ano_final,1)
    for ano in anos:
        df = df_dia.query(f'ANO == {ano}')

        fig, ax = plt.subplots(1, 2, figsize=(20, 6))

        ##  ------ RADIAÇÃO GLOBAL W/m²  ------------
        
        fig.suptitle(f'Gráficos da estação {name_estation} em {name_city} no ano {ano}')
        ax[0].plot(df.index , df['RAD'],'o-')
        ax[0].set_xlabel(xlabel,fontsize= 15)
        ax[0].set_ylabel('Radiação[W/m²]',fontsize=16)
        ax[0].axhline(df['RAD'].mean(),c = 'red',label='Radiação_média')
        ax[0].grid(True, 'both','both')
        ax[0].set_title(f'Radiação global diária média[W/m²] durante o ano {ano}')
        #ax[0].set_xticks(df.index.iloc[range(0,df.shape[0],10),0])
        ax[0].tick_params(axis='x', rotation=90)
        ax[0].legend(fontsize=15);

        ##  ------ 'TEM_MAX': TEMPERATURA MÁXIMA NA HORA ANT. °C,  ------------
        ax[1].plot(df.index , df['TEM_MAX'],'o-',color = 'black')
        ax[1].set_title(f'Temperatura[°C] média diária durante o ano {ano}')
        ax[1].set_xlabel(xlabel,fontsize= 15)
        ax[1].set_ylabel('Temperatura[°C]',fontsize=16)
        ax[1].axhline(df['TEM_MAX'].mean(),c = 'red',label='TMax_média')
        ax[1].grid(True, 'both','both')
        #ax[1].set_xticks(df.iloc[range(0,df.shape[0],10),0])
        ax[1].tick_params(axis='x', rotation=90)        
        ax[1].legend(fontsize=15);
    