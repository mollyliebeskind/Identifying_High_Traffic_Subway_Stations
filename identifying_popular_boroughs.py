import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
import locale
from locale import atof

%config InlineBackend.figure_format = 'svg'
%matplotlib inline

"""
This file loads and cleans NYC census data to determine which boroughs
to prioritize when marketing in subway stations in order to reach the most
women who are interested in technology. It then outputs a series of plots
to indicate the following.

1. Women per square mile in the five boroughs
2. Annual income per borough to indicate high-spending boroughs
3. Female-owned firms per square mile to identify women interested in tech
4. Homes with boradband to identify regions with emphasis on technology
"""

census = pd.read_csv('NYC Census Jan-09-2020.csv')

def clean_census_data(data):
    """
    Remove Superfluous "Value Note" colums, transpose dataset so that borough represents rows instead
    of columns, drop null values.
    """

    ccols = [c for c in census.columns if c.lower()[0:10] != "value note"]
    data = data[ccols]
    data.columns = data.columns.str.split(')').str[0].str.lower() \
                                   .str.split('(').str[1].str.rsplit(' ', 1).str[0]

    data.columns = ['borough', np.nan, 'nyc', 'bronx', 'brooklyn',
                      'manhattan', 'queens', 'staten_island']

    #Transpose dataframe so that boroughs represent rows instead of columns.
    data = data.set_index('borough').T

    #Drop columns with only empty values
    data = data.drop(np.nan)
    data = data.dropna(axis='columns',thresh=2)

    return data

def census_feature_selection():
    """Select only columns that will be used for analysis and rename columns for easier accessing."""

    data.columns.str.strip()

    data_cols = ['Population estimates, July 1, 2018,  (V2018)','Female persons, percent',
               'Households with a broadband Internet subscription, percent, 2014-2018',
               'Median household income (in 2018 dollars), 2014-2018',
               'Women-owned firms, 2012', 'All firms, 2012', 'Land area in square miles, 2010']

    data = data[data_cols]

    new_column_names = ['population', 'perc_female', 'perc_broadband',
                        'income_dol', 'womenfirms', 'allfirms', 'area']

    data.columns = new_column_names

    return data

def secondary_census_cleaning(data):
    """Remove symbols from dataset."""
    data.perc_female = data.perc_female.str.rstrip('%') / 100.0
    data.perc_broadband = data.perc_broadband.str.rstrip('%') / 100.0
    data.income_dol = data.income_dol.str.lstrip('$')

    return data

def feature_engineering(data):
    """Create column for percentage of firms owned by women & population per square mile"""

    data['womfirm_percent'] = data['womenfirms']/data['allfirms']
    data['pop_persqmi'] = data['population']//data['area']

    return data

def census_plots(y, y_ax, graph_title):
    brand_blue = '#042263FF'
    boroughs = ['NYC (All Boroughs)', 'Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']

    plt.figure(figsize=(10,6))
    ax = sns.barplot(boroughs, y, color=brand_blue)
    ax.set(xlabel='Borough', ylabel=y_ax, title=graph_title);
    sns.set_style('white')
    sns.despine()

    plt.savefig(f"{graph_title}.png")

    return

census = clean_census_data(census)
census = census_feature_selection(census)
census = secondary_census_cleaning(census)
census = feature_engineering(census)

#Visualize Women per Square Mile in the 5 boroughs to compare density of women per borough
y = census['perc_female']*census['pop_persqmi']
census_plots(y, y_ax='Number of Women', graph_title='Women per Square Mile')

# Plot annual income per borough to identify high spenders for marketing efficiency
y = census['income_dol']
census_plots(y, y_ax='Income', graph_title='Median Annual Income (in dollars)')

#Plot Female-Owned Firms per Square Mile
y = census['womenfirms']/census['area']
census_plots(y, y_ax='Firms', graph_title='Female-Owned Firms per Square Mile')

#Plot Homes with Broadband to identify regions with higher emphasis on technology
y = census['perc_broadband']*100
census_plots(y, y_ax='Percentage of Homes', graph_title='Homes with Broadband')
