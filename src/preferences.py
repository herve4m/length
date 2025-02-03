# preferences.py
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

import gi
from gi.repository import Adw, Gtk, Gio, GObject, Pango, Gdk, GLib

from .unit_mng import UnitMng
from .preferences_display import PreferencesDisplay


class Unit(GObject.Object):
    __gtype_name__ = "Units"

    name = GObject.Property(type=str)
    id = GObject.Property(type=str)

    def __init__(self, name, id, **kwargs) -> None:
        """Initialize the object."""
        super().__init__(**kwargs)
        self.name: str = name
        self.id: str = id


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/preferences.ui")
class PreferencesDialog(Adw.PreferencesDialog):
    __gtype_name__ = "PreferencesDialog"

    unit_comborow = Gtk.Template.Child()
    lr_toggle = Gtk.Template.Child()
    rl_toggle = Gtk.Template.Child()
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxxx
    # compute_monitor_size = Gtk.Template.Child()
    # monitor_adjustment = Gtk.Template.Child()
    use_default_font = Gtk.Template.Child()
    font_name = Gtk.Template.Child()
    use_default_color = Gtk.Template.Child()
    fg_color = Gtk.Template.Child()
    bg_color = Gtk.Template.Child()
    display_group = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object."""

        super().__init__()

        self.application_window = application_window
        self.settings = application_window.settings
        self.monitors = application_window.monitors

        # Length units
        unit_list = Gio.ListStore.new(Unit)

        unit_in_settings = self.settings.get_string("unit")
        for i, unit in enumerate(UnitMng.array()):
            unit_list.append(Unit(unit["name"], unit["id"]))
            if unit["id"] == unit_in_settings:
                current_unit = i

        self.unit_comborow.set_model(unit_list)
        if current_unit:
            self.unit_comborow.set_selected(current_unit)
        # Configure the handler after having set the initial value
        self.unit_comborow.connect("notify::selected", self._on_unit)

        # GSettings bindings
        self.settings.bind(
            "direction-left-to-right",
            self.lr_toggle,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.rl_toggle.set_active(not self.settings.get_boolean("direction-left-to-right"))

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
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

        self.settings.bind(
            "use-default-font",
            self.use_default_font,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.settings.bind(
            "font-name", self.font_name, "label", Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            "use-default-color",
            self.use_default_color,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )

        color_setting = self.settings.get_value("foreground-color")
        color_rgba = Gdk.RGBA()
        color_rgba.red = color_setting[0]
        color_rgba.green = color_setting[1]
        color_rgba.blue = color_setting[2]
        color_rgba.alpha = color_setting[3]
        self.fg_color.set_rgba(color_rgba)

        color_setting = self.settings.get_value("background-color")
        color_rgba = Gdk.RGBA()
        color_rgba.red = color_setting[0]
        color_rgba.green = color_setting[1]
        color_rgba.blue = color_setting[2]
        color_rgba.alpha = color_setting[3]
        self.bg_color.set_rgba(color_rgba)

        for monitor in self.monitors.monitor_list:
            self.display_group.add(PreferencesDisplay(application_window, monitor))

    def sync_units(self, unit_id: str) -> None:
        """Ensure the unit combo box reflect the provided unit."""
        for i, unit in enumerate(UnitMng.array()):
            if unit["id"] == unit_id:
                self.unit_comborow.set_selected(i)
                break

    def _on_unit(self, _widget, _index) -> None:
        unit = self.unit_comborow.get_selected_item()
        self.settings.set_string("unit", unit.id)
        # Reset the offset when changing units
        self.settings.set_double("offset", 0.0)
        self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _lr_toggled(self, _widget) -> None:
        self.application_window.drawing_area.queue_draw()

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # @Gtk.Template.Callback()
    # def _on_compute_monitor_size(self, _widget, _value) -> None:
    #     self.application_window.drawing_area.queue_draw()

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # @Gtk.Template.Callback()
    # def _monitor_size_changed_event(self, adjustment) -> None:
    #     self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_use_default_font(self, _widget, _value) -> None:
        self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_font(self, _widget) -> None:
        font_name = self.settings.get_string("font-name")
        font_desc = Pango.font_description_from_string(font_name)
        dialog = Gtk.FontDialog(title=_("Select Font"))
        dialog.choose_font(self.application_window, font_desc, None, self._on_font_selected)

    def _on_font_selected(self, dialog, result) -> None:
        try:
            font_desc = dialog.choose_font_finish(result)
        except gi.repository.GLib.GError:
            # The user canceled the dialog
            return
        if font_desc:
            self.font_name.set_label(font_desc.to_string())
            self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_use_default_color(self, _widget, _value) -> None:
        self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_fg_color(self, *args) -> None:
        rgba = self.fg_color.get_rgba()
        if rgba.alpha:
            self.settings.set_value(
                "foreground-color",
                GLib.Variant("(dddd)", (rgba.red, rgba.green, rgba.blue, rgba.alpha)),
            )
            self.application_window.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_bg_color(self, *args) -> None:
        rgba = self.bg_color.get_rgba()
        if rgba.alpha:
            self.settings.set_value(
                "background-color",
                GLib.Variant("(dddd)", (rgba.red, rgba.green, rgba.blue, rgba.alpha)),
            )
            self.application_window.drawing_area.queue_draw()
