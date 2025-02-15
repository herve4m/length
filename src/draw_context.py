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

import logging

from gi.repository import Pango, Adw

logger = logging.getLogger(__name__)


class DrawContext:
    """Store the parameters required for drawing the ruler."""

    def __init__(self, settings, monitors) -> None:
        """Initialize the object.

        :param settings: Application settings.
        :type settings: :py:class:``GSettings``
        :param monitors: Application settings.
        :type monitors: :py:class:``monitor_mngt.MonitorMngt``
        """
        self.settings = settings
        self.monitors = monitors

        # Warning dialog window per monitor
        self._warning_dialogs = {}

        # Monitor currently used by the ruler (monitor_mngt.Monitor)
        self.current_monitor = None

        # Cairo context
        self.ctx = None

        # Drawing area size
        self.width: int = 0
        self.height: int = 0

        # Pointer position in the Drawing area
        self.pointer_x: float = 0.0
        self.pointer_y: float = 0.0

        # Whether to track the pointer
        self.track_pointer: bool = False

        # Whether the pointer tracker is locked in position
        self.track_locked: bool = False

        # Position of the pointer tracker when locked
        self.track_pos_x: float = 0.0
        self.track_pos_y: float = 0.0

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

    def refresh_from_settings(self) -> None:
        """Reload the parameter from GSettings."""
        self.track_pointer = self.settings.get_boolean("track-pointer")
        self.offset = self.settings.get_double("offset")

        logger.debug(f"Get settings:     track-pointer: {self.track_pointer}")
        logger.debug(f"Get settings:            offset: {self.offset}")

        # Colors
        if self.settings.get_boolean("use-default-color"):
            self.color_fg = [0.0, 0.0, 0.0, 1.0]
            self.color_bg = [1.0, 1.0, 1.0, 1.0]
            logger.debug("Get settings: use-default-color: True")
        else:
            self.color_fg = self.settings.get_value("foreground-color")
            self.color_bg = self.settings.get_value("background-color")
            logger.debug("Get settings: use-default-color: False")
            logger.debug(f"Get settings:  foreground-color: {self.color_fg}")
            logger.debug(f"Get settings:  background-color: {self.color_bg}")

        # Font
        font = (
            "Monospace 10"
            if self.settings.get_boolean("use-default-font")
            else self.settings.get_string("font-name")
        )
        logger.debug(f"Get settings:              font: {font}")
        if font != self.font_name:
            self.font_name = font
            self.font_desc = Pango.font_description_from_string(font)
            # Reduce the font size by 3/4
            self.font_desc_small = self.font_desc.copy()
            self.font_desc_small.set_size(self.font_desc.get_size() * 3.0 / 4.0)

        # Scale direction
        self.left2right = self.settings.get_boolean("direction-left-to-right")
        logger.debug(f"Get settings: direction-left-to-right: {self.left2right}")

        # Monitor calibration parameters
        self.monitors.get_settings()

    def warning(self) -> None:
        """Display a warning message when the system does not provide the monitor size.

        The dialog is only displayed once per monitor.
        """
        monitor_name = self.current_monitor.name
        if not self._warning_dialogs.get(monitor_name):
            dialog = Adw.AlertDialog()
            dialog.set_heading(_("Monitor Size Unknown"))
            dialog.set_body(
                _(
                    f"The size of the {monitor_name} monitor cannot be determined.\n"
                    "Use the Preferences dialog to calibrate Length for "
                    "your monitor size.\n"
                    "In the meantime, computations are done for a "
                    f"{round(self.current_monitor.diag_inch, 1)} "
                    "inches monitor."
                )
            )
            dialog.add_response("ok", _("OK"))
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present()
            self._warning_dialogs[monitor_name] = dialog

    def set_monitor(self, monitor) -> None:
        """Set the monitor object that is used to compute some ruler units.

        :param monitor: The object used to convert the unit into pixels.
        :type monitor: :py:class:``monitor_mngt.Monitor``
        """
        self.current_monitor = monitor

    @property
    def ppmm_width(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the width."""
        if not self.current_monitor.width_ppmm:
            # Some environments do not provide the monitor size.
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user.
            logger.debug("width_ppmm == 0")
            self.current_monitor.set_diagonal_inch(24.0)
            self.current_monitor.set_compute(False)
            self.warning()
        return self.current_monitor.width_ppmm

    @property
    def ppmm_height(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the height."""
        if not self.current_monitor.height_ppmm:
            # Some environments do not provide the monitor size.
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user.
            logger.debug("height_ppmm == 0")
            self.current_monitor.set_diagonal_inch(24.0)
            self.current_monitor.set_compute(False)
            self.warning()
        return self.current_monitor.height_ppmm

    @property
    def monitor_width(self) -> int:
        """Return the display width in pixels."""
        return self.current_monitor.width_px

    @property
    def monitor_height(self) -> int:
        """Return the display height in pixels."""
        return self.current_monitor.height_px
