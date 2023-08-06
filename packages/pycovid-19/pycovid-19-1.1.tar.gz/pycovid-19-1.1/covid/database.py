# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

import pandas as pd
from numpy import unique as npunique

from covid import COVID_DEATHS, COVID_CONFIRMED, COVID_RECOVERED, COUNTRY_WB_MATCH, WORLD_POPULATION
from covid.tools import check_string


def _get_cases(case_type, index_col=1):
    """

    :param case_type:
    :return:
    """
    case_type = check_string(case_type, {'deaths', 'confirmed cases', 'recovered cases'})
    if case_type == 'deaths':
        table = pd.read_csv(COVID_DEATHS, index_col=index_col)
    elif case_type == 'confirmed cases':
        table = pd.read_csv(COVID_CONFIRMED, index_col=index_col)
    else:
        table = pd.read_csv(COVID_RECOVERED, index_col=index_col)

    date = pd.DatetimeIndex(table.loc[:, "1/22/20"::].keys())

    return date, table


def get_population(country):
    """

    :param country:
    :return:
    """
    if country in "Taiwan*":
        return 23508428  # Last estimate from CIA World Factbook

    try:
        country = COUNTRY_WB_MATCH[country]
    except KeyError:
        pass
    finally:
        try:
            return WORLD_POPULATION[country]
        except KeyError:
            return None


def map_data(case_type, date):
    """

    :param case_type:
    :param date:
    :return:
    """
    time, table = _get_cases(case_type)
    countries = table.index.to_series()
    provinces = table.loc[:, "Province/State"]
    province_and_country = countries.copy()
    province_and_country[~provinces.isna()] = provinces.loc[~provinces.isna()].str.cat(
        countries[~provinces.isna()], sep=", ")

    date = f"{date.month}/{date.day}/{date.year - 2000}"
    province_state = [province for province in province_and_country]
    nb_cases = [value for value in table.loc[:, date]]
    latitude = [lat for lat in table.loc[:, "Lat"]]
    longitude = [lon for lon in table.loc[:, "Long"]]

    for country in npunique(countries):

        if province_and_country[province_and_country == country].size == 0:
            province_state.append(country)
            nb_cases.append(table.loc[[country], date].values.sum())
            latitude.append(table.loc[[country], "Lat"].values.mean())
            longitude.append(table.loc[[country], "Long"].values.mean())

    return province_state, nb_cases, latitude, longitude


def retrieve_cases(countries, case_type):
    """

    :param countries: list of (str) country names
    :param case_type: {'deaths', 'cases', 'recovered'}
    :return:
    """
    time, table = _get_cases(case_type)
    results = []

    if countries[0] == "all":
        cases = table.loc[:, "1/22/20"::].sum(axis=0)

        results.append(("Global", time, cases))

    else:
        for country in countries:
            try:
                country_cases = table.loc[[country], :]  # Using a list return a dataframe...
            except KeyError:
                country_cases = table.loc[table["Province/State"] == country]

            if country_cases.shape[0] != 1:
                if not any(country_cases["Province/State"].isna()):
                    country_cases = country_cases.loc[country, "1/22/20"::].sum(axis=0)
                else:
                    country_cases = country_cases.loc[country_cases["Province/State"].isna(), "1/22/20"::]
            else:
                country_cases = country_cases.loc[country, "1/22/20"::]

            results.append((country, time, country_cases.values.flatten()))

    return results
