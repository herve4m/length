# offset.py
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

from gi.repository import Gtk, Gio


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/offset.ui")
class OffsetControl(Gtk.Box):
    """Manage the offset feature of the Length main window."""

    __gtype_name__ = "OffsetControl"

    offset_label = Gtk.Template.Child()
    offset_spin = Gtk.Template.Child()
    offset_adjustment = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object.

        :param application_window: The main Length application window
        :type application_window: :py:class:``Gtk.ApplicationWindow``
        """
        super().__init__()

        self.application_window = application_window
        self.offset_label.set_mnemonic_widget(self.offset_spin)
        self._unit = None

        application_window.settings.bind(
            "offset", self.offset_adjustment, "value", Gio.SettingsBindFlags.DEFAULT
        )

    def update_adjustment(self, unit: str, unit_obj) -> None:
        """Update the GtkAdjustment for the offset GtkSpinButton."""
        if self._unit == unit:
            return
        self._unit = unit
        save_value = self.application_window.settings.get_double("offset")
        self.offset_adjustment.configure(*unit_obj.offset_adjustment)
        self.offset_adjustment.set_value(save_value)
        self.offset_spin.set_digits(unit_obj.offset_decimals)

    @Gtk.Template.Callback()
    def _on_value_changed(self, adjustment) -> None:
        self.application_window.drawing_area.queue_draw()
