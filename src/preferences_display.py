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


from gi.repository import Adw, Gtk, Gdk


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/preferences_display.ui")
class PreferencesDisplay(Adw.ExpanderRow):
    __gtype_name__ = "PreferencesDisplay"

    # unit_comborow = Gtk.Template.Child()
    # lr_toggle = Gtk.Template.Child()
    # rl_toggle = Gtk.Template.Child()
    # compute_monitor_size = Gtk.Template.Child()
    # monitor_adjustment = Gtk.Template.Child()
    # use_default_font = Gtk.Template.Child()
    # font_name = Gtk.Template.Child()
    # use_default_color = Gtk.Template.Child()
    # fg_color = Gtk.Template.Child()
    # bg_color = Gtk.Template.Child()
    compute_monitor_size = Gtk.Template.Child()
    monitor_adjustment = Gtk.Template.Child()

    def __init__(self, monitor, monitors, settings) -> None:
        """Initialize the object."""

        super().__init__()

        self.monitors = monitors
        self.monitor = monitor
        self.settings = settings

        self.set_title(monitor.name)
        if monitor.diag_inch:
            self.monitor_adjustment.set_value(monitor.diag_inch)
        self.compute_monitor_size.set_active(monitor.compute)
        # monitor_adjustment = Gtk.Template.Child("monitor_adjustment")
        print(self.monitor_adjustment)
        print(type(self.monitor_adjustment))
        # self.set_title(title)
        # self.monitor_adjustment.set_value(diag)
        # self.application_window = application_window
        # self.settings = application_window.settings

        # # Length units
        # unit_list = Gio.ListStore.new(Unit)

        # unit_in_settings = self.settings.get_string("unit")
        # for i, unit in enumerate(UnitMng.array()):
        #     unit_list.append(Unit(unit["name"], unit["id"]))
        #     if unit["id"] == unit_in_settings:
        #         current_unit = i

        # self.unit_comborow.set_model(unit_list)
        # if current_unit:
        #     self.unit_comborow.set_selected(current_unit)
        # # Configure the handler after having set the initial value
        # self.unit_comborow.connect("notify::selected", self._on_unit)

        # # GSettings bindings
        # self.settings.bind(
        #     "direction-left-to-right",
        #     self.lr_toggle,
        #     "active",
        #     Gio.SettingsBindFlags.DEFAULT,
        # )
        # self.rl_toggle.set_active(not self.settings.get_boolean("direction-left-to-right"))

        # self.settings.bind(
        #     "compute-monitor-size",
        #     self.compute_monitor_size,
        #     "active",
        #     Gio.SettingsBindFlags.DEFAULT,
        # )
        # self.settings.bind(
        #     "monitor-size",
        #     self.monitor_adjustment,
        #     "value",
        #     Gio.SettingsBindFlags.DEFAULT,
        # )

        # self.settings.bind(
        #     "use-default-font",
        #     self.use_default_font,
        #     "active",
        #     Gio.SettingsBindFlags.DEFAULT,
        # )
        # self.settings.bind(
        #     "font-name", self.font_name, "label", Gio.SettingsBindFlags.DEFAULT
        # )

        # self.settings.bind(
        #     "use-default-color",
        #     self.use_default_color,
        #     "active",
        #     Gio.SettingsBindFlags.DEFAULT,
        # )

        # color_setting = self.settings.get_value("foreground-color")
        # color_rgba = Gdk.RGBA()
        # color_rgba.red = color_setting[0]
        # color_rgba.green = color_setting[1]
        # color_rgba.blue = color_setting[2]
        # color_rgba.alpha = color_setting[3]
        # self.fg_color.set_rgba(color_rgba)

        # color_setting = self.settings.get_value("background-color")
        # color_rgba = Gdk.RGBA()
        # color_rgba.red = color_setting[0]
        # color_rgba.green = color_setting[1]
        # color_rgba.blue = color_setting[2]
        # color_rgba.alpha = color_setting[3]
        # self.bg_color.set_rgba(color_rgba)

    @Gtk.Template.Callback()
    def _on_compute_monitor_size(self, widget, value) -> None:
        print("== _on_compute_monitor_size")
        print(value)
        # self.application_window.drawing_area.queue_draw()
        return Gdk.EVENT_PROPAGATE

    @Gtk.Template.Callback()
    def _monitor_size_changed_event(self, adjustment) -> None:
        print("== _monitor_size_changed_event")
        print(adjustment.get_value())
        # self.application_window.drawing_area.queue_draw()
        return Gdk.EVENT_PROPAGATE
