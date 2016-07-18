from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt


del_data = pd.read_csv('airline_delay_causes.csv')

city_names = del_data.groupby('airport_name')['airport_name'].first()

flag = True
while flag==True:
    city = raw_input("Please enter connecting city: ")
    src_res = city_names[ city_names.str.contains( city , case=False) ]
    
    if len(src_res)==0:
        print 'City not found please search again'
    if len(src_res)==1:
        city =  src_res[0]
        print 'Your connecting city: ', city 
        flag=False
    if len(src_res)>1:
        for nn in range( len(src_res) ):
            print str(nn) + '.', src_res[nn]
            
        num = raw_input('Select your connecting city:')
        city = src_res[int(num)]
        print 'Your connecting city: ', city     
        flag=False

del_data = del_data[ del_data[ 'airport_name' ] == city ]

flag = True
while flag==True:
        
    car_names = del_data.groupby('carrier_name')['carrier_name'].first()
    airline = raw_input("Please enter the airline you are arriving at the connecting city: ")
    
    src_res = car_names[ car_names.str.contains( airline , case=False) ]
    
    if len(airline)==0:
        print 'Airline not found please search again'
    if len(src_res)==1:
        airline = src_res[0]  
        print 'Your airline: ', airline
        flag=False
        
    if len(src_res)>1:
        for nn in range( len(src_res) ):
            print str(nn) + '.', src_res[nn]            
        num = raw_input('Select your airline:')
        airline = src_res[int(num)] 
        print 'Your airline: ', airline  
        flag=False
        
del_data = del_data[ del_data[ 'carrier_name' ] == airline ]


def group_div( df, xcol, ycol):

    return df[xcol].sum() / df[ycol].sum() 

    
del_prob_year = 100*del_data.groupby(' month').apply( group_div , xcol='arr_del15' , ycol='arr_flights')


month = raw_input("Month you are arriving at "+city+": ")

del_data = del_data[ del_data[ ' month' ] == int(month) ]    

del_prob_month = 100*del_data.groupby('year').apply( group_div , xcol='arr_del15' , ycol='arr_flights')


plt.close('all')

plt.figure(0)
del_prob_year.plot(kind='bar', color='green', alpha=0.8)
plt.ylabel('Chance of at least 15min delay in %')

plt.figure(1)

del_prob_month.plot( color='blue', linewidth=2)
plt.ylabel('Chance of at least 15min delay in %')

