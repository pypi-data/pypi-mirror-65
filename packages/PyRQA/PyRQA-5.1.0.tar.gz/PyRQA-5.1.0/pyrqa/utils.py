#!/usr/bin/env python

"""
Collection of abstract classes.
"""

from pyrqa.exceptions import InconsistentNumberOfVectorsException
from pyrqa.exceptions import InvalidSettingsInputException
from pyrqa.settings import Settings

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class SettableSettings(object):
    """
    Base settings.

    :ivar settings: Recurrence analysis settings.
    """
    def __init__(self, settings):
        self.settings_1 = self.get_settings(settings,
                                            0)
        self.settings_2 = self.get_settings(settings,
                                            1)

    @staticmethod
    def get_settings(settings,
                     ind):
        """
        Get single Settings instance.

        :param settings: One or multiple Settings instances.
        :param ind: Index of Settings instance to retrieve.
        :return: Single Settings instance.
        """
        if type(settings) is Settings:
            return settings
        elif (type(settings) is tuple or type(settings) is list) and len(settings) == 2:
            return settings[ind]
        else:
            raise InvalidSettingsInputException(
                "Either a single Settings instance or tuple/list of two settings instances should be passed as argument.")

    @property
    def settings(self):
        """
        Alias for settings_1 to ensure compatibility with RQA and CRQA processing.

        :return: Settings instance.
        """
        return self.settings_1

    @property
    def settings_1(self):
        """
        Get Settings instance of the first (cross) recurrence matrix.

        :return: Settings instance.
        """
        try:
            return self.__settings_1
        except Exception:
            return None

    @settings_1.setter
    def settings_1(self,
                   settings):
        """
        Set Settings instance of the first (cross) recurrence matrix.

        :param settings: Settings instance of the first (cross) recurrence matrix.
        :return: Settings instance.
        """
        if type(settings) is not Settings:
            raise InvalidSettingsInputException("First instance is not of type Settings.")

        self.__settings_1 = settings

    @property
    def settings_2(self):
        """
        Get Settings instance of the second (cross) recurrence matrix.

        :return: Settings instance.
        """
        try:
            return self.__settings_2
        except Exception:
            return None

    @settings_2.setter
    def settings_2(self,
                   settings):
        """
        Set Settings instance of the second (cross) recurrence matrix.

        :param settings: Settings instance of the second (cross) recurrence matrix.
        :return: Settings instance.
        """
        if type(settings) is not Settings:
            raise InvalidSettingsInputException("Second instance is not of type Settings.")

        self.__settings_2 = settings

    def validate_settings(self):
        if self.settings_1 and self.settings_2:
            if not self.settings_1.time_series_x.number_of_vectors == self.settings_2.time_series_x.number_of_vectors:
                raise InconsistentNumberOfVectorsException(
                    "The number of vector of the time series on the x axis are inconsistent.")
            if not self.settings_1.time_series_y.number_of_vectors == self.settings_2.time_series_y.number_of_vectors:
                raise InconsistentNumberOfVectorsException(
                    "The number of vector of the time series on the y axis are inconsistent.")

        return True

class SettableMatrixRuntimes(object):
    """
    Base matrix runtimes.

    :ivar matrix_runtimes: Computing runtimes.
    """

    def __init__(self, matrix_runtimes):
        self.matrix_runtimes = matrix_runtimes


class Runnable(object):
    """
    Base runnable.
    """

    def run(self):
        """
        Perform computations.
        """

        pass

    def run_single_device(self):
        """
        Perform computations using a single computing device.
        """

        pass

    def run_multiple_devices(self):
        """
        Perform computations using multiple computing devices.
        """

        pass


class Verbose(object):
    """
    Base verbose.

    :ivar verbose: Boolean value indicating the verbosity of print outs.
    """

    def __init__(self, verbose):
        self.verbose = verbose

    def print_out(self, obj):
        """
        Print string if verbose is true.
        """

        if self.verbose:
            print(obj)
