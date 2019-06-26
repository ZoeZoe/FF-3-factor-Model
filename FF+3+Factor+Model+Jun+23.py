
# coding: utf-8

# In[77]:

import statsmodels.api as sm #for OLS regression
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt #for heatmap plotting
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns #for heatmap plotting
from statsmodels.iolib.summary2 import summary_col #to summarize multiple regressions in one table


# In[12]:

p25 = pd.read_csv('C:/Users/yz2991/Desktop/25_Porfolio.csv')
ff3 = pd.read_csv('C:/Users/yz2991/Desktop/3 factor.csv')


# In[13]:

#check the start and end of p25 
print(p25.head())
print(p25.tail())


# In[14]:

#check the start and end of ff3
print(ff3.head())
print(ff3.tail())


# In[15]:

#updated the field name of Year&month field
p25.rename(columns = {'Unnamed: 0': 'YYMM'}, inplace = True)
ff3.rename(columns = {'Unnamed: 0': 'YYMM'}, inplace = True)


# In[16]:

#check the column names
print(ff3.columns)
print(p25.columns)


# In[17]:

#to convert to decile format and get excess returns
ff3.iloc[:,1:ff3.shape[1]] = ff3.iloc[:,1:ff3.shape[1]]/100
p25_excess=(p25.iloc[:,1:p25.shape[1]]/100).sub(ff3.RF,axis=0)
print(p25_excess.head())


# In[18]:

#YYMM as timestamp
ff3['YYMM'] = pd.to_datetime(ff3['YYMM'],yearfirst=True, format='%Y%m')
p25_excess['YYMM'] = pd.to_datetime(p25['YYMM'],yearfirst=True, format='%Y%m')


# In[19]:


#change timestamps to index and delete unnecessary columns
ff3.index = ff3['YYMM']
p25_excess.index = p25_excess['YYMM']
ff3 = ff3.drop('YYMM', axis = 1)
p25_excess = p25_excess.drop('YYMM', axis = 1)
ff3 = ff3.drop('RF', axis = 1)


# In[20]:


#calculate average excess return for the 25 porfolios over the whole history
avg_return = p25_excess.mean(axis = 0)
avg_return = avg_return.as_matrix(columns = None)
avg_return = pd.DataFrame(avg_return.reshape((5,5)))
avg_return.rename(columns = {0:'Market Size 0', 1:'Market Size 1', 2: 'Market Size 2', 3:'Market Size 3',4:'Market Size 4'}, inplace = True) 
avg_return.rename(index = {0:'B/M 0', 1:'B/M 1', 2: 'B/M 2', 3:'B/M 3',4:'B/M 4'}, inplace = True)

print(avg_return)
type(avg_return)


# In[21]:

#plot the average excess return of 25 portfolios in a heatmap
plt.pcolor(avg_return)
plt.yticks(np.arange(0.5, len(avg_return.index), 1), avg_return.index)
plt.xticks(np.arange(0.5, len(avg_return.columns), 1), avg_return.columns)
plt.show()


# In[22]:

#create class to run OLS for 25 portfolios
class famafrench():
    def __init__(self, y, start = '1963-7-1', end = '1990-12-1'):
        self.start = start
        self.end = end
        self.y = y[start:end]
    
    def __str__(self):
        return 'from %s to %s' %(self.start, self.end)

    def variables(self):
        x = ff3[self.start:self.end]
        y = self.y[self.start:self.end]
        return x, y

    def regression(self):
        x = self.variables()[0]
        x = sm.add_constant(x)
        y = self.variables()[1]
        model = sm.OLS(y,x)
        result = model.fit()

        return result


# In[38]:

#get results from OLS
x = famafrench(p25_excess)
res = x.regression()
print(res.params)
print(dir(res))
type(res)
# res.rsquared()
# res.tvalues()
print(np.squeeze(np.array(res.rsquared)))


# In[54]:

#run OLS regresion without a class
x = ff3['1963-7-1':'1990-12-1']
x = sm.add_constant(x)
y = p25_excess['1963-7-1':'1990-12-1']
y0 = y.iloc[:, 0]


# In[56]:

reg0 = sm.OLS(y0, x)
result0 = reg0.fit()
print(result0.summary())


# In[74]:

#run OLS regessions for 25 porfolios in a loop
models = []
for i in range (25):
    reg = sm.OLS(y.iloc[:, i], x)
    models.append(reg.fit())
print(models[0].params)
print(models[0].summary())


# In[102]:

#summarize the 25 regression ouputs into one table
info_dict={'R-squared' : lambda x: f"{x.rsquared:.2f}",
           'No. observations' : lambda x: f"{int(x.nobs):d}"}
           
results_table = summary_col(results= models,
                            stars = True,
                            model_names=y.columns.tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table.add_title('Table - OLS Regressions')

print(results_table)


# In[94]:

print(y.columns[0:5])


# In[112]:

#summarize the regression output of Small-size portfolios
info_dict={'R-squared' : lambda x: f"{x.rsquared:.2f}",
           'No. observations' : lambda x: f"{int(x.nobs):d}"}
           
results_table_0 = summary_col(results= [models[0],models[1],models[2],models[3],models[4]],
                            stars = True,
                            model_names=y.columns[0:5].tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table_0.add_title('Table - Small Size - OLS Regressions')

print(results_table_0)


# In[113]:

#summarize the regression output of size-1 portfolios
results_table_1 = summary_col(results= [models[5],models[6],models[7],models[8],models[9]],
                            stars = True,
                            model_names=y.columns[5:10].tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table_1.add_title('Table - Size 1 - OLS Regressions')

print(results_table_1)


# In[115]:

#summarize the regression output of size-2 portfolios
results_table_2 = summary_col(results= [models[10],models[11],models[12],models[13],models[14]],
                            stars = True,
                            model_names=y.columns[10:15].tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table_2.add_title('Table - Size 2 - OLS Regressions')

print(results_table_2)


# In[116]:

#summarize the regression output of size-3 portfolios
results_table_3 = summary_col(results= [models[15],models[16],models[17],models[18],models[19]],
                            stars = True,
                            model_names=y.columns[15:20].tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table_3.add_title('Table - Size 3 - OLS Regressions')

print(results_table_3)


# In[118]:

#summarize the regression output of Large-eize portfolios
results_table_4 = summary_col(results= [models[20],models[21],models[22],models[23],models[24]],
                            stars = True,
                            model_names=y.columns[20:25].tolist(),
                            float_format ="%.2f",
                            info_dict = info_dict
                           )

results_table_4.add_title('Table - Large Size - OLS Regressions')

print(results_table_4)


# In[ ]:

# TAKEAWAYS:
# Almost all portfolios (except for 1) have R-square higher than 90%
# Most of the constant terms are insignificant
# All portfolios have excess returns in positive correlation with market excess return. Ususally mid-size companies have higher correlation with market excess return.
# Smaller companies have stronger positive correlation with SMB factor, which meant to mimic the risk factor in returns related to size. For the largest companies, the correlation turns negative.
# No consistent pattern is observed for HML factor across companies with different sizes
# Companies with higher B/M ratios will have stronger positive correlation with HML factor, which meant to mimic the risk factor in returns related B/M equity. For the companies with lowest B/M ratio, the correlation turns negative.
# Usually, companies with the lowest and highest B/M ratios will have stronger correlation with SMB factor.
# The last bulletpoint is intuitive as 1.low B/M ratio is usually because of high market value, thus the company is more likely to fall in the larger-size portfolios. 2. high B/M ratio is usually due to low market value, and thus the company is more likely to fall into the small-size portfolio.


# In[ ]:

# Problems to solve:
# how to run the regressions in a class and extract statistics out of it
# how to construct a better consolidated table for all the regresion reults. And how to visulize the results better.
# use up-to-date data to run regressions, and if the results are weaker, try expanding window to check the pattern.
# how to plot 3-D bars
# how to do prediction with 3-factor model

