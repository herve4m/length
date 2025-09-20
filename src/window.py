# window.py
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
import math

from gi.repository import Adw, Gtk, Gdk, GLib

from .unit_mng import UnitMng
from .offset import OffsetControl
from .opacity import OpacityControl
from .pointer_tracking import PointerTrackingControl
from .scale import ScaleControl

from .orientation import OrientationControl
from .settings import Settings
from .draw_context import DrawContext, DEFAULT_COLOR_BG
from .monitor_mngt import MonitorMngt, Monitor

logger = logging.getLogger(__name__)


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/window.ui")
class LengthWindow(Adw.ApplicationWindow):
    """Length main window"""

    __gtype_name__ = "LengthWindow"

    drawing_area = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        """Initialize the object."""

        super().__init__(**kwargs)

        self.application = kwargs["application"]
        self.settings = Settings.new(self.application.get_application_id())
        self.monitors = MonitorMngt(self.settings)
        self.context = DrawContext(self.settings, self.monitors)
        self.unit_obj = None
        self.style_css_provider = Gtk.CssProvider()
        self.display = Gdk.Display.get_default()

        w, h = self.settings.get_value("window-size")
        self.set_default_size(w, h)

        popover = self.menu_button.get_popover()
        self.opacity_control = OpacityControl(self)
        popover.add_child(self.opacity_control, "opacity")
        self.pointer_tracking_control = PointerTrackingControl(self)
        popover.add_child(self.pointer_tracking_control, "pointer_tracking")
        self.offset_control = OffsetControl(self)
        popover.add_child(self.offset_control, "offset")
        self.scale_control = ScaleControl(self)
        popover.add_child(self.scale_control, "scale")
        self.orientation_control = OrientationControl(self)
        popover.add_child(self.orientation_control, "orientation")

        self.set_background_color()

    def draw(self, da, ctx, width: int, height: int) -> None:
        """Gtk.DrawingArea drawing function."""
        self.context.ctx = ctx
        self.context.width = width
        self.context.height = height
        self.context.diagonal = math.sqrt(width**2 + height**2)
        self.context.refresh_from_settings()

        unit = self.settings.get_string("unit")
        unit_class = UnitMng.get_unit_class(unit)
        self.unit_obj = unit_class(self.context)

        w, h = self.unit_obj.draw()
        if w:
            da.set_content_width(w)
        if h:
            da.set_content_height(h)

        self.offset_control.update_adjustment(unit, self.unit_obj)
        self.scale_control.update_adjustment(unit, self.unit_obj)
        self.orientation_control.update_orientation()

    def set_background_color(
        self, use_default_color: bool = None, opacity: int = None
    ) -> None:
        """Change the background color of Length."""
        if use_default_color is None:
            use_default_color = self.settings.get_boolean("use-default-color")
        if opacity is None:
            opacity = self.settings.get_int("opacity")

        rgba = Gdk.RGBA()
        rgba.alpha = opacity / 100.0
        if use_default_color:
            rgba.red = DEFAULT_COLOR_BG[0]
            rgba.green = DEFAULT_COLOR_BG[1]
            rgba.blue = DEFAULT_COLOR_BG[2]
        else:
            color_setting = self.settings.get_value("background-color")
            rgba.red = color_setting[0]
            rgba.green = color_setting[1]
            rgba.blue = color_setting[2]
        rgba_str = rgba.to_string()
        self.style_css_provider.load_from_string(
            f"window.length-main {{ background-color: {rgba_str}; }}"
        )
        Gtk.StyleContext.add_provider_for_display(
            self.display,
            self.style_css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def _on_enter_monitor(self, surface, monitor) -> None:
        """Switch monitor.

        The Gdk.Monitor object provides the physical monitor details. This
        object is used to retrieve the screen size in pixels and the physical
        size of the monitor.
        When the selected unit is centimeters, inches, picas, or points, these
        values are used to compute the number of pixels per unit.

        In some environments, the physical size of the monitor is not
        reported.

        :param surface: The surface object.
        :type surface: :py:class:``Gdk.Surface``
        :param monitor: The monitor object.
        :type monitor: :py:class:``Gdk.Monitor``
        """
        name = Monitor.get_name(monitor)
        logger.debug(f"Switching to monitor <{name}>")
        self.context.set_monitor(self.monitors.get_monitor(name))
        self.drawing_area.set_draw_func(self.draw)

    @Gtk.Template.Callback()
    def _on_map(self, win) -> None:
        """Retrieve the Gdk.Surface object for the ruler window, and listen to
        the enter-monitor signal to retrieve the Gdk.Monitor object.

        :param win: The application window.
        :type win: :py:class:``Adw.ApplicationWindow``
        """
        surface = win.get_surface()
        surface.connect("enter-monitor", self._on_enter_monitor)

    @Gtk.Template.Callback()
    def on_close(self, *args) -> None:
        """Save the window size in GSettings on exit."""
        self.settings.set_value("window-size", GLib.Variant("(ii)", self.get_default_size()))

    @Gtk.Template.Callback()
    def _on_key_pressed_event(self, event_ctrl_key, key_val, key_code, modifier_type) -> None:
        unit_changed = False
        unit_index = 0
        if key_val in (Gdk.KEY_Right, Gdk.KEY_Up):
            self.opacity_control.increment_value()
        elif key_val in (Gdk.KEY_Left, Gdk.KEY_Down):
            self.opacity_control.decrement_value()
        elif key_val == Gdk.KEY_1:
            unit_changed = True
            unit_index = 0
        elif key_val == Gdk.KEY_2:
            unit_changed = True
            unit_index = 1
        elif key_val == Gdk.KEY_3:
            unit_changed = True
            unit_index = 2
        elif key_val == Gdk.KEY_4:
            unit_changed = True
            unit_index = 3
        elif key_val == Gdk.KEY_5:
            unit_changed = True
            unit_index = 4
        elif key_val == Gdk.KEY_6:
            unit_changed = True
            unit_index = 5
        elif key_val == Gdk.KEY_7:
            unit_changed = True
            unit_index = 6
        elif key_val == Gdk.KEY_t:
            self.context.track_locked = False
            self.context.track_pointer = not self.context.track_pointer
            self.settings.set_boolean("track-pointer", self.context.track_pointer)
            self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_p:
            if self.context.track_pointer:
                self.context.track_locked = not self.context.track_locked
                self.context.track_pos_x = self.context.pointer_x
                self.context.track_pos_y = self.context.pointer_y
                self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_g:
            v = self.settings.get_boolean("show-grid")
            self.settings.set_boolean("show-grid", not v)
            self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_i:
            v = self.settings.get_boolean("show-diagonals")
            self.settings.set_boolean("show-diagonals", not v)
            self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_a:
            v = self.settings.get_boolean("show-angles")
            self.settings.set_boolean("show-angles", not v)
            self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_d:
            v = self.settings.get_boolean("direction-left-to-right")
            self.settings.set_boolean("direction-left-to-right", not v)
            self.drawing_area.queue_draw()

        #
        # You cannot programmatically rotate the window with Gtk 4. See
        # https://discourse.gnome.org/t/programmatically-set-window-size/31339/6
        #
        # elif key_val == Gdk.KEY_r:
        #     self.orientation_control.rotate()

        if unit_changed:
            id = UnitMng.array()[unit_index]["id"]
            unit_in_settings = self.settings.get_string("unit")
            if unit_in_settings != id:
                self.settings.set_string("unit", id)
                # Reset the offset when changing units
                self.settings.set_double("offset", 0.0)
                self.drawing_area.queue_draw()
                if self.application.preferences_dialog:
                    self.application.preferences_dialog.sync_units(id)

    @Gtk.Template.Callback()
    def _on_motion_event(self, event_controller_key, x: float, y: float) -> None:
        self.context.pointer_x = x
        self.context.pointer_y = y
        if self.context.track_pointer and not self.context.track_locked:
            self.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_leave_event(self, event_controller_key) -> None:
        if self.context.track_pointer and not self.context.track_locked:
            self.context.pointer_x = self.context.pointer_y = 0.0
            self.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_button_pressed_event(self, gesture, n_press: int, x: float, y: float) -> None:
        # Rotate on middle button click
        if gesture.get_current_button() == 2:
            self.orientation_control.rotate()
