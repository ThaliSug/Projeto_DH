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

def EDA_boxplot(ts, cols):    
    ts=df[['DT_MEDICAO','RAD','UMD_MAX','CHUVA']]
    ts=ts.groupby('DT_MEDICAO')['RAD','UMD_MAX','CHUVA'].sum()
    ts['month_name'] = ts.index.month_name()
    for col in cols:
        fig, ax = plt.subplots(figsize = (12, 8))
        sns.boxplot(y = ts[col], x = ts['month_name'], ax = ax).set_title(f'Boxplot de - {col}')

#box Plot Anos

def EDA_boxplot_year(ts, cols):    
    ts=df[['DT_MEDICAO','RAD','UMD_MAX','CHUVA']]
    ts=ts.groupby('DT_MEDICAO')['RAD','UMD_MAX','CHUVA'].sum()
    ts['year_name'] = ts.index.year
    for col in cols:
        fig, ax = plt.subplots(figsize = (12, 8))
        sns.boxplot(y = ts[col], x = ts['year_name'], ax = ax).set_title(f'Boxplot de - {col}')
