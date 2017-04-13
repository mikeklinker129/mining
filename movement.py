from yahoo_finance import Share
#import yahoo_finance as yh 
import numpy as np
import ast
import time
import datetime
from dateutil import parser
import matplotlib.pyplot as plt


class Stock_Movement():

    def __init__(self):

        self.watchlist = ['AMZN','F']
        self.stocks = []

        for symb in self.watchlist:
            self.stocks.append(Stock_Obj(symb))

        


    def update_prices(self):

        for stock in self.stocks:
            stock.pull_data()


    def update_metrics(self):

        for stock in self.stocks:
            stock.process_data()



class Stock_Obj():
    def __init__(self,symb):
        self.symb = symb
        self.s = Share(self.symb)

        self.last_price = 0
        self.last_volume = 0
        self.last_timestamp = 0
        self.last_dataset = {}

        self.bb_avg = []
        self.bb_low = []
        self.bb_high = []


        self.price_list = []
        self.volume_list = []
        self.ts_list = []
        
        self.pull_data()

        #Calculated Metrics:
        self.d_p = [] #Velocity of price
        self.dd_p = []#Acceleration of price

        self.d_v = []#Velocity of volume
        self.dd_v = []#Accel of price

        self.valid_data = False


    def pull_data(self):

        self.s.refresh()

        self.last_price = float(self.s.get_price())
        self.last_volume = float(self.s.get_volume())
        self.last_timestamp = parser.parse(self.s.get_trade_datetime())

        self.last_dataset = self.s.data_set

        self.price_list.append(self.last_price)
        self.volume_list.append(self.last_volume)
        self.ts_list.append(self.last_timestamp)

        print "Symb: %s, Price: %.2f" %(self.symb, float(self.last_price))

    def process_data(self):

        if len(self.price_list) < 5:
            self.valid_data = False
            self.d_p.append(0)
            self.d_v.append(0)
            self.dd_p.append(0)
            self.dd_v.append(0)
            return 0
        else:
            self.valid_data = True

            # VELOCITY AND ACCEL
        if self.valid_data:
            dt = (self.ts_list[-1] - self.ts_list[-2]).total_seconds()

            if self.ts_list[-1] == self.ts_list[-2]:
                self.d_p.append(0)
                self.d_v.append(0)
                self.dd_p.append(0)
                self.dd_v.append(0)
            else:
                measure_d_p = (self.price_list[-1]-self.price_list[-2])/dt
                measure_d_v = (self.volume_list[-1]-self.volume_list[-2])/dt

                self.d_p.append(measure_d_p)
                self.d_v.append(measure_d_v)

                #Determine accel
                measure_dd_p = (self.d_p[-1]-self.d_p[-2])/dt
                measure_dd_v = (self.d_v[-1]-self.d_v[-2])/dt

                self.dd_p.append(measure_dd_p)
                self.dd_v.append(measure_dd_v)

        if len(self.price_list)>6:
            self.bbands()
            self.plot_bbands()


    def bbands(self,N=5,numsd=2):
        p = np.array(self.price_list[-N:])

        avg = np.mean(p)
        std = np.std(p)

        upband = avg + (std*numsd)
        dnband = avg - (std*numsd)

        self.bb_avg.append(np.round(avg,2))
        self.bb_low.append(np.round(dnband,2))
        self.bb_high.append(np.round(upband,2))

    def plot_bbands(self):
        try:
            plt.clear()
        except:
            pass

        plt.plot(self.bb_avg)
        plt.plot(self.bb_high)
        plt.plot(self.bb_low)
        plt.show()


    def log_data(self):

        output = {}
        output['price_list'] = self.price_list
        output['volume_list'] = self.volume_list
        output['ts_list'] = ts_list

        try:
            outfile = 'data/%s.txt' %self.symb
            with open(outfile,'w') as w:
                w.write(str(output))
        except Exception as e:
            print 'Error logging data: %s' %e


    def load_data(self):
        try:
            infile = 'data/%s.txt' %self.symb
            with open(infile,'r') as r:
                raw = r.read()
                data = ast.literal_eval(raw)

            self.price_list = data['price_list']
            self.volume_list = data['volume_list']
            self.ts_list = data['ts_list']

        except Exception as e:
            print 'Error loading data: %s' %e


stock = Stock_Movement()


while True:
    time.sleep(3)
    stock.update_prices()
    stock.update_metrics()


















            