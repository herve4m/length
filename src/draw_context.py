# draw_context.py
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

import math

from gi.repository import Pango, Adw


class DrawContext:
    """Store the parameters required for drawing the ruler."""

    def __init__(self, settings) -> None:
        """Initialize the object.

        :param settings: Application settings.
        :type settings: :py:class:``GSettings``
        """

        self.settings = settings
        self._warning_dialog = None

        # Gdk.Monitor
        self._monitor = None
        # Monitor width
        self.monitor_width: int = 0
        # Monitor height
        self.monitor_height: int = 0
        # Pixels per millimeter
        self._ppmm: float = 0.0

        # Cairo context
        self.ctx = None

        # Drawing area size
        self.width: int = 0
        self.height: int = 0

        # Orientation
        self.is_horizontal: bool = True

        # Pointer position in the Drawing area
        self.pointer_x: float = 0.0
        self.pointer_y: float = 0.0

        # Whether to track the pointer
        self.track_pointer: bool = False

        # Whether the pointer tracker is locked in position
        self.track_locked: bool = False

        # Position of the pointer tracker
        self.track_pos: float = 0.0

        # Offset (in ruler units)
        self.offset: float = 0.0

        # Colors (RGBA)
        self.color_fg: list[float] = [0.0, 0.0, 0.0, 1.0]
        self.color_bg: list[float] = [1.0, 1.0, 1.0, 1.0]
        self.color_track: list[float] = [1.0, 0.0, 0.0, 1.0]

        # Font
        self.font_name: str = None
        self.font_desc = None
        # Font for the pointer tracking label
        self.font_desc_small = None

        # Scale direction
        self.left2right: bool = True

        # Monitor size
        self.compute_monitor_size: bool = True
        self.monitor_diagonal_inch: float = 24.0

    def refresh_from_settings(self) -> None:
        """Reload the parameter from GSettings."""

        self.track_pointer = self.settings.get_boolean("track-pointer")
        self.offset = self.settings.get_double("offset")

        # Colors
        if self.settings.get_boolean("use-default-color"):
            self.color_fg = [0.0, 0.0, 0.0, 1.0]
            self.color_bg = [1.0, 1.0, 1.0, 1.0]
        else:
            self.color_fg = self.settings.get_value("foreground-color")
            self.color_bg = self.settings.get_value("background-color")

        # Font
        font = (
            "Monospace 10"
            if self.settings.get_boolean("use-default-font")
            else self.settings.get_string("font-name")
        )
        if font != self.font_name:
            self.font_name = font
            self.font_desc = Pango.font_description_from_string(font)
            # Reduce the font size by 3/4
            self.font_desc_small = self.font_desc.copy()
            self.font_desc_small.set_size(self.font_desc.get_size() * 3.0 / 4.0)

        # Scale direction
        self.left2right = self.settings.get_boolean("direction-left-to-right")

        # Monitor size
        self.compute_monitor_size = self.settings.get_boolean("compute-monitor-size")
        self.monitor_diagonal_inch = self.settings.get_double("monitor-size")

    def warning(self) -> None:
        """Display a warning message when the system does not provide the monitor size.

        The dialog is only displayed once.
        """

        if not self._warning_dialog:
            self._warning_dialog = Adw.AlertDialog()
            self._warning_dialog.set_heading(_("Monitor Size Unknown"))
            self._warning_dialog.set_body(
                _(
                    "The monitor size cannot be determined.\n"
                    "Use the Preferences dialog to calibrate Length for "
                    "your monitor size.\n"
                    "In the meantime, computations are done for a "
                    f"{round(self.monitor_diagonal_inch, 1)} "
                    "inches monitor."
                )
            )
            self._warning_dialog.add_response("ok", _("OK"))
            self._warning_dialog.set_default_response("ok")
            self._warning_dialog.set_close_response("ok")
            self._warning_dialog.present()

    def set_monitor(self, monitor) -> None:
        """Set the monitor object that is used to compute some ruler units.

        :param monitor: The object used to convert the unit into pixels.
        :type monitor: :py:class:``Gdk.Monitor``
        """
        self._monitor = monitor
        if monitor:
            geometry = monitor.get_geometry()
            self.monitor_width = geometry.width
            self.monitor_height = geometry.height
        else:
            # monitor should not be None
            self.monitor_width = 1920
            self.monitor_height = 1080
        self._ppmm = 0.0

    def _compute_ppmm(self) -> float:
        """Compute and return the number of pixels per millimeter (ppmm).

        The computation uses the user provided monitor diagonal size (in the
        ``monitor-size`` GSettings parameter).
        """
        if self._ppmm:
            return self._ppmm
        ppi = self.monitor_width / math.sqrt(
            (self.monitor_diagonal_inch**2)
            / (1 + (self.monitor_height / self.monitor_width) ** 2)
        )
        self._ppmm = ppi / 25.4  # Convert from inch to millimeter
        return self._ppmm

    @property
    def ppmm_width(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the width."""

        # If the user specifies their monitor size through the Preferences
        # dialog, then use that size for computing the ppmm.
        if not self.compute_monitor_size:
            return self._compute_ppmm()

        if self._monitor and (mm := self._monitor.get_width_mm()):
            return self.monitor_width / mm
        else:
            # Some environments do not provide the monitor size (mm == 0).
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user
            self.warning()
            return self._compute_ppmm()

    @property
    def ppmm_height(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the height."""

        # If the user specifies their monitor size through the Preferences
        # dialog, then use that size for computing the ppmm.
        if not self.compute_monitor_size:
            return self._compute_ppmm()

        if self._monitor and (mm := self._monitor.get_height_mm()):
            return self.monitor_height / mm
        else:
            # Some environments do not provide the monitor size (mm == 0).
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user
            self.warning()
            return self._compute_ppmm()
