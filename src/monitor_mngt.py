# monitor_mngt.py
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

import logging
import math

from gi.repository import Gdk, GLib

logger = logging.getLogger(__name__)


class Monitor:
    """Store a monitor parameters."""

    def __init__(self, monitor) -> None:
        """Initialize the object.

        :param monitor: The monitor object.
        :type monitor: :py:class:``Gdk.Monitor``
        """
        self.monitor = monitor

        # Whether the user specifies to let the system compute the monitor size
        # (True), or to compute the size from the given monitor size (False)
        self.compute: bool = True

        # Name of the monitor
        self.name = monitor.get_description()
        logger.debug(f"init ============= {self.name} =============")

        # Size in millimeters. In some environments, the information is not
        # available, and the two methods return 0.
        self.width_mm: int = monitor.get_width_mm()
        self.height_mm: int = monitor.get_height_mm()
        logger.debug(f"     width_mm: {self.width_mm}")
        logger.debug(f"    height_mm: {self.height_mm}")

        # Size in pixels
        geometry = monitor.get_geometry()
        self.width_px: int = geometry.width
        self.height_px: int = geometry.height
        logger.debug(f"     width_px: {self.width_px}")
        logger.debug(f"    height_px: {self.height_px}")

        # Coordinates of the monitor in the display. When several monitors are
        # installed, these coordinates help sorting the monitors in the
        # Preferences window: the left/top most monitor is listed first.
        self.display_x: int = geometry.x
        self.display_y: int = geometry.y
        logger.debug(f"    display_x: {self.display_x}")
        logger.debug(f"    display_y: {self.display_y}")

        # Some environments do not provide the monitor size (*mm == 0).
        if self.width_mm and self.height_mm:
            # Size in pixels per millimeter
            self.width_ppmm: float = self.width_px / self.width_mm
            self.height_ppmm: float = self.height_px / self.height_mm
            # Compute the diagonal size of the monitor
            self.diag_inch: float = math.sqrt(self.width_mm**2 + self.height_mm**2) / 25.4

        else:
            self.width_ppmm = self.height_ppmm = self.diag_inch = 0.0
        logger.debug(f"   width_ppmm: {self.width_ppmm}")
        logger.debug(f"  height_ppmm: {self.height_ppmm}")
        logger.debug(f"    diag_inch: {self.diag_inch}")

    def __lt__(self, other):
        """Compare Monitor objects.

        This method is used to sort the monitors according to their position in
        the display.

        :param other: The monitor object to compare.
        :type other: :py:class:``Monitor``

        """
        x_abs = abs(self.display_x, other.display_x)
        y_abs = abs(self.display_y, other.display_y)
        if x_abs > y_abs:
            return self.display_x < other.display_x
        return self.display_y < other.display_y

    def set_diagonal_inch(self, diag: float) -> None:
        """Force setting the diagonal size of the display."""
        self.compute = False
        self.diag_inch = diag
        # Compute the *ppm attributes according to the given diagonal size
        ppi = self.width_px / math.sqrt(
            (diag**2) / (1 + (self.height_px / self.width_px) ** 2)
        )
        self.width_ppmm = self.height_ppmm = ppi / 25.4  # Convert from inch to millimeter
        logger.debug(f"set_diagonal_inch ============= {self.name} =============")
        logger.debug(f"  width_ppmm: {self.width_ppmm}")
        logger.debug(f" height_ppmm: {self.height_ppmm}")
        logger.debug(f"   diag_inch: {self.diag_inch}")


class MonitorMngt:
    """Mange the list of monitors available on the system."""

    def __init__(self, settings) -> None:
        """Initialize the object.

        :param settings: Application settings.
        :type settings: :py:class:``GSettings``
        """
        self.settings = settings

        # Monitor list as a dictionary. The key is the monitor name/description
        self.monitors = {}
        # List of the Monitor objects ordered by their position in the display
        self.monitor_list = []

    def set_settings(self) -> None:
        """Save the monitor parameters into GSettings."""
        array = GLib.VariantBuilder.new(GLib.VariantType.new("aa{ss}"))
        for monitor in self.monitor_list:
            d_monitor = GLib.VariantBuilder.new(GLib.VariantType.new("a{ss}"))

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "monitor"))
            entry.add_value(GLib.Variant("s", monitor.name))
            d_monitor.add_value(entry.end())

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "compute"))
            entry.add_value(GLib.Variant("s", str(monitor.compute)))
            d_monitor.add_value(entry.end())

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "diagonal"))
            entry.add_value(GLib.Variant("s", str(monitor.diag_inch)))
            d_monitor.add_value(entry.end())

            array.add_value(d_monitor.end())
        self.settings.set_value("calibration", array.end())
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx
        # print(self.settings.get_value("calibration"))

    def get_settings(self) -> None:
        """Update the monitor list with the GSettings parameters."""
        va = self.settings.get_value("calibration")
        for i in range(va.n_children()):
            vd = va.get_child_value(i)
            monitor = {}
            for j in range(vd.n_children()):
                m = vd.get_child_value(j)
                k = m.get_child_value(0).get_string()
                v = m.get_child_value(1).get_string()
                if k == "compute":
                    v = bool(v)
                elif k == "diagonal":
                    v = float(v)
                monitor[k] = v
                logger.debug(f"Get settings:       calibration: {k} -> {v}")
            if monitor_obj := self.get_monitor(monitor.get("monitor")):
                if not monitor.get("compute", True) and monitor.get("diagonal"):
                    monitor_obj.set_diagonal_inch(monitor.get("diagonal"))

    def retrieve_monitors(self) -> None:
        """Build the monitor lists from the monitors discovered in the system"""

        # Retrieve the monitors from the hardware
        display = Gdk.Display.get_default()
        monitors = {}
        for monitor in display.get_monitors():
            monitor_obj = Monitor(monitor)
            monitors[monitor_obj.name] = monitor_obj
        self.monitors = monitors
        self.monitor_list = sorted(monitors.values())

    def get_monitor(self, monitor_name: str):
        """Return the Monitor object that correspond to the given name.

        :return: The Monitor object or None if the monitor does not exist.
        :rtype: :py:class:``Monitor``
        """
        if not monitor_name:
            return None
        if not self.monitors:
            self.retrieve_monitors()
        return self.monitors.get(monitor_name)
