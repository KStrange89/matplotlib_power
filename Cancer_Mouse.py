#!/usr/bin/env python
# coding: utf-8

# ## Observations and Insights
#  - On average, Ramican results in a smaller tumor volume.
#  - However, Capomulin has results that are almost as good and has a smaller variability in results.
#  - Ceftamin and Infubinol are not effective as the average tumor size increases throughout the course of the treatment for both of these drug regimens.
#  

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as sts
import numpy as np
from scipy.stats import linregress


# In[2]:


# import the data

data_path = "Mouse_metadata.csv"
results_path = "Study_results.csv"


# In[3]:


# read the data

mouse_data = pd.read_csv(data_path)
study_results = pd.read_csv(results_path)


# In[4]:


# combine the two data sets into one using the Mouse ID

combined = pd.merge(mouse_data, study_results, on = "Mouse ID", how = "outer")
combined


# In[5]:


# count the mice

num = pd.DataFrame({"Number of Mice" : [combined['Mouse ID'].nunique()]})
num.set_index('Number of Mice', inplace=True)

num


# In[6]:


# check the data for any mouse ID with duplicate time points

dups = combined.loc[combined.duplicated(subset = ['Mouse ID', 'Timepoint']), 'Mouse ID'].unique()

dups


# In[7]:


# look at duplicate mouse data

dup_data = combined.loc[combined['Mouse ID'] == 'g989']

dup_data


# In[8]:


# remove duplicate mouse data

clean = combined[~combined['Mouse ID'].isin(['g989'])].reset_index(drop = True)

clean


# In[9]:


# recount the mice

num = pd.DataFrame({"Number of Mice" : [clean['Mouse ID'].nunique()]})
num.set_index('Number of Mice', inplace=True)

num


# In[10]:


# generate a summary statistics table 
# mean, median, variance, standard deviation, SEM

tv = clean.groupby('Drug Regimen')['Tumor Volume (mm3)']

tumor_table = pd.DataFrame({
    'Mean' : tv.mean(),
    'Median' : tv.median(),
    'Variance' : tv.var(),
    'Standard Deviation' : tv.std(),
    'SEM' : tv.sem()
})

tumor_table


# In[11]:


# summary stats with aggregation

clean.groupby(['Drug Regimen'])['Tumor Volume (mm3)']    .agg(['mean', 'median', 'var', 'std', 'sem'])


# In[12]:


# bar graph one way

bg1 = tv.count().plot(kind = 'bar', color = "mediumvioletred")
bg1.set_ylabel('Measurements Taken')
bg1


# In[13]:


# bar graph two way

x_axis = np.arange(len(tumor_table))
drugs = clean['Drug Regimen'].unique()
drugs = np.sort(drugs)
tick_locations = [value for value in x_axis]
plt.xticks(tick_locations, drugs, rotation = 'vertical')
plt.xlabel('Drug Regimen')
plt.ylabel('Measurements Taken')

bg2 = plt.bar(x_axis, tv.count(), color = 'deeppink' , width = .5)


# In[35]:


# pie chart one way
gender = clean.groupby('Sex')['Mouse ID'].nunique()

pc1 = gender.plot(kind = 'pie', autopct = '%1.1f%%')
pc1


# In[36]:


# pie chart two way
sexdf = clean.groupby('Sex', as_index = False)['Mouse ID'].nunique()
sexnum = sexdf[['Mouse ID']].rename(columns = {'Mouse ID' : 'Gender'})
sn = sexnum['Gender']
sex = sexdf['Sex']

plt.pie(sn, labels = sex, autopct = '%1.1f%%')

plt.show()


# In[17]:


# get the last timepoint for each mouse

ltp = combined.loc[combined.groupby('Mouse ID')['Timepoint'].idxmax()]
ftv = ltp[['Mouse ID', 'Timepoint', 'Tumor Volume (mm3)']].reset_index(drop = True)
ftv


# In[18]:


# merge with the original dataframe to get last timepoint tumor volume

ltp_df = combined.merge(ltp)
ltp_df = ltp_df.rename(columns = {'Tumor Volume (mm3)' : 'Final Tumor Volume (mm3)'})
ltp_df


# In[19]:


capo = ltp_df[ltp_df['Drug Regimen'] == 'Capomulin']
catumvol = capo['Final Tumor Volume (mm3)']
quartiles = catumvol.quantile([.25, .5, .75])
q1 = quartiles[.25]
q3 = quartiles[.75]
iqr = q3 - q1
lowb = q1 - (iqr * 1.5)
upb = q3 + (iqr * 1.5)
print(f'The spread of the data is {round(iqr, 2)}')
print(f'The lower bound for outliers is {round(lowb, 2)}')
print(f'The upper bound for outliers is {round(upb, 2)}')
print(f'The minimum tumor volume is {round(min(capo["Final Tumor Volume (mm3)"]), 2)}')
print(f'The maximum tumor volcume is {round(max(capo["Final Tumor Volume (mm3)"]), 2)}')
print('There are no outliers here')


# In[20]:


rami = ltp_df[ltp_df['Drug Regimen'] == 'Ramicane']
rtumvol = rami['Final Tumor Volume (mm3)']
quartiles = rtumvol.quantile([.25, .5, .75])
q1 = quartiles[.25]
q3 = quartiles[.75]
iqr = q3 - q1
lowb = q1 - (iqr * 1.5)
upb = q3 + (iqr * 1.5)
print(f'The spread of the data is {round(iqr, 2)}')
print(f'The lower bound for outliers is {round(lowb, 2)}')
print(f'The upper bound for outliers is {round(upb, 2)}')
print(f'The minimum tumor volume is {round(min(rami["Final Tumor Volume (mm3)"]), 2)}')
print(f'The maximum tumor volcume is {round(max(rami["Final Tumor Volume (mm3)"]), 2)}')
print('There are no outliers here')


# In[21]:


infu = ltp_df[ltp_df['Drug Regimen'] == 'Infubinol']
itumvol = infu['Final Tumor Volume (mm3)']
quartiles = itumvol.quantile([.25, .5, .75])
q1 = quartiles[.25]
q3 = quartiles[.75]
iqr = q3 - q1
lowb = q1 - (iqr * 1.5)
upb = q3 + (iqr * 1.5)
print(f'The spread of the data is {round(iqr, 2)}')
print(f'The lower bound for outliers is {round(lowb, 2)}')
print(f'The upper bound for outliers is {round(upb, 2)}')
print(f'The minimum tumor volume is {round(min(infu["Final Tumor Volume (mm3)"]), 2)}')
print(f'The maximum tumor volcume is {round(max(infu["Final Tumor Volume (mm3)"]), 2)}')
print('There are potential outliers')


# In[22]:


# find the mouse who is the outlier

outlier_mouse = infu[infu['Final Tumor Volume (mm3)'] < lowb]
outlier_mouse


# In[23]:


ceft = ltp_df[ltp_df['Drug Regimen'] == 'Ceftamin']
cetumvol = ceft['Final Tumor Volume (mm3)']
quartiles = cetumvol.quantile([.25, .5, .75])
q1 = quartiles[.25]
q3 = quartiles[.75]
iqr = q3 - q1
lowb = q1 - (iqr * 1.5)
upb = q3 + (iqr * 1.5)
print(f'The spread of the data is {round(iqr, 2)}')
print(f'The lower bound for outliers is {round(lowb, 2)}')
print(f'The upper bound for outliers is {round(upb, 2)}')
print(f'The minimum tumor volume is {round(min(ceft["Final Tumor Volume (mm3)"]), 2)}')
print(f'The maximum tumor volcume is {round(max(ceft["Final Tumor Volume (mm3)"]), 2)}')
print('There are no outliers here')


# In[24]:


# filter to get only the drug regimens we want:
# Capomulin, Ramicane, Infubinol, and Ceftamin

dr = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']

drug_df = ltp_df[ltp_df['Drug Regimen'].isin(dr)]
drug_df = drug_df[['Drug Regimen', 'Final Tumor Volume (mm3)']]
drug_df


# In[25]:


boxplot = drug_df.boxplot(column = ['Final Tumor Volume (mm3)'],                           by = 'Drug Regimen', )
plt.suptitle('')
plt.tight_layout
plt.show()


# In[26]:


# create a dataframe of just Capomulin for the remaining steps

cap_df = combined[combined['Drug Regimen'] == 'Capomulin']
cap_df


# In[27]:


# line graph for Mouse ID i557, a mouse treated with Capomulin

i557_df = cap_df[cap_df['Mouse ID'] == 'i557']
i557_df

i557 = i557_df.plot.line(x = 'Timepoint', y = 'Tumor Volume (mm3)')


# In[28]:


ram_df = combined[combined['Drug Regimen'] == 'Ramicane']
cef_df = combined[combined['Drug Regimen'] == 'Ceftamin']
inf_df = combined[combined['Drug Regimen'] == 'Infubinol']
ram_df


# In[29]:


# I know this wasn't asked for. But I think a graph that compares average tumor size of all Capomulin 
# mice at each time point would be much more valuable to researchers than just the one mouse
# I then decided to look at the four drug regimens we care about and do the same thing and plot them on the same graph 
# for comparison's sake

capavtumsize = cap_df.groupby('Timepoint')['Tumor Volume (mm3)'].mean()
ramavtumsize = ram_df.groupby('Timepoint')['Tumor Volume (mm3)'].mean()
cefavtumsize = cef_df.groupby('Timepoint')['Tumor Volume (mm3)'].mean()
infavtumsize = inf_df.groupby('Timepoint')['Tumor Volume (mm3)'].mean()

capavtumsize_plot = capavtumsize.plot.line(label = 'Capomulin')
ramavtumsize_plot = ramavtumsize.plot.line(label = 'Ramicane')
cefavtumsize_plot = cefavtumsize.plot.line(label = 'Ceftamin')
infavtumsize_plot = infavtumsize.plot.line(label = 'Infubinol')

plt.ylabel('Average Tumor Volume')
plt.tight_layout
plt.legend()
plt.show()


# In[30]:


# get average mouse weight and average tumor volume


atvcap = cap_df.groupby('Mouse ID')['Tumor Volume (mm3)'].mean()
amwcap = cap_df.groupby('Mouse ID')['Weight (g)'].mean()

cap_scatter = pd.DataFrame({
    'Average Tumor Volume (mm3)' : atvcap,
    'Average Weight (g)' : amwcap
})


# In[31]:


# scatter plot of average tumor volume vs. mouse weight for Capomulin

x_values = cap_scatter['Average Weight (g)']
y_values = cap_scatter['Average Tumor Volume (mm3)']

#find the values for the regression line
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)

#y = mx + b
regress_values = slope * x_values + intercept

# find correlation
correlation = sts.pearsonr(x_values, y_values)

plt.scatter(x_values, y_values)
plt.plot(x_values, regress_values, "r-")
plt.xlabel('Average Weight(g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.show()
print(f'The correlation between average mouse weight and average tumor volume with the Capomulin treatment is {round(correlation[0], 2)}')

