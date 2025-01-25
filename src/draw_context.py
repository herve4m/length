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
        self.color_fg: list[float] = [0, 0, 0.20, 1.0]
        self.color_bg: list[float] = [1.0, 1.0, 0.0, 1.0]
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
            self.color_fg = [0, 0, 0.20, 1.0]
            self.color_bg = [1.0, 1.0, 0.0, 1.0]
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
