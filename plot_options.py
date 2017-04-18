#plot_options


import numpy as np
import datetime 
import matplotlib.pyplot as plt
from yahoo_finance import Share

CALL = 1
PUT = 2
BUY = 3
SELL = 4

symb = ''

##########################################
quote = web.get_quote_yahoo(symb)
option_m = Options(symb,'yahoo')
print option_m.expiry_dates
ex_date = option_m.expiry_dates[3]
data = option_m.get_options_data(expiry=ex_date)

##########################################

options = []
s = Share(symb)
price = float(s.get_price())
price = 100

x = np.arange(price*.7, price*1.3, 0.01)
y = np.zeros(len(x))
# options.append({'type':CALL, 'act':BUY , 'prem':10, 'strike': 100})
# options.append({'type':PUT,  'act':BUY , 'prem':5,  'strike': 95})
# options.append({'type':CALL, 'act':SELL ,'prem':3, 'strike': 103})
# options.append({'type':PUT,'act':SELL ,'prem':4, 'strike': 97})


plt.figure(0)

y_list = []

for opt in options:
    if opt['type']==CALL:
        if opt['act']==BUY:

            for i in range(0,len(x)):
                if x[i] < opt['strike']:
                    y[i] = -opt['prem']
                else:
                    y[i] = -opt['prem'] + (x[i]-opt['strike'])

            plt.plot(x,y)
            y_list.append(y.copy())
            continue

        if opt['act']==SELL:

            for i in range(0,len(x)):
                if x[i] < opt['strike']:
                    y[i] = opt['prem']
                else:
                    y[i] = opt['prem'] - (x[i]-opt['strike'])

            plt.plot(x,y)
            y_list.append(y.copy())
            continue


    if opt['type']==PUT:
        if opt['act']==BUY:

            for i in range(0,len(x)):
                if x[i] > opt['strike']:
                    y[i] = -opt['prem']
                else:
                    y[i] = -opt['prem'] + (-x[i]+opt['strike'])

            plt.plot(x,y)
            y_list.append(y.copy())
            continue

            
        if opt['act']==SELL:
            for i in range(0,len(x)):
                if x[i] > opt['strike']:
                    y[i] = opt['prem']
                else:
                    y[i] = opt['prem'] - (-x[i]+opt['strike'])

            plt.plot(x,y)
            y_list.append(y.copy())
            continue

y_tot = np.zeros(len(x))
for y in y_list:
    for i in range(0,len(x)):
        y_tot[i]+=y[i]

zeros = []

for i in range(5,len(y_tot)-5):
    if abs(y_tot[i-1])>abs(y_tot[i]) and abs(y_tot[i+1])>abs(y_tot[i]):
        zeros.append(x_p[i])

for zero in zeros:
    print 'Delta: %s' %((zero-price)/price * 100 )

plt.plot(x,y_tot,linewidth=4)




plt.plot([x[0],x[-1]],[0,0],'--')
plt.plot([price, price],[-15,15],'--')
plt.grid()
plt.show()

