import datetime
from dateutil import parser
import numpy as np
import ast
import os
import sys

from yahoo_finance import Share

from data_manager import Stock_Data_Manager()

class Stock_Object():
    def __init__(self, symb):
        self.symb   = symb
        self.s      = Share(symb)   
        self.sdm    = Stock_Data_Manager(symb) #Data Manager
        self.d      = self.sdm.data



    def update(self): #PULL NEW DATA
        try:
            self.s.refresh()
            p = np.round(float(self.s.get_price()),3)
            v = int(self.s.get_volume())
            t = parser.parse(self.s.get_trade_datetime())
            self.sdm.add_line(p,v,t)
            self.d = self.sdm.data
        except Exception as e:
            print 'Update Failed: %s' %e


    def ma(self,t_window): #MOVING AVERAGE
        #t_window = minutes
        sump = 0
        count = 0
        start = parser.parse(self.d[0]['time'])
        for dp in self.d:
            stop = dp['time']
            if self.dt_min(start,stop)>=t_window:
                break
            else:
                sump += dp['price']
                count++

        moving_avg = sump/count

        return moving_avg


    def velp(self,t_window): #VELOCITY PRICE


    def accelp(self,t_window): #ACCEL PRICE


    def velv(self,t_window): # VELOCITY VOLUME
        

    def accelv(self,t_window): #ACCEL VOLUME



    def ekf(self):

        #predict
        x_k = f(x_km1) # predicted state given my last state
        P_k = F_km1 * P_km1 * F_km1 + Q_km1

        #update
        y_k = #measurement - predicted measurement
        S_k = H*P_k*H + R 
        K_k = P_k * H / S_k

        x = x_k + K_k * y_k
        P = (1-K_k*H) * P_k
 







###################################################################

    def dt_min(self,start,stop):
        dt =(stop-start).total_seconds()/60
        return np.round(dt,2)

    def dt_sec(self,start,stop):
        dt =(stop-start).total_seconds()
        return np.round(dt,2)

