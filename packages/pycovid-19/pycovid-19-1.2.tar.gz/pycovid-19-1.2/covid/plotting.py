# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import datetime

import folium
from pandas.plotting import register_matplotlib_converters

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from covid.database import retrieve_cases, map_data, get_population

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

from covid.exceptions import OffsetError

from covid.tools import check_string

register_matplotlib_converters()


def _get_folium_color(case_type):
    case_type = check_string(case_type, {'deaths', 'confirmed cases', 'recovered cases'})
    if case_type == "deaths":
        return 'red'
    elif case_type == "confirmed cases":
        return 'orange'
    else:
        return "green"  # recovered


def _get_axes_and_database(countries, case_type):
    database = retrieve_cases(countries, case_type)
    if len(countries) > 1:
        nrows = int(np.ceil(len(countries) / 2))
        fig, axes = plt.subplots(nrows, 2)
        axes = axes.flatten()
    else:
        fig, axes = plt.subplots()
        axes = [axes]

    return axes, database


def get_world_map(case_type, normalized=False, date=None):
    """

    :param case_type:
    :param normalized: if True, normalized cases by country's population
    :param date: (datetime object) date for which displaying cases
    :return:
    """
    if date is None:
        date = datetime.date.today() - datetime.timedelta(days=1)

    if normalized:
        title = f"Prevalence ({case_type}) among population"
    else:
        title = f"Number of {case_type}"

    world_map = folium.Map(location=[30, 0], zoom_start=2)
    title_html = f'''<h3 align="center" style="font-size:20px"><b>{title} ({date.strftime('%Y-%m-%d')})</b></h3>'''
    world_map.get_root().html.add_child(folium.Element(title_html))

    (countries, nb_cases, latitude, longitude) = map_data(case_type, date)
    max_of_day = max(nb_cases)

    for country, case, lat, long in zip(countries, nb_cases, latitude, longitude):
        if case > 0:
            if normalized:
                population = get_population(country)
                if population:
                    folium.CircleMarker(
                        location=[lat, long],
                        radius=50 * np.sqrt(100 * case / population),
                        popup=folium.Popup(f'{country}<br>Prevalence: %.3f / 1000<br>{case_type.capitalize()}: '
                                           f'{case}' % (1000 * case/population), max_width=200),
                        fill=True,
                        color=_get_folium_color(case_type),
                        fill_color=_get_folium_color(case_type)).add_to(world_map)
            else:
                folium.CircleMarker(
                    location=[lat, long],
                    radius=20 * np.sqrt(case/max_of_day),
                    popup=folium.Popup(f'{country}<br>{case_type.capitalize()}: {case}', max_width=200),
                    fill=True,
                    color=_get_folium_color(case_type),
                    fill_color=_get_folium_color(case_type)).add_to(world_map)

    return world_map


def plot_cases(countries, case_type, doubling_factor=2, plot_type="log", normalized=False, min_number_of_cases=None,
               min_prevalence=None):
    """ Plot Covid-19 cases

    :param countries:
    :param case_type:
    :param doubling_factor:
    :param plot_type: {'daily', 'log'}
    :param normalized:
    :param min_number_of_cases: minimum number of cases condition for plotting
    :param min_prevalence:
    :return:
    """
    if isinstance(countries, str):
        countries = [countries]

    axes, database = _get_axes_and_database(countries, case_type)

    for ax, (country, dates, cases) in zip(axes, database):

        if normalized:
            ax.set_ylabel("Prevalence (\u2030)")
            population = get_population(country)
            cases = 1000 * cases / population
            if min_prevalence:
                dates = dates[cases >= min_prevalence]
                cases = cases[cases >= min_prevalence]
        else:
            ax.set_ylabel(f"Number of {case_type}")
            if min_number_of_cases:
                dates = dates[cases >= min_number_of_cases]
                cases = cases[cases >= min_number_of_cases]

        theoretical_cases = cases[0] * (2 ** (1 / doubling_factor)) ** np.arange(cases.size)

        if plot_type == 'log':
            for case in [theoretical_cases, cases]:
                ax.plot(dates, case)
            ax.legend([f"Situation where {case_type} double every %.f days" % doubling_factor, f"COVID-19 {case_type}"])
            ax.set_yscale("log")
        elif plot_type == 'daily':
            daily_cases = np.concatenate([[cases[0]], np.diff(cases)])
            ax.bar(dates, daily_cases)
            ax.legend([f"Daily increase of COVID-19 {case_type}"])

        ax.set_title(country)

        # format the ticks
        day_of_month = mdates.DayLocator(interval=max(int(cases.size/4), 1))
        ax.xaxis.set_major_locator(day_of_month)

    plt.subplots_adjust(hspace=0.35)


def plot_pace(countries, case_type, normalized=True, plot_type="log", do_offset=False, offset_value=0.0001,
              min_number_of_cases=None, min_prevalence=None):
    """ Plot case occurrence pace of given countries on the same figure

    :param countries:
    :param case_type:
    :param normalized: (bool)
    :param plot_type: {"normal", "log"}
    :param do_offset: (bool) offset at min_prevalence value
    :param offset_value: (per-thousand)
    :param min_number_of_cases:
    :param min_prevalence:
    :return:
    """
    if isinstance(countries, str):
        countries = [countries]

    fig, ax = plt.subplots()
    if plot_type == "log":
        ax.set_yscale("log")
    plt.grid(True, which='both')
    ax.set_ylabel(f"{case_type.capitalize()} (\u2030)")
    database = retrieve_cases(countries, case_type)
    num_dates = []

    for (country, dates, cases) in database:

        if normalized:
            population = get_population(country)
            cases = 1000 * cases / population
            if min_prevalence:
                dates = dates[cases >= min_prevalence]
                cases = cases[cases >= min_prevalence]
        else:
            if min_number_of_cases:
                dates = dates[cases >= min_number_of_cases]
                cases = cases[cases >= min_number_of_cases]

        if do_offset:
            try:
                offset_date = dates[np.where(cases >= offset_value)[0][0]]
            except IndexError:
                raise OffsetError("Offset value (= %.3f) is greater than the max prevalence/number of cases (= %.3f)"
                                  % (offset_value, cases[-1]))
            dates -= offset_date
            dates = dates.days
            ax.set_xlabel(f"Time (days), origin at {offset_value} (\u2030)")

        num_dates.append(cases.size)
        ax.plot(dates, cases)

    ax.legend(countries)
    if normalized:
        ax.set_title(f"Prevalence ({case_type}) over time")
    else:
        ax.set_title(f"Number of {case_type} over time")

    if not do_offset:
        day_of_month = mdates.DayLocator(interval=int(max(num_dates) / 4))
        ax.xaxis.set_major_locator(day_of_month)
