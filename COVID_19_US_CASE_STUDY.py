'''
Step 1: Importing Data
'''
#Import the required libraries
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Import data
cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

#Have a look at the data:
print(cases.head())
print(deaths.head())
'''
Step 2: Data Cleanup and Transformation
'''
#Filtering data for "California" city only
cases_CA = cases[cases["Province_State"] == "California"]
cases_CA.head()

#Transposing the data set (make the rows columns, and the columns rows)
cases_CA_indexed = cases_CA.set_index("Admin2")
cases_CA_T = cases_CA_indexed.T

print(cases_CA_T)

#Remove the unnecessary columns
cases_clean = cases_CA_T.drop(['UID','iso2','iso3','code3','FIPS','Province_State','Country_Region','Lat','Long_','Combined_Key'])

#Do the same for the deaths dataset
deaths_clean = deaths[deaths["Province_State"] == "California"].set_index("Admin2").T.drop(['UID','iso2','iso3','code3','FIPS','Province_State','Country_Region','Lat','Long_','Combined_Key']).drop("Population",axis=0)

#Create a list foe the 4 counties
counties = ['Alameda',
           'San Francisco',
           'San Mateo',
           'Santa Clara']

plot = cases_clean[counties].plot(figsize=(20,10))
plot.set_title("COVID-19 cases in Bay Area Counties")

plot = deaths_clean[counties].plot(figsize=(20,10))
plot.set_title("COVID-19 deaths in Bay Area Counties")
plt.show()

'''
Revisit step 2: including rolling averages of new cases/deaths and data per milion inhabitants
'''
#diff: difference
cases_diff = cases_clean.diff().rolling(window=7).mean()
deaths_diff = deaths_clean.diff().rolling(window=7).mean()
#pop: population
pop = pd.read_csv('https://gist.githubusercontent.com/NillsF/7923a8c7f27ca98ec75b7e1529f259bb/raw/3bedefbe2e242addba3fb47cbcd239fbed16cd54/california.csv')
pop.head(10)

#Remove the word county from all columns
pop["CTYNAME"] = pop["CTYNAME"].str.replace(" County", "")
pop.head(10)

#No need for GrowthRate column
pop2 = pop.drop('GrowthRate', axis=1).set_index('CTYNAME')
pop2.head(10)

#Adjust the numbers in the cases and death dataframes:
#pm: per milion 

cases_pm = cases_clean.copy()
for c in pop2.index.tolist():
    cases_pm[c] = cases_pm[c]/pop2.loc[c , : ]['Pop']    
cases_pm = cases_pm*1000000

deaths_pm = deaths_clean.copy()
for c in pop2.index.tolist():
    deaths_pm[c] = deaths_pm[c]/pop2.loc[c , : ]['Pop']
deaths_pm = deaths_pm*1000000

cases_pm_diff = cases_pm.diff().rolling(window=7).mean()
deaths_pm_diff = deaths_pm.diff().rolling(window=7).mean()
plot = cases_diff[counties].plot(figsize=(20,10))
plot.set_title("7 day moving avg of new COVID-19 cases")
plt.show()

plot = cases_pm.sort_values(axis=1,by='7/20/20',ascending=False).iloc[:, : 10].plot(figsize=(20,10))
plot.set_title("Top 10 counties by COVID-19 cases per milion inhabitanys")
plt.show()

plot = deaths_pm.sort_values(axis=1,by='7/20/20',ascending=False).iloc[:, : 10].plot(figsize=(20,10))
plot.set_title("Top 10 counties by COVID-19 deaths per milion inhabitanys")
plt.show()

plot = deaths_pm_diff.sort_values(axis=1,by='7/20/20',ascending=False).iloc[:, : 10].plot(figsize=(20,10))
plot.set_title("Top 10 counties by 7 days rolling avg COVID-19 deaths per milion inhabitanys")
plt.show()
















