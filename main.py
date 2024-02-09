#módulos
from functions import *
import time

'''
#Coleta de dados
t_start = time.perf_counter()
get_data_market()
get_data_stocks()
get_data_funds()
t_stop = time.perf_counter()
print(t_stop-t_start, 'segundos')

#gets: 137.55519150000327 segundos
'''

#Processar Tabela Selic (Fonte: https://www3.bcb.gov.br/sgspub/consultarvalores/telaCvsSelecionarSeries.paint)
#functions.daily_selic()


#Cálculo de indicadores
for stock in Ibovespa_list:
    print(stock)
    volatilidade(stock)
    #sharpe(stock)
    #treynor(data)
    #info_ratio(data)
    #sortino(data)
