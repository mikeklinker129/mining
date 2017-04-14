
import datetime
import numpy as np
import ast
import os




class Stock_Data_Manager():
    def __init__(self,filename):

        self.filename = 'data/%s.txt' %filename

        self.data = [] #Top of the list is the most recent information. 

        if os.path.isfile(self.filename):
            self.load_data()

        else:   
            self.create_file()

        #   Data Storage: 
        # {  'price': float,
        #     'volume': int,
        #     'time': datetime
        # }

    def create_file(self):
        with open(self.filename,'w') as wr:
            wr.write('')

    def add_line(self,price,volume,time):

        d = {}
        d['price'] = price
        d['volume']= volume
        d['time']  = time.isoformat() #datetime object

        self.data.insert(0,d)

        with open(self.filename,'a') as wr:
            wr.write(str(d)+'\n')


    def load_data(self):
        lines = [line.rstrip('\n') for line in open(self.filename,'r')]

        for line in lines:
            dic = ast.literal_eval(line)
            self.data.insert(0,dic)


