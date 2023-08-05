#!/usr/bin/env python

"""
Factories for creating recurrence analysis computations.
"""

from pyrqa.exceptions import UnsupportedNeighbourhoodException
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor, \
    Unthresholded

from pyrqa.variants.rp.radius.execution_engine import ExecutionEngine as RPRadiusExecutionEngine
from pyrqa.variants.rp.unthresholded.execution_engine import ExecutionEngine as RPUnthresholdedExecutionEngine
from pyrqa.variants.rqa.radius.execution_engine import ExecutionEngine as RQAExecutionEngine

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPComputation(object):
    """
    Factory for creating a recurrence plot computation.
    """

    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create RQA computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """

        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RPRadiusExecutionEngine(settings,
                                           **kwargs)
        elif isinstance(settings.neighbourhood,
                        Unthresholded):
            return RPUnthresholdedExecutionEngine(settings,
                                                  **kwargs)
        else:
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not supported regarding recurrence plot computations!" % settings.neighbourhood.__class__.__name__)


class RQAComputation(object):
    """
    Factory for creating a recurrence quantification analysis computation.
    """

    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create recurrence plot computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """

        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RQAExecutionEngine(settings,
                                      **kwargs)
        else:
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not supported regarding RQA computations!" % settings.neighbourhood.__class__.__name__)
