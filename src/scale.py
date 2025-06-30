# scale.py
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


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/scale.ui")
class ScaleControl(Gtk.Box):
    """Manage the scale factor of the Length units."""

    __gtype_name__ = "ScaleControl"

    scale_label = Gtk.Template.Child()
    scale_spin = Gtk.Template.Child()
    scale_adjustment = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object.

        :param application_window: The main Length application window
        :type application_window: :py:class:``Gtk.ApplicationWindow``
        """
        super().__init__()

        self.application_window = application_window
        self.scale_label.set_mnemonic_widget(self.scale_spin)
        self._unit = None

        application_window.settings.bind(
            "scale", self.scale_adjustment, "value", Gio.SettingsBindFlags.DEFAULT
        )

    def update_adjustment(self, unit: str, unit_obj) -> None:
        """Update the GtkAdjustment for the offset GtkSpinButton."""
        if self._unit == unit:
            return
        self._unit = unit
        self.scale_spin.set_sensitive(unit_obj.scalable)

    @Gtk.Template.Callback()
    def _on_value_changed(self, adjustment) -> None:
        print("Changed")
