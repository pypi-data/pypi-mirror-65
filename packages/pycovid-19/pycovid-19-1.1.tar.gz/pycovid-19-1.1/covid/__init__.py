# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'
__version__ = '1.01'

import os
import tempfile
import world_bank_data as wb
from urllib.request import urlretrieve

from pandas import read_csv

covid_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(covid_dir, "data")

COVID_DEATHS = os.path.join(tempfile.gettempdir(), "covid_deaths.csv")
COVID_CONFIRMED = os.path.join(tempfile.gettempdir(), "covid_confirmed.csv")
COVID_RECOVERED = os.path.join(tempfile.gettempdir(), "covid_recovered.csv")
WORLD_POPULATION = wb.get_series('SP.POP.TOTL', mrv=1, simplify_index=True)["Afghanistan"::]
COUNTRY_WB_MATCH = read_csv(os.path.join(data_dir, "country_wb_match.csv"), index_col=0,
                            skipinitialspace=True)["Country WB"]

urlretrieve("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
            "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv", COVID_DEATHS)

urlretrieve("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
            "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", COVID_CONFIRMED)

urlretrieve("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
            "/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", COVID_RECOVERED)
