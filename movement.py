from yahoo_finance import Share
#import yahoo_finance as yh 
import numpy as np
import ast



class Stock_Movement():

    def __init__(self):

        self.watchlist = ['AMZN','F','AMD']

        self.stocks = []


    def update_prices(self):

        self.stocks = []


    def update_metrics(self):

        self.stocks = []



class Stock_Obj():
    def __init__(self,symb):
        self.symb = symb
        self.s = Share(self.symb)

        self.last_price = 0
        self.last_volume = 0
        self.last_timestamp = 0
        self.last_dataset = {}


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

        self.last_price = self.s.get_price()
        self.last_volume = self.s.get_volume()
        self.last_timestamp = self.s.get_trade_datetime()

        self.last_dataset = self.s.data_set

        self.price_list.append(self.last_price)
        self.volume_list.append(self.last_volume)
        self.ts_list.append(self.last_timestamp)

    def process_data(self):

        if len(self.last_price) < 5:
            self.valid_data = False
            return 0
        else:
            self.valid_data = True

        if self.valid_data:
            dt = (self.ts_list[-1] - self.ts_list[-2]).total_seconds()

            measure_d_p = (self.price_list[-1]-self.price_list[-2])/dt
            measure_d_v = (self.volume_list[-1]-self.volume_list[-2])/dt

            self.d_p.append(measure_d_p)
            self.d_v.append(measure_d_v)

            #Determine accel
            measure_dd_p = (self.d_p[-1]-self.d_p[-2])/dt
            measure_dd_v = (self.d_v[-1]-self.d_v[-2])/dt

            self.dd_p.append(measure_dd_p)
            self.dd_v.append(measure_dd_v)


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























            