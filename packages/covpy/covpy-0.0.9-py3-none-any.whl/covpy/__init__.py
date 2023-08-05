import pandas as pd
import datetime
from urllib.error import HTTPError
from numpy import sort, unique, average

class DataCollector:
    def __init__(self):
        self._df = pd.DataFrame()
        self._df_date = None
        self._cases_df = None
            
    
    def __get_df__(self, lookback = 7, force_new = False):
        today = datetime.date.today() + datetime.timedelta(days=1)
        
        if (force_new or (self._df.empty or self._df_date != today)):
            for i in range(lookback):
                try:
                    day = today.strftime("%Y-%m-%d")
                    url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%s.xlsx"%day
                    self._df = pd.read_excel(url)
                    self._df.columns = map(str.lower, self._df.columns)
                    self._df.columns = self._df.columns.str.replace(' ', '')

                    self._df_date = today
                except HTTPError:
                    today -= datetime.timedelta(days=1)
        
    def get_covid19_cases(self, cumulative = False, force_new = False, perHundredThousand = False):
        self.__get_df__(force_new = force_new)
        days = sort(unique(self._df['daterep']))
        cases_df = pd.DataFrame(index = days)

        for country in unique(self._df['countriesandterritories']):
            country_df = self._df.loc[self._df['countriesandterritories'] == country][['daterep', 'cases']]
            country_df = country_df.set_index('daterep')
            population = average(self._df.loc[self._df['countriesandterritories'] == country][['popdata2018']])
            if perHundredThousand:
                country_df['cases'] =  country_df['cases'] / (population / 100000.0)
            #remove duplicate indexes
            country_df = country_df.groupby(country_df.index).agg({ 'cases':sum})
            country_df = country_df.reindex(days, fill_value = 0)
            if cumulative:
                cases_df[country] = country_df["cases"].cumsum()
            else:
                cases_df[country] = country_df["cases"]
        cases_df["World"] = cases_df[list(cases_df)].sum(axis=1)

        return cases_df
    
    def get_covid19_deaths(self, cumulative= False, force_new = False, perHundredThousand = False):

        self.__get_df__(force_new = force_new)
        days = sort(unique(self._df['daterep']))
        deaths_df = pd.DataFrame(index = days)

        for country in unique(self._df['countriesandterritories']):
            country_df = self._df.loc[self._df['countriesandterritories'] == country][['daterep', 'deaths']]
            country_df = country_df.set_index('daterep')
            population = average(self._df.loc[self._df['countriesandterritories'] == country][['popdata2018']])
            if perHundredThousand:
                country_df['deaths'] =  country_df['deaths'] / (population / 100000.0)
            #remove duplicate indexes
            country_df = country_df.groupby(country_df.index).agg({'deaths':sum })
            country_df = country_df.reindex(days, fill_value = 0)
            if cumulative:
                deaths_df[country] = country_df["deaths"].cumsum()
            else:
                deaths_df[country] = country_df["deaths"]
        deaths_df["World"] = deaths_df[list(deaths_df)].sum(axis=1)

        return deaths_df