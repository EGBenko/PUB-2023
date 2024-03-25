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
listinha = ['ABEV3', 'PETR3']
for stock in listinha:
    retorno(stock)
    volatilidade(stock)
    sharpe(stock)
    beta(stock)
    treynor(stock)
    info_ratio(stock)
    sortino(stock)
t_stop = time.perf_counter()
print(t_stop-t_start, 'segundos')

#gets+std+return+sharpe: 501.6275638999996 segundos