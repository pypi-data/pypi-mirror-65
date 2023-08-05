from truedata_ws.websocket.TD import TD
import sys
from time import sleep

import pandas as pd

from colorama import Style, Fore

# Testing connection
td_app = TD(sys.argv[0], sys.argv[1], live_port=8082, historical_port=8092)

# Testing malformed live contracts
# hist_data_0 = td_app.start_live_data(f'BANKNIFTY99ZYXFUT')

# Testing Live data
# td_app.start_live_data(f'BANKNIFTY{sys.argv[3]}FUTbk')
req_id = td_app.start_live_data(f'CRUDEOIL-I')
count = 0
live_data_obj = td_app.live_data[req_id]
while count < 30:
    if live_data_obj != td_app.live_data[req_id]:
        print(td_app.live_data[req_id].__dict__)
        count = count + 1
        live_data_obj = td_app.live_data[req_id]

# Testing malformed historical contracts
hist_data_0 = td_app.get_historic_data(f'BANKNIFTY99ZYXFUT')

# Testing historical data
hist_data_1 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT')
hist_data_2 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', duration='3 D')
hist_data_3 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', duration='3 D', bar_size='15 mins')
hist_data_4 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', bar_size='30 mins')

print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 1...{Style.RESET_ALL}')
for hist_point in hist_data_1:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 2...{Style.RESET_ALL}')
for hist_point in hist_data_2:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 3...{Style.RESET_ALL}')
for hist_point in hist_data_3:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 4...{Style.RESET_ALL}')
for hist_point in hist_data_4:
    print(hist_point)

# Testing conversion to pandas dataframe
df = pd.DataFrame(hist_data_1)
print(df)
