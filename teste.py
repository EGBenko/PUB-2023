import pandas
import numpy as np

stock = 'ABEV3'

#sharpe

Data = pandas.read_csv('data\\'+stock+'.csv',index_col=0)
dfselic = pandas.read_csv('data\Selic12M.csv',index_col=0)
#Data.insert(Data.shape[1], 'Sharpe(12M)', value=0)

coluna = Data.columns.get_loc('Sharpe(12M)')
colunastd = Data.columns.get_loc('Standard Deviation(12M)')
colunaR = Data.columns.get_loc('Retorno(12M)')
colunaSelic = dfselic.columns.get_loc('Retorno Selic(12M)')
lista_index = dfselic.index.values.tolist()
aux = 0

for i, row in Data.iterrows():
    if aux<2:
        aux = aux + 1
        continue
    
    ind = 0

    index = i[:-9]
    while lista_index[ind] != index:
        ind = ind + 1
        if ind >= len(lista_index): 
            ind = ind - 1                  #desnivel nos dados
            break
    
    Data.iloc[aux, coluna] = (Data.iloc[aux, colunaR] - dfselic.iloc[ind, colunaSelic])/ Data.iloc[aux, colunastd]
    aux = aux + 1

Data.to_csv('data\\'+stock+'.csv')
