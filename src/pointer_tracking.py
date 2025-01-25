# pointer_tracking.py
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


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/pointer_tracking.ui")
class PointerTrackingControl(Gtk.Box):
    """Manage the pointer tracking feature of the Length main window."""

    __gtype_name__ = "PointerTrackingControl"

    tracking_label = Gtk.Template.Child()
    tracking_switch = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object.

        :param application_window: The main Length application window
        :type application_window: :py:class:``Gtk.ApplicationWindow``
        """
        super().__init__()

        self.application_window = application_window

        application_window.settings.bind(
            "track-pointer", self.tracking_switch, "active", Gio.SettingsBindFlags.DEFAULT
        )
        self.tracking_label.set_mnemonic_widget(self.tracking_switch)

    @Gtk.Template.Callback()
    def _on_track_switch(self, _widget, _value) -> None:
        self.application_window.drawing_area.queue_draw()
