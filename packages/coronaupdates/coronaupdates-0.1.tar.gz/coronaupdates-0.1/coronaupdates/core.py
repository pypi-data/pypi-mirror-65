'''Scraping Covid19 informations and dividing into world, countries and continents.'''
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Covid19:
    '''Gets Covid19 data and divides geographically.'''

    def __init__(self):
        '''Scrape the website text from Worldometer.'''

        self.response = requests.get(
            'https://www.worldometers.info/coronavirus/?').text

    def get_cleaned_data(self):
        '''Get the cleaned table data from Worldometer by removing HTML tags.'''
        soup = BeautifulSoup(self.response, 'lxml')
        table_content = soup.find(
            'table',
            {
                'id': 'main_table_countries_today'
            }
        )

        data = []
        for row_data in table_content.findAll('tr'):

            cleaned_row_data = []

            for cell_data in row_data.text.split('\n'):
                cleaned_row_data.append(cell_data)

            data.append(cleaned_row_data)

        return data

    def get_country_dataframe(self):
        '''Get the country wise dataframe related to CoViD-19 with various categories available.'''

        cleaned_data = self.get_cleaned_data()

        # We found that country wise data starts from 9th i.e [8:-8] row of table.
        countries_data = cleaned_data[8:-8]

        # Available columns of data.
        country_columns = [
            'blank',
            'country',
            'total_cases',
            'new_cases',
            'total_deaths',
            'new_deaths',
            'total_recovered',
            'active_cases',
            'critical_cases',
            'cases_per_million',
            'deaths_per_million',
            'total_test',
            'tests_per_million',
            'continent',
            'after_blank'
        ]

        # Creating the list for storing column wise data which will be
        # helpful for creating the Dataframe object.
        country_data_lists = {
            'first_blank': [],
            'country_name': [],
            'total_cases': [],
            'new_cases': [],
            'total_deaths': [],
            'new_deaths': [],
            'total_recovered': [],
            'active_cases': [],
            'critical_cases': [],
            'cases_per_million': [],
            'deaths_per_million': [],
            'total_test': [],
            'tests_per_million': [],
            'continent': [],
            'final_blank': [],
        }

        # Adding each columns data to the list for creating Dataframe object.
        for country_data in countries_data:
            country_data_lists['first_blank'].append(country_data[0])
            country_data_lists['country_name'].append(country_data[1])
            country_data_lists['total_cases'].append(country_data[2])
            country_data_lists['new_cases'].append(country_data[3])
            country_data_lists['total_deaths'].append(country_data[4])
            country_data_lists['new_deaths'].append(country_data[5])
            country_data_lists['total_recovered'].append(country_data[6])
            country_data_lists['active_cases'].append(country_data[7])
            country_data_lists['critical_cases'].append(country_data[8])
            country_data_lists['cases_per_million'].append(country_data[9])
            country_data_lists['deaths_per_million'].append(country_data[10])
            country_data_lists['total_test'].append(country_data[11])
            country_data_lists['tests_per_million'].append(country_data[12])
            country_data_lists['continent'].append(country_data[12])
            country_data_lists['final_blank'].append(country_data[14])

        # Creating dictionary like : {column_name: list_of_column_data}
        country_data = {
            country_columns[1]: country_data_lists['country_name'],
            country_columns[2]: country_data_lists['total_cases'],
            country_columns[3]: country_data_lists['new_cases'],
            country_columns[4]: country_data_lists['total_deaths'],
            country_columns[5]: country_data_lists['new_deaths'],
            country_columns[6]: country_data_lists['total_recovered'],
            country_columns[7]: country_data_lists['active_cases'],
            country_columns[8]: country_data_lists['critical_cases'],
            country_columns[9]: country_data_lists['cases_per_million'],
            country_columns[10]: country_data_lists['deaths_per_million'],
            country_columns[11]: country_data_lists['total_test'],
            country_columns[12]: country_data_lists['tests_per_million'],
            country_columns[13]: country_data_lists['continent'],
        }

        # Creating Dataframe object and slicing blank columns.
        country_df = pd.DataFrame(country_data, columns=country_columns[1:-2])
        return country_df

    def get_continent_dataframe(self):
        '''Get continent wise dataframe related to CoViD-19 with various categories available.'''

        # Rest documentation are same as get_country_dataframe().
        cleaned_data = self.get_cleaned_data()
        continent_dataset = cleaned_data[1:7]

        continent_columns = [
            'continent_name',
            'continent_new_cases',
            'continent_total_cases',
            'continent_total_deaths',
            'continent_new_deaths',
            'continent_total_recovered',
            'continent_active_cases',
            'continent_critical_cases',
            'continent_cases_per_million',
            'continent_deaths_per_million',
            'continent_total_test',
            'continent_tests_per_million',
        ]

        continent_data_lists = {

            'continent_name': [],
            'continent_new_cases': [],
            'continent_total_cases': [],
            'continent_total_deaths': [],
            'continent_new_deaths': [],
            'continent_total_recovered': [],
            'continent_active_cases': [],
            'continent_critical_cases': [],
            'continent_cases_per_million': [],
            'continent_deaths_per_million': [],
            'continent_total_test': [],
            'continent_tests_per_million': [],
        }

        for continent_data in continent_dataset:
            continent_data_lists['continent_name'].append(continent_data[2])
            continent_data_lists['continent_new_cases'].append(
                continent_data[4])
            continent_data_lists['continent_total_cases'].append(
                continent_data[5])
            continent_data_lists['continent_total_deaths'].append(
                continent_data[6])
            continent_data_lists['continent_new_deaths'].append(
                continent_data[7])
            continent_data_lists['continent_total_recovered'].append(
                continent_data[8])
            continent_data_lists['continent_active_cases'].append(
                continent_data[9])
            continent_data_lists['continent_critical_cases'].append(
                continent_data[10])
            continent_data_lists['continent_cases_per_million'].append(
                continent_data[11])
            continent_data_lists['continent_deaths_per_million'].append(
                continent_data[12])
            continent_data_lists['continent_total_test'].append(
                continent_data[13])
            continent_data_lists['continent_tests_per_million'].append(
                continent_data[14])

        continent_data = {
            continent_columns[0]: continent_data_lists['continent_name'],
            continent_columns[1]: continent_data_lists['continent_new_cases'],
            continent_columns[2]: continent_data_lists['continent_total_cases'],
            continent_columns[3]: continent_data_lists['continent_total_deaths'],
            continent_columns[4]: continent_data_lists['continent_new_deaths'],
            continent_columns[5]: continent_data_lists['continent_total_recovered'],
            continent_columns[6]: continent_data_lists['continent_active_cases'],
            continent_columns[7]: continent_data_lists['continent_critical_cases'],
            continent_columns[8]: continent_data_lists['continent_cases_per_million'],
            continent_columns[9]: continent_data_lists['continent_deaths_per_million'],
            continent_columns[10]: continent_data_lists['continent_total_test'],
            continent_columns[11]: continent_data_lists['continent_tests_per_million'],
        }

        continent_df = pd.DataFrame(continent_data, columns=continent_columns)

        return continent_df

    def get_world_dataframe(self):
        '''Get the accumulated world data related to CoViD-19 with various categories available.'''

        # We found that the accumulated world data gets sits on the top of list of counties.
        # Thus we retrieved that index and returned it.
        country_dataframe = self.get_country_dataframe()
        world_dataframe = country_dataframe.iloc[0]  # Topmost row.
        return world_dataframe
