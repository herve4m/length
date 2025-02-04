# unit_mng.py
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

from .unit_cm import UnitCm
from .unit_inch import UnitInch
from .unit_pct import UnitPct
from .unit_pica import UnitPica
from .unit_point import UnitPoint
from .unit_px import UnitPx


class UnitMng:
    """Manage ruler scale units."""

    # List of the class for each units.
    # The order of the classes in this list is used for mapping keyboard
    # shortcuts to units: key 1 switches to pixels, key 2 to centimeters, ...
    unit_classes = [UnitPx, UnitCm, UnitInch, UnitPica, UnitPoint, UnitPct]

    @classmethod
    def array(cls) -> list[dict]:
        """Return a list of unit descriptions.

        Each item of the returned list is a dictionary with the following
        keys:
        * ``name`` is long unit name in human format.
        * ``id`` is the internal identifier of the unit. It is used for the
          ``unit`` GSettings option.
        """
        return [{"name": c.long_name, "id": c.id} for c in cls.unit_classes]

    @classmethod
    def get_unit_class(cls, id: str):
        """Return a class from a unit identifier."""
        for c in cls.unit_classes:
            if c.id == id:
                return c
        return None
