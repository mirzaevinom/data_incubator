"""
Author: Inom Mirzaev

It takes about 2-3 minutes for this code to run. For ellipse approximation, 
I used PCA with one standard deviation as instucted. However,
I feel like, two standard deviations would give better accuracy.
"""
from __future__ import division


import numpy as np
import pandas as pd

import statsmodels.api as sm

import time

start = time.time()

prop_data = pd.read_csv('Historic_Secured_Property_Tax_Rolls.csv')

df = prop_data.sort( columns=[  'Block and Lot Number', 
                               'Closed Roll Fiscal Year' ,
                               'Closed Roll Assessed Improvement Value'] , 
                     ascending=False  )


#==============================================================================
# Fraction of assessments for properties of the most common class
#==============================================================================

com_prop = df.groupby('Property Class Code').size().values

print 'Fraction of assessments for properties of the most common class', np.max(com_prop) / df.shape[0]



#==============================================================================
# Median assessed improvement value
#==============================================================================

latest = df.groupby('Block and Lot Number').first()

latest_aiv = latest['Closed Roll Assessed Improvement Value'].values

latest_aiv = latest_aiv[latest_aiv>0]


print 'Median assessed improvement value, considering only non-zero assessments', np.median( latest_aiv) 


#==============================================================================
# Difference between the greatest and least average values
#==============================================================================
nbrhd_mean = latest.groupby('Neighborhood Code')['Closed Roll Assessed Improvement Value'].mean().values

print 'Difference between the greatest and least average values' , np.max(nbrhd_mean) - np.min( nbrhd_mean )



#==============================================================================
#  Average yearly growth rate
#==============================================================================

def ols_res(df, xcols,  ycol):
    """Function to be used with apply method of dataframe.
    Returns the slope of semi-log fit"""
    
    return sm.OLS( np.log( df[ycol] ) ,  df[xcols] ).fit().params[0]
    

mask = df['Closed Roll Assessed Land Value'].isin([0])

lin_reg = df[~mask].groupby('Block and Lot Number').apply(ols_res, xcols='Closed Roll Fiscal Year' , ycol='Closed Roll Assessed Land Value')    

print 'Yearly growth rate of Land Values over the years: average by property', lin_reg.mean()



#==============================================================================
# Largest Neighborhood
#==============================================================================

#Radius of earth in kilometers
e_rad = 6371

loc  = latest['Location']

#Parse the strings into floating point numbers

str_loc = loc.str[1:-1].str.split(', ')
lat = np.pi*( np.float_( str_loc.str[0]) - np.float(str_loc.str[0][0] ) ) / 180
lon = np.pi*( np.float_( str_loc.str[1]) - np.float(str_loc.str[1][0] ) ) / 180


#Convert latitude and longitude into 3D coordinates

x = e_rad * np.cos( lat ) * np.cos( lon )
y = e_rad * np.cos( lat ) * np.sin( lon )
z = e_rad * np.sin( lat )


loc_df = pd.DataFrame({'Neighborhood Code': latest['Neighborhood Code'] , 
                       'x': x , 
                       'y': y , 
                       'z' : z })
                       
                                           
loc_df = loc_df.dropna()      

def ellipse_area( df , xcol, ycol ):                                                 
    """ Using Principal component analysis returns area of ellipsoid """                      
    data_raw = np.asarray( df[ [xcol, ycol] ] )                                                                             
    # obtain the means                                                            
    mu = np.mean(data_raw,axis=0)                                                 
    
    # center the data                                                             
    data_c = data_raw - mu                                                        
                                                            
    # obtain the eigensystem                                                    
    evals, evecs = np.linalg.eigh( np.dot( data_c.T, data_c ) )                      
    
    # rotate the centered data to the body frame                                                 
    data_rc = np.inner( data_c , evecs.T )
                                             
    # compute the axes lenghts                                                  
    axes = np.std( data_rc , axis=0 ) 
                                                                                            
    return np.pi * np.prod(axes)

ngbrhd_area = loc_df.groupby('Neighborhood Code').apply( ellipse_area , xcol='y' , ycol='z' )

print 'Largest neighborhood area' , ngbrhd_area.max()   

n_name = df[df['Neighborhood Code']== ngbrhd_area.argmax()]['Neighborhood Code Definition'].values[0]

print 'Largest neighborhood name' , n_name


#==============================================================================
# Difference between the average number of units
#==============================================================================

mu = df['Year Property Built'].mean()
sigma = df['Year Property Built'].std()

#Select rows with reasonable years
reas_years = df[ ( df['Year Property Built'] > mu - 3*sigma ) & ( df['Year Property Built'] < 2016 ) ]

mask = reas_years['Number of Units'].isin([0])
reas_years = reas_years[~mask]
reas_years = reas_years.sort( columns=[  'Block and Lot Number', 
                               'Closed Roll Fiscal Year'] ).groupby('Block and Lot Number').first()



avg_bef_1950 = reas_years[ reas_years['Year Property Built']<1950 ]['Number of Units'].mean()
avg_aft_1950 = reas_years[ reas_years['Year Property Built']>=1950 ]['Number of Units'].mean()

print 'Difference between the average number of units', avg_aft_1950 - avg_bef_1950

#==============================================================================
# Ratio in the zip code where it achieves its maximum
#==============================================================================

zip_bed_mean = reas_years.groupby('Zipcode of Parcel')['Number of Bedrooms'].mean()
zip_unit_mean = reas_years.groupby('Zipcode of Parcel')['Number of Units'].mean()
ratio_mean = zip_bed_mean / zip_unit_mean

print 'Ratio in the zip code where it achieves its maximum' ,  ratio_mean.max() 

#==============================================================================
# Largest ratio of property area to surface area of all zip codes
#==============================================================================


mask = reas_years['Lot Area'].isin([0])
reas_years = reas_years[~mask]

zip_lot_area = reas_years.groupby('Zipcode of Parcel')['Lot Area'].sum()

zip_prop_area = reas_years.groupby('Zipcode of Parcel')['Property Area in Square Feet'].sum()

prop_ratio = zip_prop_area / zip_lot_area

print 'Largest ratio of property area to surface area of all zip codes'  , prop_ratio.max()
print 'The most built-up zip code', int(prop_ratio.argmax())


end = time.time()

print 'Time elapsed', round( (end - start) / 60, 2) , 'minutes'
