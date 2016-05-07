import numpy as np
import pandas
import statsmodels.formula.api as smf

# import the csv file into pandas
yelp = pandas.read_csv('Prepped Data/output.csv', sep=',')

# print the first few rows to check the data
print(yelp.head(5))

# check the variable types and change as necessary
print(yelp.dtypes)

# a simple example of how to do a linear regression
model = smf.ols(formula='stars ~ np.log(review_count) + np.log(Price_Range) + np.log(Number_of_Checkins + 1) +'
                        'Number_of_Tip_Likes + C(Alcohol) + Outdoor_Seating + Take_Out +'
                        'Good_for_Groups + Waiter_Service + C(Wi_Fi) + C(Attire)', data=yelp)

# print the model results
res = model.fit()
print(res.summary())
