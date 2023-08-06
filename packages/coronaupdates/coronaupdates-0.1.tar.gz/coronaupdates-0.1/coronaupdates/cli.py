'''Command Line Interface for retrieving CoViD-19 related informations.'''
import argparse
import datetime
import os
from sys import argv
from tabulate import tabulate

from .core import Covid19

# Commands available.
CHOICES = [
    'confirmed',
    'recovered',
    'dead',
    'critical',
    'newcases',
    'active',
    'newdeaths'
]

# Mapping commands to columns of dataframes.
MAPPINGS = {
    'confirmed': 'total_cases',
    'recovered': 'total_recovered',
    'dead': 'total_deaths',
    'critical': 'critical_cases',
    'newcases': 'new_cases',
    'active': 'active_cases',
    'newdeaths': 'new_deaths',
}

COVID_19_OBJ = Covid19()


def create_csv(geography_type=None, filepath=None):
    '''Creates the CSV file containing CoViD-19 updates of current time.'''

    if geography_type.lower() == 'country':
        dataframe = COVID_19_OBJ.get_country_dataframe()
        geography_type = 'Country'
    elif geography_type.lower() == 'country':
        dataframe = COVID_19_OBJ.get_continent_dataframe()
        geography_type = 'Continent'
    else:
        print('Invalid Geography type.')
        return None

    timestamp = datetime.datetime.now()
    filename = '{}COVID_19_{}_{}_{}_{}__{}_{}__{}.csv'.format(
        filepath,
        geography_type.upper(),
        timestamp.year,
        timestamp.month,
        timestamp.day,
        timestamp.hour,
        timestamp.minute,
        timestamp.strftime("%A")
    )
    dataframe.to_csv(filename, sep=',')

    return filename


def parse_args_from_user():
    '''Retrieves arguments from user and processes accordingly.'''

    parser = argparse.ArgumentParser(
        description='Command Line Interface for Corona Virus (CoViD-19) Informations.',
        prog='covid',
    )

    parser.add_argument('--show',
                        '-s',
                        help='Shows the info by category',
                        choices=CHOICES,  # Allowed choices.
                        metavar='category'  # Alias
                        )

    parser.add_argument('--country',
                        '-c',
                        help='Shows the info by country.',
                        metavar='country'
                        )

    parser.add_argument('--downloadcsv',
                        '-d',
                        help='Downloads the CSV file containing CoViD-19 updates of current time.',
                        metavar='filepath'
                        )

    args = parser.parse_args()

    if len(argv) < 2:
        parser.parse_args(['-h'])

    if args.show and args.country:

        country_df = COVID_19_OBJ.get_country_dataframe()
        country_df['country'] = country_df['country'].str.upper()
        country_query = args.country.upper()
        country_result = country_df.loc[country_df['country'] == country_query]
        categorical_country_result = country_result[MAPPINGS[args.show]]
        result = list(categorical_country_result)[0]
        if len(result) < 0 or result == ' ':
            result = 0
        label = MAPPINGS[args.show].replace('_', ' ').title()
        print(f'\n{label} : {result} in {country_query}\n')

    elif not args.country and args.show:

        world_df = COVID_19_OBJ.get_world_dataframe()
        label = MAPPINGS[args.show].replace('_', ' ').title()
        result = world_df[MAPPINGS[args.show]]
        print(f'\n{label} : {result} WORLDWIDE\n')

    elif not args.show and args.country:

        country_df = COVID_19_OBJ.get_country_dataframe()
        country_df['country'] = country_df['country'].str.upper()
        country_query = args.country.upper()
        country_result = country_df.loc[country_df['country'] == country_query]
        country_result = country_result.T
        country_result = country_result[country_result[country_result.columns[0]].map(
            len) != 0]
        print(tabulate(country_result, headers='', tablefmt='psql'))

    if args.downloadcsv:
        os.chdir(args.downloadcsv)
        create_csv(filepath=f'{os.getcwd()}/', geography_type='country')
