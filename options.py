from pandas_datareader.data import Options
import pandas_datareader.data as web
import datetime
import pprint
import matplotlib.pyplot as plt
import numpy as np 
import time
import sys
#print F.expiry_dates,'\n'






# print '\n\n'
#print data.iloc[0].name
#print data.iloc[0]['JSON']#['strike']
# print '\n\n'
# print data.iloc[1].name
# print data.iloc[1]['JSON']['strike']

def call_intrinsic(stock,strike):
    in_val = stock.iloc[0]['last']-strike
    return in_val

def call_extrinsic(stock,strike,premium):
    val = premium - call_intrinsic(stock,strike)
    return val

def put_intrinsic(stock,strike):
    in_val = - stock.iloc[0]['last'] +strike
    return in_val



def calc_butterfly_call(s_low, s_mid, s_high, d_low, d_mid, d_high, d_expire):
    calc = {}
    info = {}
    net_debit = d_low - (2*d_mid) + d_high

    info['strike_low'] = s_low
    info['strike_mid'] = s_mid
    info['strike_high'] = s_high
    info['price_low'] = d_low
    info['price_mid'] = d_mid
    info['price_high'] = d_high

    loss1 = -d_low+2*d_mid-d_high
    loss2 = (-d_high+s_high-s_high)+(2*d_mid-2*(s_high-s_mid))+(-d_low+s_high-s_low)
    max_p = -d_high+2*d_mid+(-d_low+s_mid-s_low)

    calc['low_break'] = s_low + net_debit
    calc['high_break'] = s_high - net_debit
    calc['max_profit'] = [s_mid - s_low - net_debit,max_p]
    calc['min_profit'] = min(loss1,loss2)#-net_debit
    calc['total_liq'] = 100*(d_low+d_high)
    calc['days'] = (d_expire-datetime.date.today()).days
    calc['width'] = calc['high_break']-calc['low_break']

    rtrn = {'info':info, 'calc':calc}
    return rtrn

def calc_iron_condor(buyPut,sellPut,sellCall,buyCall, d1, d2, d3, d4):

    # sellPut > buyPut
    # sellCall< buyCall

    calc = {}
    info = {}
    net_premium = -d1 + d2 + d3 - d4


    info['strike_low']  = buyPut
    info['strike_mid1'] = sellPut
    info['strike_mid2'] = sellCall   
    info['strike_high'] = buyCall
    info['price_low']   = d1
    info['price_mid1']  = d2
    info['price_mid2']  = d3
    info['price_high']  = d4

    calc['max_profit'] = net_premium 
    calc['low_break']  = d2-net_premium
    calc['high_break'] = d3+net_premium
    calc['min_profit'] = -np.max( [buyCall-sellCall-net_premium , sellPut-buyPut-net_premium])
    calc['width'] = calc['high_break']-calc['low_break']

    rtrn = {'info':info, 'calc':calc}

    # print '\nPrices: -%.2f  %.2f   %.2f  -%.2f '%(d1,d2,d3,d4)
    # print 'strikes: %.2f   %.2f   %.2f    %.2f' %(buyPut,sellPut,sellCall,buyCall)
    # print 'net premium: %.1f, max loss %.1f' %(net_premium,calc['min_profit'])

    return rtrn

def loop_iron_condor(calls,puts):

    OTM_calls = []
    OTM_puts = []

    for i in range(0,len(calls)):
        if not calls[i]['inTheMoney']:
            OTM_calls.append(calls[i])

    for i in range(0,len(puts)):
        if not puts[i]['inTheMoney']:
            OTM_puts.append(puts[i])

    put_pairs = []
    for i in range(0,len(OTM_puts)-1):
        for j in range( i+1,len(OTM_puts) ):
            put_pairs.append( [OTM_puts[i],OTM_puts[j]] ) #low strike, high strike

    call_pairs = []
    for i in range(0,len(OTM_calls)-1):
        for j in range(i+1,len(OTM_calls)):
            call_pairs.append( [OTM_calls[i] , OTM_calls[j]] )

    condors = []

    for pairP in put_pairs:
        for pairC in call_pairs:
            s_low = pairP[0]['strike']
            s_mid1 = pairP[1]['strike']
            s_mid2 = pairC[0]['strike']
            s_high = pairC[1]['strike']

            p_low = pairP[0]['lastPrice']
            p_mid1 = pairP[1]['lastPrice']
            p_mid2 = pairC[0]['lastPrice']
            p_high = pairC[1]['lastPrice']
            
            if  abs(abs(s_mid1-s_low) - abs(s_high-s_mid2))<1:

                condors.append(calc_iron_condor(s_low,s_mid1,s_mid2,s_high, p_low,p_mid1,p_mid2,p_high))




    condors.sort(key=lambda r: -r['calc']['min_profit'])

    return condors

def loop_butterfly_call(calls,ex_date):
    # Find Center call to sell.
    for i in range(0,len(calls)):
        #print calls[i]['strike']
        if not calls[i]['inTheMoney'] and i>0:
            in_center = [i-1,i]
            print 'Center: ',in_center
            break

    in_low = []
    for i in range(0,in_center[0]):
        in_low.append(i)

    in_high = []
    for i in range(in_center[1]+1,len(calls)-1):
        in_high.append(i)

    #print in_low,in_center,in_high

    butterflies = []
    for i in in_center:
        for j in in_low:
            for k in in_high:
                #print i,j,k
                s_mid = calls[i]['strike']
                s_low = calls[j]['strike']
                s_high = calls[k]['strike']
                d_mid = calls[i]['lastPrice']
                d_low = calls[j]['lastPrice']
                d_high = calls[k]['lastPrice']

                butterflies.append(calc_butterfly_call(s_low, s_mid, s_high, d_low, d_mid, d_high, ex_date))

    butterflies.sort(key=lambda r: -r['calc']['min_profit'])


    return butterflies[0:4]


def plot_butterfly(sp):
    i = sp['info']
    print i


    s1 =i['strike_low']
    s2 =i['strike_mid']
    s3 =i['strike_high']
    p1 =-i['price_low']
    p2 =i['price_mid']
    p3 =-i['price_high']

    x_p = np.linspace(s1-1, s3+1, 200)#[i['s_low']-10,i['s_low'],i['s_mid'],i['s_high'],i['s_high']+10]
    y_p = []
    y1 = []
    y2=[]
    y3=[]

    for x in x_p:
        if x<=s1:
            y = p1
        else:
            y = p1 + (x-s1)
        y1.append(y)

        if x<=s2:
            y = 2*p2
        else:
            y = 2*p2-2*(x-s2)
        y2.append(y)

        if x<=s3:
            y = p3
        else:
            y = p3 + (x-s3)
        y3.append(y)
        y_p.append(y1[-1]+y2[-1]+y3[-1])

    plt.plot(x_p,y1)
    plt.plot(x_p,y2)
    plt.plot(x_p,y3)
    plt.plot(x_p,y_p)
    plt.plot([s1-1,s3+1],[0,0],ls='dashed')
    plt.show()


####################################################################

symb = 'IBM'
quote = web.get_quote_yahoo(symb)
price = quote.iloc[0]['last']
option_m = Options(symb,'yahoo')
print option_m.expiry_dates
ex_date = option_m.expiry_dates[1]

print ex_date
data = option_m.get_options_data(expiry=ex_date)


# Make lists of calls and puts.
in_calls = []
in_puts = []
calls = []
puts = []
for i in range(0,100):#data.iloc:
    try:
        if data.iloc[i].name[2]=='call':
            in_calls.append(i)
            calls.append(data.iloc[i]['JSON'])
        elif data.iloc[i].name[2]=='put':
            in_puts.append(i)
            puts.append(data.iloc[i]['JSON'])
    except IndexError:
        break
    except Exception as e:
        break


results = loop_iron_condor(calls,puts)

print 'N: ',len(results)

for i in range(0,len(results)):
    a= results[i]['info']
    b= results[i]['calc']

# print len(a)
    #print '\nPrices: -%.2f  %.2f   %.2f  -%.2f '%()
    min_prof = results[i]['calc']['min_profit']
    max_prof = results[i]['calc']['max_profit']

    spread = b['width']/price*100



    if spread>.1 and max_prof>.1 and min_prof>-5:


        print '\nMax Profit: %.1f    Max loss: %.1f' %(max_prof,min_prof)
        print 'strikes: %.2f   %.2f   %.2f    %.2f' %(a['strike_low'],a['strike_mid1'],a['strike_mid2'],a['strike_high'])
        print 'Spread: %.2f  percentage:  %.1f ' %(b['width'], b['width']/price*100 )



    #print ,,results[i]['calc']['max_profit']


sys.exit(1)
##########################################################################































price = quote.iloc[0]['last']
y_all = []


for call in calls:
    strike = call['strike']
    premium = call['lastPrice']
    intrin = call_intrinsic(quote,strike)
    extrin = call_extrinsic(quote,strike,premium)

    print 'Option Stike: %s Premium: %.2f  Intrinsic: %.2f  Extrinsic: %.2f' %(strike,premium,intrin,extrin)

# sys.exit(1)

for i in range(0,min(len(calls),len(puts))):
    cs = calls[i]['strike']
    call_act = calls[i]

    if abs(cs-price)>4:
        continue


    for put in puts:
        if cs==put['strike']:
            put_act = put
            break
        else:
            put_act = None

    if put_act==None:
        continue

    
    x_p = np.linspace(price*.5,price*1.5,1000)


    s1 = cs
    s2 = put_act['strike']
    p1 = -call_act['lastPrice']
    p2 = -put['lastPrice']

    print p1,p2, p1+p2, cs

    y1=[]
    y2=[]
    y_p=[]
    y_p2 = []

    for x in x_p:
        if x<=s1:
            y = p1
        else:
            y = p1 + (x-s1)
        y1.append(y)

        if x>=s2:
            y = p2
        else:
            y = p2-(x-s2)
        y2.append(y)
        y_p.append(y1[-1]+y2[-1])   
        y_p2.append(2*y1[-1]+y2[-1]) 
 
    plt.plot(x_p,y_p)
    y_all.append(y_p)
    #plt.plot(x_p,y_p2)
    #plt.plot(x_p,y1)
   # plt.plot(x_p,y2)

min_loss = y_all[0]
for yi in y_all:
    if min(yi)>min(min_loss):
        min_loss = yi

zeros = []

for i in range(5,len(min_loss)-5):
    if abs(min_loss[i-1])>abs(min_loss[i]) and abs(min_loss[i+1])>abs(min_loss[i]):
        zeros.append(x_p[i])

for zero in zeros:
    print 'Delta: %s' %((zero-price)/price * 100 )


plt.plot(x_p,min_loss,linewidth=5)


plt.plot([price,price],[-5,5],linewidth=3,ls='dashed')
plt.grid(True)
plt.show()    



#butterflys = loop_butterfly_call(calls,ex_date)

# for bf in butterflys:
#     #print '\n',bf['calc']['max_profit'],'  ',bf['calc']['min_profit'],'  ',bf['calc']['width'],'  ',bf['calc']['total_liq']
#     pp = pprint.PrettyPrinter(indent=4)
#     print '\n'
#     pp.pprint(bf['calc'])
#     pp.pprint(bf['info'])
#     plot_butterfly(bf)
# print '\n'
#print calc_butterfly_call(72,75,78, 6.1,4.1,2.6,F.expiry_dates[0])

# print butterflys[0['info']




# {u'impliedVolatility': 0.9882813671875, 
# u'lastTradeDate': 1491000550, 
# u'contractSize': u'REGULAR',
# u'lastPrice': 1.19, 
# u'contractSymbol': u'F170407C00010500',
# u'inTheMoney': True, 
# u'bid': 0.96, 
# u'ask': 1.37,
# u'volume': 5,
# u'currency': u'USD',
# u'expiration': 1491523200,
# u'percentChange': 0.0,
# u'strike': 10.5,
# u'openInterest': 7,
# u'change': 0.0}










