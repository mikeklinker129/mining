import numpy as np
import matplotlib.pyplot as plt
import time as t

yrs = 20

time = range(0,yrs*365)
total= [0]*len(time)
total_interest= [0]*len(time)

d1 =[0]*len(time)
d2 = [0]*len(time)
d3 = [0]*len(time)
d4 = [0]*len(time)


debt =     [10000]# [40500,40500,55000]
rates=     [.01]# [.0586,.0531,.025]
interest=  [1000]# [3515,1059,0]

debt =     [40500,40500,55000,0]
rates=     [.0586,.0531,.025,0.025]
interest=  [3515,1059,0,0]

monthly_payment = 4000.0
dayp = monthly_payment/30.0

for day in time:


    #add interest
    for i in range(0,len(debt)):
        add_amount = (debt[i]+interest[i])*(rates[i]/365.0)
        interest[i] += add_amount

    #Payments
    curr_payment = dayp*1.0
    for i in range(0,len(debt)):
        if interest[i]>curr_payment:
            interest[i] = interest[i]-curr_payment
            break
        elif interest[i]>0:
            debt[i] = debt[i]-(curr_payment-interest[i])
            interest[i] = 0
            break
        elif debt[i]>curr_payment:
            debt[i] = debt[i]-curr_payment
            break
        elif debt[i]>0:
            curr_payment = curr_payment-debt[i]
            debt[i] = 0
            

    d1[day] = debt[0]
    d2[day] = debt[1]
    d3[day] = debt[2]
    d4[day] = debt[3]


    if sum(debt)<10:
        time = time[:day]
        total=total[:day]
        total_interest=total_interest[:day]

        d1 = d1[:day]
        d2 = d2[:day]
        d3 = d3[:day]
        d4 = d4[:day]
        print 'Monthly: %.1f  Years: %.1f' %(monthly_payment, day/365.0)
        break



    total[day] = sum(debt)+sum(interest)
    total_interest[day] = sum(interest)


plt.plot(time,total)
plt.plot(time,d1)
plt.plot(time,d2)
plt.plot(time,d3)
plt.plot(time,total_interest)
plt.ion()
plt.show()
t.sleep(5)










