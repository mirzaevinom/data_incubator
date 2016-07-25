
"""
Author: Inom Mirzaev

Right now number of trials is set to 10^5, which gives couple of digits of accuracy.
This takes 4-5 minutes on a desktop machine. For more accuracy you need to set the number 
of trials higher. I got my answers with 10^7 on a supercomputer.
"""
from __future__ import division

import numpy as np

import time, os, cPickle

start = time.time()

#Possible jumps at each key
jumps = [ [4,6] , [6,8] , [7,9] , [4,8] , [0,3,9] , [] , [0 , 1 , 7 ] , [2,6] , [1,3] , [2,4] ]


def mean_std_prob( num_jumps , mod, prob_num, cond_num, trials=10**4):
    
    #Array storing key sums, S
    myarr = np.zeros( trials )
    
    for nn in xrange( len( myarr) ):
        
        key = 0
        key_sum = 0
        
        for mm in xrange(num_jumps):
            key = np.random.choice( jumps[key] )
            key_sum += key
        
        myarr[nn] =  key_sum
    #Indice of S divisible by conditional number
    indice = np.nonzero( np.mod( myarr, cond_num )==0 )
    
    #Ratio of trials divisible by prob_num given that S is divisible by cond_num
    prob = np.sum( np.mod( myarr[ indice ] , prob_num )==0 ) / np.sum(np.mod( myarr, cond_num )==0)  
    
    return np.mean( np.mod( myarr , mod ) ) , np.std( np.mod( myarr , mod ) ) , prob   

ans10 = mean_std_prob( 10 , 10 , 5, 7)


ans1024 = mean_std_prob( 1024 , 1024 , 23 , 29 )
"""

data_dict = {'ans10':ans10, 'ans1024': ans1024}

fname = 'knight_'+ time.strftime( "%H_%M" , time.localtime() ) +'.pkl'  

output_file = open( fname  , 'wb')
cPickle.dump(data_dict, output_file)

output_file.close()


r_ans10 =  np.load('mean_std_prob_10.npy')
r_ans1024 =  np.load('mean_std_prob_1024.npy')

print 'T=10, (Mean, Standard Deviation, Probability) =' , r_ans10
print 'T=1024, (Mean, Standard Deviation, Probability) =' , r_ans1024

fnames = []
for file in os.listdir(os.curdir):
    if file.startswith("knight") and file.endswith('pkl'):
        fnames.append(file)
        
        
for mm in range(len(fnames)):
    
    myfile = fnames[mm]
    
    pkl_file = open(myfile , 'rb')
    
    data_dict = cPickle.load( pkl_file )
    print 'Relativce error for mod 10' , np.abs( r_ans10 - data_dict['ans10'] )
    print 'Relativce error for mod 1024' , np.abs( r_ans1024 - data_dict['ans1024'] )    
    pkl_file.close()"""


end = time.time()

print 'Time elapsed', round( (end - start) / 60, 2) , 'minutes'
