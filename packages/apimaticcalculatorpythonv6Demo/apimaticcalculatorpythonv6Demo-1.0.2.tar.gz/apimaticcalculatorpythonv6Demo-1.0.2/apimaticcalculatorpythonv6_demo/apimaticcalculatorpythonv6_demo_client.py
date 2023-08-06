# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv6_demo

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv6_demo.decorators import lazy_property
from apimaticcalculatorpythonv6_demo.configuration import Configuration
from apimaticcalculatorpythonv6_demo.controllers.calculator_dev_ops_conf import CalculatorDevOpsConf


class Apimaticcalculatorpythonv6DemoClient(object):

    config = Configuration

    @lazy_property
    def calculator_dev_ops_conf(self):
        return CalculatorDevOpsConf()


