#!/usr/bin/env python
# coding: utf-8

# In[3]:


import statsmodels.api as sm
import numpy as np
import pandas as pd


# In[33]:


p25 = pd.read_csv('C:/Users/yzou/Desktop/25_Porfolio.csv')


# In[34]:


p25.head()


# In[35]:


p25.tail()


# In[36]:


p25.index


# In[37]:


p25.columns


# In[38]:


p25.info()


# p25.columns[1] 

# In[39]:


p25.rename(columns = {'Unnamed: 0': 'YYMM'}, inplace = True)


# In[40]:


p25.columns


# In[83]:


ff3 = pd.read_csv('C:/Users/yzou/Desktop/3 factor.csv')


# In[42]:


ff3.head()


# In[43]:


ff3.tail()


# In[44]:


ff3.info()


# In[84]:


ff3.rename(columns = {'Unnamed: 0': 'YYMM'}, inplace = True)


# In[59]:


ff3.columns


# In[75]:


ff3.iloc[:,1:ff3.shape[1]] = ff3.iloc[:,1:ff3.shape[1]]/100
p25_excess=(p25.iloc[:,1:p25.shape[1]]/100).sub(ff3.RF,axis=0)


# In[76]:


ff3.head()


# In[77]:


p25_excess.head()


# In[78]:


ff3.index


# In[92]:


ff3['YYMM'] = pd.to_datetime(ff3['YYMM'],yearfirst=True, format='%Y%m')
p25_excess['YYMM'] = pd.to_datetime(p25['YYMM'],yearfirst=True, format='%Y%m')


# In[93]:


ff3.index = ff3['YYMM']
p25_excess.index = p25_excess['YYMM']


# In[96]:


p25_excess.index[1]


# In[143]:


class famafrench(object):
    def _init_(self, y = p25_excess, start = '1963-7-1', end = '1990-12-1'):
        self.start = start
        self.end = end
        self.y = y[start:end]
    
    def _str_(self):
        return 'from %s to %s' %(self.start, self.end)

    def variables(self):
        x = ff3[self.start:self.end]
        y = self.y[self.start:self.end]
        return x, y

    def regression(self):
        x = self.variables()[0]
        x = sm.add_constant(X)
        y = self.variables()[1]
        model = sm.OLS(Y,X)
        result = model.fit()
        return result
        print(result.params())


# In[144]:


parameters = famafrench()


# In[145]:


parameters


# In[ ]:




