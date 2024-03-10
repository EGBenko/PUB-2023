#módulos
from functions import *
import time


#Coleta de dados
t_start = time.perf_counter()
get_data_market()
selic_return()
ibov_variance()
get_data_stocks()
get_data_funds()

#Cálculo de indicadores
#rodar retorno() primeiro
#rodar sharpe antes dos outros indicadores

for stock in Ibovespa_list:
    retorno(stock)
    volatilidade(stock)
    sharpe(stock)
    #treynor(data)
    info_ratio(stock)
    #sortino(data)
t_stop = time.perf_counter()
print(t_stop-t_start, 'segundos')

#gets+std+return+sharpe: 501.6275638999996 segundos