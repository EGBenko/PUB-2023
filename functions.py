import pandas
import numpy as np
from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()

Ibovespa_list = ["RRRP3","ALOS3","ALPA4","ABEV3","ARZZ3","ASAI3","AZUL4","B3SA3","BBSE3","BBDC3","BBDC4","BRAP4","BBAS3",
                     "BRKM5","BRFS3","BPAC11","CRFB3","BHIA3","CCRO3","CMIG4","CIEL3","COGN3","CPLE6","CSAN3","CPFE3","CMIN3",
                     "CVCB3","CYRE3","DXCO3","ELET3","ELET6","EMBR3","ENGI11","ENEV3","EGIE3","EQTL3","EZTC3","FLRY3","GGBR4",
                     "GOAU4","NTCO3","SOMA3","HAPV3","HYPE3","IGTI11","IRBR3","ITSA4","ITUB4","JBSS3","KLBN11","RENT3","LREN3",
                     "LWSA3","MGLU3","MRFG3","BEEF3","MRVE3","MULT3","PCAR3","PETR3","PETR4","RECV3","PRIO3","PETZ3","RADL3",
                     "RAIZ4","RDOR3","RAIL3","SBSP3","SANB11","SMTO3","CSNA3","SLCE3","SUZB3","TAEE11","VIVT3","TIMS3","TOTS3",
                     "TRPL4","UGPA3","USIM5","VALE3","VAMO3","VBBR3","WEGE3","YDUQ3"]
#Fonte: https://www.b3.com.br/en_us/market-data-and-indices/indices/broad-indices/indice-ibovespa-ibovespa-composition-index-portfolio.htm

funds_list = ['TAEE11','SMAL11','BOVA11','KNHY11']

def get_data_market():

    data = tv.get_hist(symbol='IBOV', exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
    data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                , errors="raise", inplace=True)
    data.to_csv('data\IBOV.csv')

    return

def get_data_stocks():
    
    for stock in Ibovespa_list:
        data = tv.get_hist(symbol=stock, exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
        data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                    , errors="raise", inplace=True)
        data.to_csv('data\\'+stock+'.csv') 
        print('data\\'+stock+'.csv')

    return

def get_data_funds():
    
    for stock in funds_list:
        data = tv.get_hist(symbol=stock, exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
        data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                    , errors="raise", inplace=True)
        data.to_csv('data\\'+stock+'.csv') 

    return

#print(tv.search_symbol('','BMFBOVESPA'))

'''
Códigos dos intervalos:
Interval.in_1_minute, Interval.in_3_minute, Interval.in_5_minute, Interval.in_15_minute, Interval.in_30_minute, Interval.in_45_minute,
Interval.in_1_hour, Interval.in_2_hour, Interval.in_3_hour, Interval.in_4_hour, Interval.in_daily, Interval.in_weekly, Interval.in_monthly
'''

#A ser alterado conforme automatizacao da coleta - juntar com selic12M()
def Selic():
    Data = pandas.read_csv("Data\Selic.csv", sep=';')
    Data.columns = ['datetime','TaxaSelic']
    for i in range(Data.shape[0]):
        Data['datetime'][i]=pandas.to_datetime(Data['datetime'][i],format="%d/%m/%Y", errors='coerce')
    
    Data.set_index('datetime')

    for i in Data.index:
        taxa=float(Data['TaxaSelic'][i].replace(",", "."))
        Data['TaxaSelic'][i] = (((1+(taxa/100))**(1/252))-1)*100

    Data.to_csv('Data\SelicDiario.csv')
    return

def selic12M():
    Data = pandas.read_csv('data\SelicDiario.csv', index_col=0)
    Data.insert(Data.shape[1], 'Retorno Selic(12M)', value=0)
    aux = list()
    coluna= Data.columns.get_loc('TaxaSelic')
    coluna2= Data.columns.get_loc('Retorno Selic(12M)')

    for i in range(Data.shape[0]):
        soma = 1
        aux.append(Data.iloc[i, coluna])
        if i<2:
            continue
        if i>251:
            aux.pop(0)
        
        for j in range(len(aux)):
            soma = soma * (1+(aux[j]/100))
        
        Data.iloc[i, coluna2] = (soma-1)*100

    Data.to_csv('data\Selic12M.csv')

    return

def volatilidade(stock):
    Data = pandas.read_csv('data\\'+stock+'.csv', index_col=0)
    Data.insert(Data.shape[1], 'Standard Deviation(12M)', value=0)
    aux = list()
    coluna= Data.columns.get_loc('Close')
    colunastd= Data.columns.get_loc('Standard Deviation(12M)')

    for i in range(Data.shape[0]):
        aux.append(Data.iloc[i, coluna])
        if i<2:
            continue
        if i>251:
            aux.pop(0)
        
        #media = np.mean(aux, axis=1, keepdims=True)
        
        Data.iloc[i, colunastd] = np.std(aux, ddof=1)

    Data.to_csv('data\\'+stock+'.csv')
    return

#Retorno simples - logaritmico é o utilizado pela B3 #TODO
def retorno(stock, indx):
    Data = pandas.read_csv('data\\'+stock+'.csv', index_col=0)
    Data.insert(Data.shape[1], 'Retorno(12M)', value=0)
    aux = list()
    coluna= Data.columns.get_loc('Close')
    coluna2= Data.columns.get_loc('Retorno(12M)')

    for i in range(Data.shape[0]):
        aux.append(Data.iloc[i, coluna])
        if i<2:
            continue
        if i>251:
            aux.pop(0)
        
        Data.iloc[i, coluna2] = ((aux[-1] - aux[0])/aux[0])*100

    Data.to_csv('data\\'+stock+'.csv')
    return


def sharpe(stock):
    Data = pandas.read_csv('data\\'+stock+'.csv',index_col=0)
    dfselic = pandas.read_csv('data\Selic12M.csv',index_col=0)
    Data.insert(Data.shape[1], 'Sharpe(12M)', value=0)

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
    return 

def beta():

    return

def treynor(data):
    
    return data

def info_ratio(data):
    
    return data

def sortino(data):
    
    return data