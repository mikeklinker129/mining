import pandas_datareader.data as web
import datetime as dt
import numpy as np 
import matplotlib.pyplot as plt





# def Bolinger_Bands(stock_price, window_size, num_of_std):

#     rolling_mean = stock_price.rolling(window=window_size).mean()
#     rolling_std  = stock_price.rolling(window=window_size).std()
#     upper_band = rolling_mean + (rolling_std*num_of_std)
#     lower_band = rolling_mean - (rolling_std*num_of_std)

#     return rolling_mean, upper_band, lower_band

def bbands(price, length=30, numsd=2):
    """ returns average, upper band, and lower band"""
    #ave = pd.stats.moments.rolling_mean(price,length)
    ave = price.rolling(length, center=False).mean()
    # sd = pd.stats.moments.rolling_std(price,length)
    sd = price.rolling(length,center=False).std()
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

def main():

    start, end = dt.datetime(2016, 9, 1), dt.datetime(2017, 4, 10)
    sp = web.DataReader('JNUG','yahoo', start, end) 

    #sp['ave'], sp['upper'], sp['lower'] = bbands(sp.Close, length=30, numsd=1)
    avg,upper,lower = bbands(sp.Open, length=15, numsd=1)
    #sp= sp[-200:]


    plt.plot(avg)
    plt.plot(upper)
    plt.plot(lower)
    plt.plot(sp.Close)
    plt.show()



    # sp.plot()

main()

# data_ext.all_stock_df.plot(x='Date', y=['Adj Close','20d_ma','50d_ma','Bol_upper','Bol_lower' ])
# data_ext.all_stock_df.plot(x='Date', y=['Bol_BW','Bol_BW_200MA' ])
#         plt.show()

    # price_series = get_data(ticker, dates) # it is a Pandas series...

    # rolling_avg_price, upper_band, lower_band = Bolinger_Bands(price_series, 20, 2)

    # do_other_processing(rolling_avg_price, upper_band, lower_band)