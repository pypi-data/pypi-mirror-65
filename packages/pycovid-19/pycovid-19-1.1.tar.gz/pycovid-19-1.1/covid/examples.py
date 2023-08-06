# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


from covid.plotting import plot_cases
from matplotlib import pyplot as plt

countries = ["Germany", "Sweden", "Netherlands", "France"]

plot_cases(countries, "deaths", doubling_factor=2, plot_type="log")
plot_cases("Sweden", "deaths", plot_type="daily")
plot_cases("all", "confirmed", doubling_factor=2, plot_type="log")

plt.show()
