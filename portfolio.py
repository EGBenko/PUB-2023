import pandas
import numpy as np
from itertools import combinations
import time

t_start = time.perf_counter()
ibov_df = pandas.read_csv('data\Processada\IBOV_p.csv',index_col=0)
selic_df = pandas.read_csv('data\Processada\Selic_p.csv',index_col=0)
df = pandas.read_csv("RetornoDiario.csv", sep=';', encoding = 'ISO-8859-1', index_col=0)

selic_index = selic_df.index.values.tolist()
ibov_index = ibov_df.index.values.tolist()
df_index = df.index.values.tolist()
inic_s = selic_index.index(df_index[0])
inic_ib = ibov_index.index(df_index[0])
Selic_1M = list()
Selic_3M = list()
Selic_6M = list()
Selic_12M = list()
Selic_24M = list()
Ibov_1M = list()
Ibov_3M = list()
Ibov_6M = list()
Ibov_12M = list()
Ibov_24M = list()

for i in range(df.shape[0]):
    s = selic_df.iloc[inic_s+i, 1] #Retorno %a.d.
    ib = ibov_df.iloc[inic_ib+i, 4] #Close

    Selic_1M.append(s)
    if len(Selic_1M) >= 22:
            Selic_1M.pop(0)
    Selic_3M.append(s)
    if len(Selic_3M) >= 64:
            Selic_3M.pop(0)
    Selic_6M.append(s)
    if len(Selic_6M) >= 127:
            Selic_6M.pop(0)
    Selic_12M.append(s)
    if len(Selic_12M) >= 253:
            Selic_12M.pop(0)
    Selic_24M.append(s)

    Ibov_1M.append(ib)
    if len(Ibov_1M) >=22:
           Ibov_1M.pop(0)
    Ibov_3M.append(ib)
    if len(Ibov_3M) >=64:
           Ibov_3M.pop(0)
    Ibov_6M.append(ib)
    if len(Ibov_6M) >=127:
           Ibov_6M.pop(0)
    Ibov_12M.append(ib)
    if len(Ibov_12M) >=253:
           Ibov_12M.pop(0)
    Ibov_24M.append(ib)

#Ibov variance
Ibov_var_1M = ((np.std(Ibov_1M, ddof=1)/Ibov_1M[-1]) *100)**2
Ibov_var_3M = ((np.std(Ibov_3M, ddof=1)/Ibov_3M[-1]) *100)**2
Ibov_var_6M = ((np.std(Ibov_6M, ddof=1)/Ibov_6M[-1]) *100)**2
Ibov_var_12M = ((np.std(Ibov_12M, ddof=1)/Ibov_12M[-1]) *100)**2
Ibov_var_24M = ((np.std(Ibov_24M, ddof=1)/Ibov_24M[-1]) *100)**2

#Ibov Retorno diario
Ibov_daily_1M = list()
Ibov_daily_3M = list()
Ibov_daily_6M = list()
Ibov_daily_12M = list()
Ibov_daily_24M = list()
anterior_price = ibov_df.iloc[inic_ib-1, 4]
for i in range (len(Ibov_24M)):
    retorno_diario_ib = ((Ibov_24M[i] - anterior_price)/Ibov_24M[i])*100
    anterior_price = Ibov_24M[i]
    Ibov_daily_1M.append(retorno_diario_ib)
    if len(Ibov_daily_1M) >= 22:
            Ibov_daily_1M.pop(0)
    Ibov_daily_3M.append(retorno_diario_ib)
    if len(Ibov_daily_3M) >= 64:
            Ibov_daily_3M.pop(0)
    Ibov_daily_6M.append(retorno_diario_ib)
    if len(Ibov_daily_6M) >= 127:
            Ibov_daily_6M.pop(0)
    Ibov_daily_12M.append(retorno_diario_ib)
    if len(Ibov_daily_12M) >= 253:
            Ibov_daily_12M.pop(0)
    Ibov_daily_24M.append(retorno_diario_ib)

#Ibov Retorno
Ibov_Retorno_1M = ((Ibov_1M[-1] - Ibov_1M[0])/Ibov_1M[0])*100
Ibov_Retorno_3M = ((Ibov_3M[-1] - Ibov_3M[0])/Ibov_3M[0])*100
Ibov_Retorno_6M = ((Ibov_6M[-1] - Ibov_6M[0])/Ibov_6M[0])*100
Ibov_Retorno_12M = ((Ibov_12M[-1] - Ibov_12M[0])/Ibov_12M[0])*100
Ibov_Retorno_24M = ((Ibov_24M[-1] - Ibov_24M[0])/Ibov_24M[0])*100

#Selic Return
sum_s = 1
for j in range(len(Selic_1M)):
    sum_s = sum_s * (1+(Selic_1M[j]/100))
Selic_Retorno_1M = (sum_s-1)*100
sum_s = 1
for j in range(len(Selic_3M)):
    sum_s = sum_s * (1+(Selic_3M[j]/100))
Selic_Retorno_3M = (sum_s-1)*100
sum_s = 1
for j in range(len(Selic_6M)):
    sum_s = sum_s * (1+(Selic_6M[j]/100))
Selic_Retorno_6M = (sum_s-1)*100
sum_s = 1
for j in range(len(Selic_12M)):
    sum_s = sum_s * (1+(Selic_12M[j]/100))
Selic_Retorno_12M = (sum_s-1)*100
sum_s = 1
for j in range(len(Selic_24M)):
    sum_s = sum_s * (1+(Selic_24M[j]/100))
Selic_Retorno_24M = (sum_s-1)*100

#Portfolios
portfolios = list( combinations(range(0,df.shape[1]), 4) )
num_portfolios = len(portfolios)
results = np.zeros((35, num_portfolios )) #num_portfolios

for i in range(num_portfolios): #num_portfolios
    print(i)
    weights = np.ones(4)/4
    #Close artificial do portfolio
    Close_1M = list()
    Close_3M = list()
    Close_6M = list()
    Close_12M = list()
    Close_24M = list()
    #Retorno diario do portfolio
    Close_daily_1M = list()
    Close_daily_3M = list()
    Close_daily_6M = list()
    Close_daily_12M = list()
    Close_daily_24M = list()
    #Close artificial de cada fundo
    fundo1 = 100 * weights[0]
    fundo2 = 100 * weights[1]
    fundo3 = 100 * weights[2]
    fundo4 = 100 * weights[3]
    
    for j in range(df.shape[0]):
        portfolio_price = fundo1 + fundo2 + fundo3 + fundo4
        fundo1 = fundo1 + (fundo1*df.iloc[j,portfolios[i][0]])/100
        fundo2 = fundo2 + (fundo2*df.iloc[j,portfolios[i][1]])/100
        fundo3 = fundo3 + (fundo3*df.iloc[j,portfolios[i][2]])/100
        fundo4 = fundo4 + (fundo4*df.iloc[j,portfolios[i][3]])/100

        #Close artificial do portfolio
        Close_1M.append(fundo1+fundo2+fundo3+fundo4)
        if len(Close_1M) >= 22:
            Close_1M.pop(0)
        Close_3M.append(fundo1+fundo2+fundo3+fundo4)
        if len(Close_3M) >= 64:
            Close_3M.pop(0)
        Close_6M.append(fundo1+fundo2+fundo3+fundo4)
        if len(Close_6M) >= 127:
            Close_6M.pop(0)
        Close_12M.append(fundo1+fundo2+fundo3+fundo4)
        if len(Close_12M) >= 253:
            Close_12M.pop(0)
        Close_24M.append(fundo1+fundo2+fundo3+fundo4)

        #Retorno diario do portfolio
        retorno_diario = (((fundo1+fundo2+fundo3+fundo4) - portfolio_price)/portfolio_price)*100
        Close_daily_1M.append(retorno_diario)
        if len(Close_daily_1M) >= 22:
            Close_daily_1M.pop(0)
        Close_daily_3M.append(retorno_diario)
        if len(Close_daily_3M) >= 64:
            Close_daily_3M.pop(0)
        Close_daily_6M.append(retorno_diario)
        if len(Close_daily_6M) >= 127:
            Close_daily_6M.pop(0)
        Close_daily_12M.append(retorno_diario)
        if len(Close_daily_12M) >= 253:
            Close_daily_12M.pop(0)
        Close_daily_24M.append(retorno_diario)
    
    #Retorno
    results[0,i] = ((Close_1M[-1] - Close_1M[0])/Close_1M[0])*100
    results[1,i] = ((Close_3M[-1] - Close_3M[0])/Close_3M[0])*100
    results[2,i] = ((Close_6M[-1] - Close_6M[0])/Close_6M[0])*100
    results[3,i] = ((Close_12M[-1] - Close_12M[0])/Close_12M[0])*100
    results[4,i] = ((Close_24M[-1] - Close_24M[0])/Close_24M[0])*100

    #Volatilidade
    results[5,i] = (np.std(Close_1M, ddof=1)/Close_1M[-1]) *100
    results[6,i] = (np.std(Close_3M, ddof=1)/Close_3M[-1]) *100
    results[7,i] = (np.std(Close_6M, ddof=1)/Close_6M[-1]) *100
    results[8,i] = (np.std(Close_12M, ddof=1)/Close_12M[-1]) *100
    results[9,i] = (np.std(Close_24M, ddof=1)/Close_24M[-1]) *100

    #Covariance com o mercado
    sum_cov_1M=0
    mean_c1 = np.mean(Close_1M)
    mean_ib1 = np.mean(Ibov_1M)
    for j in range(len(Close_1M)):
        sum_cov_1M = sum_cov_1M + ((Close_1M[j]-mean_c1)*(Ibov_1M[j]-mean_ib1))
    cov_1M = sum_cov_1M/(len(Close_1M)-1)

    sum_cov_3M=0
    mean_c3 = np.mean(Close_3M)
    mean_ib3 = np.mean(Ibov_3M)
    for j in range(len(Close_3M)):
        sum_cov_3M = sum_cov_3M + ((Close_3M[j]-mean_c3)*(Ibov_3M[j]-mean_ib3))
    cov_3M = sum_cov_3M/(len(Close_3M)-1)

    sum_cov_6M=0
    mean_c6 = np.mean(Close_6M)
    mean_ib6 = np.mean(Ibov_6M)
    for j in range(len(Close_6M)):
        sum_cov_6M = sum_cov_6M + ((Close_6M[j]-mean_c6)*(Ibov_6M[j]-mean_ib6))
    cov_6M = sum_cov_6M/(len(Close_6M)-1)

    sum_cov_12M=0
    mean_c12 = np.mean(Close_12M)
    mean_ib12 = np.mean(Ibov_12M)
    for j in range(len(Close_12M)):
        sum_cov_12M = sum_cov_12M + ((Close_12M[j]-mean_c12)*(Ibov_12M[j]-mean_ib12))
    cov_12M = sum_cov_12M/(len(Close_12M)-1)

    sum_cov_24M=0
    mean_c24 = np.mean(Close_24M)
    mean_ib24 = np.mean(Ibov_24M)
    for j in range(len(Close_24M)):
        sum_cov_24M = sum_cov_24M + ((Close_24M[j]-mean_c24)*(Ibov_24M[j]-mean_ib24))
    cov_24M = sum_cov_24M/(len(Close_24M)-1)
    
    #Beta
    results[10,i] = cov_1M/Ibov_var_1M
    results[11,i] = cov_3M/Ibov_var_3M
    results[12,i] = cov_6M/Ibov_var_6M
    results[13,i] = cov_12M/Ibov_var_12M
    results[14,i] = cov_24M/Ibov_var_24M

    #Sharpe
    results[15,i] = (results[0,i]-Selic_Retorno_1M)/results[5,i]
    results[16,i] = (results[1,i]-Selic_Retorno_3M)/results[6,i]
    results[17,i] = (results[2,i]-Selic_Retorno_6M)/results[7,i]
    results[18,i] = (results[3,i]-Selic_Retorno_12M)/results[8,i]
    results[19,i] = (results[4,i]-Selic_Retorno_24M)/results[9,i]

    #Treynor
    results[20,i] = (results[0,i]-Selic_Retorno_1M)/results[10,i]
    results[21,i] = (results[1,i]-Selic_Retorno_3M)/results[11,i]
    results[22,i] = (results[2,i]-Selic_Retorno_6M)/results[12,i]
    results[23,i] = (results[3,i]-Selic_Retorno_12M)/results[13,i]
    results[24,i] = (results[4,i]-Selic_Retorno_24M)/results[14,i]

    #Desvio padrao negativo
    downside_close_1M = list()
    downside_close_3M = list()
    downside_close_6M = list()
    downside_close_12M = list()
    downside_close_24M = list()

    for j in range(len(Close_daily_24M)):
        minimo = min(Close_daily_24M[j]- Ibov_daily_24M[j], 0)
        downside_close_1M.append(minimo**2)
        if len(downside_close_1M) >= 22:
            downside_close_1M.pop(0)
        downside_close_3M.append(minimo**2)
        if len(downside_close_3M) >= 64:
            downside_close_3M.pop(0)
        downside_close_6M.append(minimo**2)
        if len(downside_close_6M) >= 127:
            downside_close_6M.pop(0)
        downside_close_12M.append(minimo**2)
        if len(downside_close_12M) >= 253:
            downside_close_12M.pop(0)
        downside_close_24M.append(minimo**2)
    
    downside_std_1M = np.sqrt(sum(downside_close_1M)/len(downside_close_1M))
    if downside_std_1M == 0:
         downside_std_1M = 0.1
    downside_std_3M = np.sqrt(sum(downside_close_3M)/len(downside_close_3M))
    if downside_std_3M == 0:
         downside_std_3M = 0.1
    downside_std_6M = np.sqrt(sum(downside_close_6M)/len(downside_close_6M))
    if downside_std_6M == 0:
         downside_std_6M = 0.1
    downside_std_12M = np.sqrt(sum(downside_close_12M)/len(downside_close_12M))
    if downside_std_12M == 0:
         downside_std_12M = 0.1
    downside_std_24M = np.sqrt(sum(downside_close_24M)/len(downside_close_24M))
    if downside_std_24M == 0:
         downside_std_24M = 0.1

    #Sortino
    results[25,i] = (results[0,i]-Selic_Retorno_1M)/downside_std_1M
    results[26,i] = (results[1,i]-Selic_Retorno_3M)/downside_std_3M
    results[27,i] = (results[2,i]-Selic_Retorno_6M)/downside_std_6M
    results[28,i] = (results[3,i]-Selic_Retorno_12M)/downside_std_12M
    results[29,i] = (results[4,i]-Selic_Retorno_24M)/downside_std_24M

    #TrackingError
    Trackingerror_list_1M = list()
    Trackingerror_list_3M = list()
    Trackingerror_list_6M = list()
    Trackingerror_list_12M = list()
    Trackingerror_list_24M = list()

    for j in range(len(Close_daily_24M)):
         Trackingerror_list_1M.append(Close_daily_24M[j]-Ibov_daily_24M[j])
         if len(Trackingerror_list_1M) >= 22:
            Trackingerror_list_1M.pop(0)
         Trackingerror_list_3M.append(Close_daily_24M[j]-Ibov_daily_24M[j])
         if len(Trackingerror_list_3M) >= 64:
            Trackingerror_list_3M.pop(0)
         Trackingerror_list_6M.append(Close_daily_24M[j]-Ibov_daily_24M[j])
         if len(Trackingerror_list_6M) >= 127:
            Trackingerror_list_6M.pop(0)
         Trackingerror_list_12M.append(Close_daily_24M[j]-Ibov_daily_24M[j])
         if len(Trackingerror_list_12M) >= 253:
            Trackingerror_list_12M.pop(0)
         Trackingerror_list_24M.append(Close_daily_24M[j]-Ibov_daily_24M[j])
    
    #InfoRatio
    results[30,i] = (results[0,i]-Ibov_Retorno_1M)/np.std(Trackingerror_list_1M, ddof=1)
    results[31,i] = (results[1,i]-Ibov_Retorno_3M)/np.std(Trackingerror_list_3M, ddof=1)
    results[32,i] = (results[2,i]-Ibov_Retorno_6M)/np.std(Trackingerror_list_6M, ddof=1)
    results[33,i] = (results[3,i]-Ibov_Retorno_12M)/np.std(Trackingerror_list_12M, ddof=1)
    results[34,i] = (results[4,i]-Ibov_Retorno_24M)/np.std(Trackingerror_list_24M, ddof=1)

results_frame = pandas.DataFrame(results.T, columns = ['Retorno 1M/%','Retorno 3M/%','Retorno 6M/%','Retorno 12M/%','Retorno 24M/%','Desvio Padrão 1M/%','Desvio Padrão 3M/%','Desvio Padrão 6M/%','Desvio Padrão 12M/%','Desvio Padrão 24M/%'
                                                       ,'Beta 1M','Beta 3M','Beta 6M','Beta 12M','Beta 24M','Sharpe 1M','Sharpe 3M','Sharpe 6M','Sharpe 12M','Sharpe 24M',
                                                       'Treynor 1M', 'Treynor 3M', 'Treynor 6M', 'Treynor 12M', 'Treynor 24M', 'Sortino 1M', 'Sortino 3M', 'Sortino 6M', 'Sortino 12M', 'Sortino 24M',
                                                       'InfoRatio 1M','InfoRatio 3M','InfoRatio 6M','InfoRatio 12M','InfoRatio 24M',])

results_frame.to_csv('Portfolios.csv', encoding = 'ISO-8859-1')

t_stop = time.perf_counter()
print(t_stop-t_start, 'segundos')