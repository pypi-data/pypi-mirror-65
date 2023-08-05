#!/usr/bin/env python

"""
Generate recurrence plot from recurrence matrix
"""

import numpy as np

from PIL import Image, ImageOps

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class ImageGenerator(object):
    """
    Image generator
    """

    @classmethod
    def generate_recurrence_plot(cls,
                                 recurrence_matrix,
                                 invert=True):
        """
        Generate recurrence plot from recurrence matrix.

        :param recurrence_matrix: Recurrence matrix.
        :returns: Recurrence plot.
        :rtype: PIL image.
        """
        pil_image = Image.fromarray(np.uint8(np.floor(recurrence_matrix * 255)))

        if invert:
            pil_image = ImageOps.invert(pil_image)

        pil_image = pil_image.convert(mode='RGB',
                                      palette=Image.ADAPTIVE)

        return pil_image

    @classmethod
    def save_recurrence_plot(cls,
                             recurrence_matrix,
                             path):
        """
        Generate and save recurrence plot from recurrence matrix.

        :param recurrence_matrix: Recurrence matrix.
        :param path: Path to output file.
        """

        pil_image = ImageGenerator.generate_recurrence_plot(recurrence_matrix)
        pil_image.save(path)

    @classmethod
    def save_unthresholded_recurrence_plot(cls,
                                           recurrence_matrix,
                                           path):
        """
        Generate and save recurrence plot from recurrence matrix.

        :param recurrence_matrix: Recurrence matrix.
        :param path: Path to output file.
        """

        pil_image = ImageGenerator.generate_recurrence_plot(recurrence_matrix,
                                                            invert=False)
        pil_image.save(path)


