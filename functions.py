import pandas
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from bcb import sgs

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
#coletados com o type=fund do print(tv.search_symbol('','BMFBOVESPA'))

def get_data_market():

    #IBOVESPA
    data = tv.get_hist(symbol='IBOV', exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
    data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                , errors="raise", inplace=True)
    data.to_csv('data\Bruta\IBOV.csv')

    #Selic
    selicdata = sgs.get((f'Selic anualizada base 252 - %a.a.', 1178), start = '2000-01-01')
    selicdata.insert(selicdata.shape[1], f'Selic %a.d.', value=0)
    for i in range(selicdata.shape[0]):
        taxa = selicdata.iloc[i,0]
        selicdata.iloc[i, 1] = (((1+(taxa/100))**(1/252))-1)*100
    selicdata.to_csv('data\Bruta\Selic.csv')

    return

def get_data_stocks():
    
    for stock in Ibovespa_list:
        data = tv.get_hist(symbol=stock, exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
        data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                    , errors="raise", inplace=True)
        data.to_csv('data\Bruta\\'+stock+'.csv')

    return

def get_data_funds():
    
    for stock in funds_list:
        data = tv.get_hist(symbol=stock, exchange='BMFBOVESPA', interval=Interval.in_daily, n_bars=5000)
        data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
                    , errors="raise", inplace=True)
        data.to_csv('data\Bruta\\'+stock+'.csv') 

    return

'''
Códigos dos intervalos:
Interval.in_1_minute, Interval.in_3_minute, Interval.in_5_minute, Interval.in_15_minute, Interval.in_30_minute, Interval.in_45_minute,
Interval.in_1_hour, Interval.in_2_hour, Interval.in_3_hour, Interval.in_4_hour, Interval.in_daily, Interval.in_weekly, Interval.in_monthly
'''

def selic_return():
    Data = pandas.read_csv('data\Bruta\Selic.csv', index_col=0)
    Coluna = Data.shape[1]
    Data.insert(Coluna, 'Retorno Selic(1M)', value=0)
    Data.insert(Coluna+1, 'Retorno Selic(3M)', value=0)
    Data.insert(Coluna+2, 'Retorno Selic(6M)', value=0)
    Data.insert(Coluna+3, 'Retorno Selic(12M)', value=0)
    aux1 = list()
    aux3 = list()
    aux6 = list()
    aux12 = list()

    #Selic 1M
    for i in range(Data.shape[0]):
        soma = 1
        aux1.append(Data.iloc[i, 1])
        if i<2:
            continue
        if i>=20:
            aux1.pop(0)
        
        for j in range(len(aux1)):
            soma = soma * (1+(aux1[j]/100))
        
        Data.iloc[i, Coluna] = (soma-1)*100

    #Selic 3M
    for i in range(Data.shape[0]):
        soma = 1
        aux3.append(Data.iloc[i, 1])
        if i<2:
            continue
        if i>=62:
            aux3.pop(0)
        
        for j in range(len(aux3)):
            soma = soma * (1+(aux3[j]/100))
        
        Data.iloc[i, Coluna+1] = (soma-1)*100

    #Selic 6M
    for i in range(Data.shape[0]):
        soma = 1
        aux6.append(Data.iloc[i, 1])
        if i<2:
            continue
        if i>=125:
            aux6.pop(0)
        
        for j in range(len(aux6)):
            soma = soma * (1+(aux6[j]/100))
        
        Data.iloc[i, Coluna+2] = (soma-1)*100

    #Selic 12M
    for i in range(Data.shape[0]):
        soma = 1
        aux12.append(Data.iloc[i, 1])
        if i<2:
            continue
        if i>=251:
            aux12.pop(0)
        
        for j in range(len(aux12)):
            soma = soma * (1+(aux12[j]/100))
        
        Data.iloc[i, Coluna+3] = (soma-1)*100

    Data.to_csv('data\Processada\Selic_p.csv')

    return

def volatilidade(stock):
    Data = pandas.read_csv('data\Processada\\'+stock+'_p.csv', index_col=0)
    Coluna = Data.shape[1]
    Data.insert(Coluna, 'Volatilidade(%/1M)', value=0)
    Data.insert(Coluna+1, 'Volatilidade(%/3M)', value=0)
    Data.insert(Coluna+2, 'Volatilidade(%/6M)', value=0)
    Data.insert(Coluna+3, 'Volatilidade(%/12M)', value=0)
    aux1 = list()
    aux3 = list()
    aux6 = list()
    aux12 = list()
    col_close= Data.columns.get_loc('Close')

    #STD 1M
    for i in range(Data.shape[0]):
        actprice1= Data.iloc[i, col_close]
        aux1.append(actprice1)
        if i<2:
            continue
        if i>=20:
            aux1.pop(0)
        
        Data.iloc[i, Coluna] = (np.std(aux1, ddof=1)/actprice1) *100

    #STD 3M
    for i in range(Data.shape[0]):
        actprice3= Data.iloc[i, col_close]
        aux3.append(actprice3)
        if i<2:
            continue
        if i>=62:
            aux3.pop(0)
        
        Data.iloc[i, Coluna+1] = (np.std(aux3, ddof=1)/actprice3) *100

    #STD 6M
    for i in range(Data.shape[0]):
        actprice6= Data.iloc[i, col_close]
        aux6.append(actprice6)
        if i<2:
            continue
        if i>=125:
            aux6.pop(0)
        
        Data.iloc[i, Coluna+2] = (np.std(aux6, ddof=1)/actprice6) *100

    #STD 12M
    for i in range(Data.shape[0]):
        actprice12= Data.iloc[i, col_close]
        aux12.append(actprice12)
        if i<2:
            continue
        if i>=251:
            aux12.pop(0)

        Data.iloc[i, Coluna+3] = (np.std(aux12, ddof=1)/actprice12) *100

    Data.to_csv('data\Processada\\'+stock+'_p.csv')
    return

#Retorno simples em (%)
def retorno(stock):
    Data = pandas.read_csv('data\Bruta\\'+stock+'.csv', index_col=0)
    Coluna=Data.shape[1]
    Data.insert(Coluna, 'Retorno(1M)', value=0)
    Data.insert(Coluna+1, 'Retorno(3M)', value=0)
    Data.insert(Coluna+2, 'Retorno(6M)', value=0)
    Data.insert(Coluna+3, 'Retorno(12M)', value=0)
    aux1 = list()
    aux3 = list()
    aux6 = list()
    aux12 = list()
    col_close= Data.columns.get_loc('Close')

    #Retorno 1M
    for i in range(Data.shape[0]):
        aux1.append(Data.iloc[i, col_close])
        if i<2:
            continue
        if i>=20:
            aux1.pop(0)
        
        Data.iloc[i, Coluna] = ((aux1[-1] - aux1[0])/aux1[0])*100

    #Retorno 3M
    for i in range(Data.shape[0]):
        aux3.append(Data.iloc[i, col_close])
        if i<2:
            continue
        if i>=62:
            aux3.pop(0)
        
        Data.iloc[i, Coluna+1] = ((aux3[-1] - aux3[0])/aux3[0])*100

    #Retorno 6M
    for i in range(Data.shape[0]):
        aux6.append(Data.iloc[i, col_close])
        if i<2:
            continue
        if i>=125:
            aux6.pop(0)
        
        Data.iloc[i, Coluna+2] = ((aux6[-1] - aux6[0])/aux6[0])*100

    #Retorno 12M
    for i in range(Data.shape[0]):
        aux12.append(Data.iloc[i, col_close])
        if i<2:
            continue
        if i>=251:
            aux12.pop(0)
        
        Data.iloc[i, Coluna+3] = ((aux12[-1] - aux12[0])/aux12[0])*100

    Data.to_csv('data\Processada\\'+stock+'_p.csv')
    return

def ibov_variance():
    retorno('IBOV')
    volatilidade('IBOV')   
    Data = pandas.read_csv('data\Processada\IBOV_p.csv', index_col=0)
    Coluna = Data.shape[1]
    Data.insert(Coluna, 'Variance(1M)', value=0)
    Data.insert(Coluna+1, 'Variance(3M)', value=0)
    Data.insert(Coluna+2, 'Variance(6M)', value=0)
    Data.insert(Coluna+3, 'Variance(12M)', value=0)
    col_std= Data.columns.get_loc('Volatilidade(%/1M)')
    aux1 = list()
    aux3 = list()
    aux6 = list()
    aux12 = list()

    for i in range(Data.shape[0]):
        #Variance 1M
        Data.iloc[i,Coluna] = Data.iloc[i,col_std] ** 2
        #Variance 3M
        Data.iloc[i,Coluna+1] = Data.iloc[i,col_std+1] ** 2
        #Variance 6M
        Data.iloc[i,Coluna+2] = Data.iloc[i,col_std+2] ** 2
        #Variance 12M
        Data.iloc[i,Coluna+3] = Data.iloc[i,col_std+3] ** 2

    Data.to_csv('data\Processada\IBOV_p.csv')
    return

def sharpe(stock):
    Data = pandas.read_csv('data\Processada\\'+stock+'_p.csv',index_col=0)
    selicdata = pandas.read_csv('data\Processada\Selic_p.csv',index_col=0)
    Coluna = Data.shape[1]
    Data.insert(Coluna, 'Sharpe(1M)', value=0)
    Data.insert(Coluna+1, 'Sharpe(3M)', value=0)
    Data.insert(Coluna+2, 'Sharpe(6M)', value=0)
    Data.insert(Coluna+3, 'Sharpe(12M)', value=0)
    selic_index = selicdata.index.values.tolist()
    Data_index = Data.index.values.tolist()
    lista=list()
    aux = -1

    #Verificar desnível nos dados
    while True:    
        if pandas.to_datetime(Data_index[aux][:-9]) == pandas.to_datetime(selic_index[-1]):
            break
        else:
            aux = aux - 1

    while aux < 0:
        Data.drop(Data_index[aux], inplace= True)
        aux = aux + 1
    
    for index, row in Data.iterrows():
        if Data.loc[index, 'Volatilidade(%/1M)']==0:
            continue
        #Sharpe 1M
        Data.loc[index,'Sharpe(1M)'] = (Data.loc[index, 'Retorno(1M)'] - selicdata.loc[index[:-9],'Retorno Selic(1M)'])/ Data.loc[index, 'Volatilidade(%/1M)']
        #Sharpe 3M
        Data.loc[index,'Sharpe(3M)'] = (Data.loc[index, 'Retorno(3M)'] - selicdata.loc[index[:-9],'Retorno Selic(3M)'])/ Data.loc[index, 'Volatilidade(%/3M)']
        #Sharpe 6M
        Data.loc[index,'Sharpe(6M)'] = (Data.loc[index, 'Retorno(6M)'] - selicdata.loc[index[:-9],'Retorno Selic(6M)'])/ Data.loc[index, 'Volatilidade(%/6M)']
        #Sharpe 12M
        Data.loc[index,'Sharpe(12M)'] = (Data.loc[index, 'Retorno(12M)'] - selicdata.loc[index[:-9],'Retorno Selic(12M)'])/ Data.loc[index, 'Volatilidade(%/12M)']

    Data.to_csv('data\Processada\\'+stock+'_p.csv')
    return 

def beta():

    return

def treynor(data):
    
    return data

def info_ratio(stock):
    Data = pandas.read_csv('data\Processada\\'+stock+'_p.csv',index_col=0)
    ibovdata = pandas.read_csv('data\Processada\IBOV_p.csv',index_col=0)
    Coluna = Data.shape[1]
    Data.insert(Coluna, 'InfoRatio(1M)', value=0)
    Data.insert(Coluna+1, 'InfoRatio(3M)', value=0)
    Data.insert(Coluna+2, 'InfoRatio(6M)', value=0)
    Data.insert(Coluna+3, 'InfoRatio(12M)', value=0)
    aux1 = list()
    aux3 = list()
    aux6 = list()
    aux12 = list()
    aux = 0

    #Desnível nos dados
    ibov_index = ibovdata.index.values.tolist()
    Data_index = Data.index.values.tolist()
    if '2007-12-13 09:00:00' in Data_index:
        Data.drop('2007-12-13 09:00:00',inplace=True)
    if '2008-05-20 10:00:00' in Data_index:
        Data.drop('2008-05-20 10:00:00',inplace=True)
    if pandas.to_datetime(Data_index[0]) < pandas.to_datetime(ibov_index[0]):
        while True:    
            if pandas.to_datetime(Data_index[aux]) == pandas.to_datetime(ibov_index[0]):
                break
            else:
                aux = aux +1

    while aux >= 0:
            Data.drop(Data_index[aux], inplace= True)
            aux = aux - 1

    #Tracking Error (TE)
    #1M
    for index, row in Data.iterrows():
        aux1.append(Data.loc[index, 'Retorno(1M)']-ibovdata.loc[index, 'Retorno(1M)'])
        if len(aux1) >= 22:
            aux1.pop(0)
        if len(aux1)<2:
            continue
        TE1= np.std(aux1, ddof=1)
        if TE1 ==0:
            continue
        #InfoRatio 1M
        Data.loc[index,'InfoRatio(1M)'] = (Data.loc[index, 'Retorno(1M)'] - ibovdata.loc[index,'Retorno(1M)'])/ TE1

    #3M
    for index, row in Data.iterrows():
        aux3.append(Data.loc[index, 'Retorno(3M)']-ibovdata.loc[index, 'Retorno(3M)'])
        if len(aux3) >= 64:
            aux3.pop(0)
        if len(aux3)<2:
            continue
        TE3= np.std(aux3, ddof=1)
        if TE3 ==0:
            continue
        #InfoRatio 3M
        Data.loc[index,'InfoRatio(3M)'] = (Data.loc[index, 'Retorno(3M)'] - ibovdata.loc[index,'Retorno(3M)'])/ TE3

    #6M
    for index, row in Data.iterrows():
        aux6.append(Data.loc[index, 'Retorno(6M)']-ibovdata.loc[index, 'Retorno(6M)'])
        if len(aux6) >= 127:
            aux6.pop(0)
        if len(aux6)<2:
            continue
        TE6= np.std(aux6, ddof=1)
        if TE6 ==0:
            continue
        #InfoRatio 6M
        Data.loc[index,'InfoRatio(6M)'] = (Data.loc[index, 'Retorno(6M)'] - ibovdata.loc[index,'Retorno(6M)'])/ TE6

    #12M
    for index, row in Data.iterrows():
        aux12.append(Data.loc[index, 'Retorno(12M)']-ibovdata.loc[index, 'Retorno(12M)'])
        if len(aux12) >= 253:
            aux12.pop(0)
        if len(aux12)<2:
            continue
        TE12= np.std(aux12, ddof=1)
        if TE12 ==0:
            continue
        #InfoRatio 12M
        Data.loc[index,'InfoRatio(12M)'] = (Data.loc[index, 'Retorno(12M)'] - ibovdata.loc[index,'Retorno(12M)'])/ TE12

    Data.to_csv('data\Processada\\'+stock+'_p.csv')
    return

def sortino(data):
    
    return data