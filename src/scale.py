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

from gi.repository import Gtk  # , Gio, Gdk


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/scale.ui")
class ScaleControl(Gtk.Box):
    """Manage the scale factor of the Length units."""

    __gtype_name__ = "ScaleControl"

    scale_label = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object.

        :param application_window: The main Length application window
        :type application_window: :py:class:``Gtk.ApplicationWindow``
        """
        super().__init__()

        self.application_window = application_window
        self.scale: float = application_window.settings.get_double("scale")
        self.scale_label.set_label(f"{self.scale}")

        # self.display = Gdk.Display.get_default()
        # self.opacity_value = application_window.settings.get_int("opacity")
        # self.opacity_label.set_label(f"{self.opacity_value}%")
        # application_window.settings.bind(
        #     "opacity", self.opacity_adjustment, "value", Gio.SettingsBindFlags.DEFAULT
        # )

    # def increment_value(self) -> None:
    #     """Increase the opacity of the Length application window.

    #     Keyboard events (up and right arrow keys) call this method, which
    #     increments the opacity in 10% steps.
    #     """
    #     self.opacity_value += 10
    #     if self.opacity_value > 100:
    #         self.opacity_value = 100
    #     self.opacity_adjustment.set_value(self.opacity_value)

    # def decrement_value(self) -> None:
    #     """Decrease the opacity of the Length application window.

    #     Keyboard events (down and left arrow keys) call this method, which
    #     decrements the opacity in 10% steps.
    #     """
    #     self.opacity_value -= 10
    #     if self.opacity_value < 0:
    #         self.opacity_value = 0
    #     self.opacity_adjustment.set_value(self.opacity_value)

    def set_label(self):
        self.scale = round(self.scale, 1)
        if self.scale > 0.0:
            self.application_window.settings.set_double("scale", self.scale)
            self.scale_label.set_label(f"{self.scale}")

    @Gtk.Template.Callback()
    def _scale_in(self, _widget) -> None:
        """Update the opacity of the Length application window.

        The opacity is synchronized with the alpha channel of the background
        color.

        :param adjustment: The Gtk Adjustment object that the method uses to
                           retrieve the opacity percentage.
        :type adjustment: :py:class:``Gtk.Adjustment``
        """
        # self.opacity_value = int(adjustment.get_value())
        self.scale += 0.1
        self.set_label()
        # self.application_window.set_background_color(opacity=self.opacity_value)

    @Gtk.Template.Callback()
    def _scale_out(self, _widget) -> None:
        """Update the opacity of the Length application window.

        The opacity is synchronized with the alpha channel of the background
        color.

        :param adjustment: The Gtk Adjustment object that the method uses to
                           retrieve the opacity percentage.
        :type adjustment: :py:class:``Gtk.Adjustment``
        """
        # self.opacity_value = int(adjustment.get_value())
        self.scale -= 0.1
        if self.scale > 0.0:
            self.scale -= 0.1
        self.set_label()
        # self.application_window.set_background_color(opacity=self.opacity_value)

    @Gtk.Template.Callback()
    def _scale_reset(self, _widget) -> None:
        """Update the opacity of the Length application window.

        The opacity is synchronized with the alpha channel of the background
        color.

        :param adjustment: The Gtk Adjustment object that the method uses to
                           retrieve the opacity percentage.
        :type adjustment: :py:class:``Gtk.Adjustment``
        """
        # self.opacity_value = int(adjustment.get_value())
        self.scale = 1.0
        self.set_label()
        # self.application_window.set_background_color(opacity=self.opacity_value)
