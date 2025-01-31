# unit_cm.py
#
# Copyright 2025 Hervé Quatremain
#
# This file is part of Length.
#
# Length is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Length is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Length. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .unit import Unit


class UnitCm(Unit):

    # Identifier of the unit in the "unit" GSettings option
    id: str = "cm"
    # Short name that is used to display the unit on the ruler
    short_name: str = _("cm")
    # Human readable unit name that is used in the Preferences dialog
    long_name: str = _("Centimeters")

    # Adjustment parameters for the offset spin button
    #  [
    #    Default value (ignored because it is overwritten),
    #    Min,
    #    Max,
    #    Step increment,
    #    Page increment,
    #    Page size (always set it to 0.0)
    #  ]
    offset_adjustment = [0.0, -200.0, 200.0, 0.1, 1.0, 0.0]
    # Number of decimals to display in the spin button
    offset_decimals = 1

    def __init__(self, context) -> None:
        """Initialize the object.

        :param context: Object that stores the parameters for drawing the ruler
        :type context: :py:class:``DrawContext``
        """
        super().__init__(context)

        self.ticks = {
            1: {"length": 4, "label": False, "show_when_wide": False},
            5: {"length": 8, "label": False, "show_when_wide": True},
            10: {"length": 15, "label": True, "show_when_wide": True},
        }
        self.tick_max_length = 15

        self.unit_multiplier = 10
        self.px_per_tick_width = context.ppmm_width
        self.px_per_tick_height = context.ppmm_height
