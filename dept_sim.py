import numpy as np
import matplotlib.pyplot as plt
import time

yrs = 7

time = range(0,yrs*365)
total= [0]*len(time)



debt =     [10000]# [40500,40500,55000]
rates=     [.01]# [.0586,.0531,.025]
interest=  [1000]# [3515,1059,0]

debt =     [40500,40500,55000]
rates=     [.0586,.0531,.025]
interest=  [3515,1059,0]

monthly_payment = 2000.0
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
        


    if sum(debt)<10:
        break



    total[day] = sum(debt)+sum(interest)


plt.plot(time,total)
plt.ion()
plt.show()










