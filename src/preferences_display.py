# preferences_display.py
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

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/preferences_display.ui")
class PreferencesDisplay(Adw.ExpanderRow):
    __gtype_name__ = "PreferencesDisplay"

    compute_monitor_size = Gtk.Template.Child()
    monitor_adjustment = Gtk.Template.Child()

    def __init__(self, application_window, monitor) -> None:
        """Initialize the object."""
        super().__init__()

        self.application_window = application_window
        self.monitors = application_window.monitors
        self.monitor = monitor

        self.set_title(monitor.name)
        if monitor.diag_inch:
            self.monitor_adjustment.set_value(monitor.diag_inch)
        self.compute_monitor_size.set_active(monitor.compute)

    @Gtk.Template.Callback()
    def _on_compute_monitor_size(self, widget, value) -> None:
        compute = widget.get_active()
        self.monitor.set_compute(compute)
        if not compute:
            self.monitor.set_diagonal_inch(self.monitor_adjustment.get_value())
        self.monitors.set_settings()
        self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _monitor_size_changed_event(self, adjustment) -> None:
        self.monitor.set_diagonal_inch(adjustment.get_value())
        self.monitors.set_settings()
        self.application_window.drawing_area.queue_draw()
