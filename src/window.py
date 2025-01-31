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

from gi.repository import Adw, Gtk, Gdk, GLib  # , Graphene

from .unit_mng import UnitMng
from .opacity import OpacityControl
from .pointer_tracking import PointerTrackingControl
from .offset import OffsetControl

# from .orientation import OrientationControl
from .settings import Settings
from .draw_context import DrawContext


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
        self.context = DrawContext(self.settings)
        self.unit_obj = None

        popover = self.menu_button.get_popover()
        self.opacity_control = OpacityControl(self)
        popover.add_child(self.opacity_control, "opacity")
        self.pointer_tracking_control = PointerTrackingControl(self)
        popover.add_child(self.pointer_tracking_control, "pointer_tracking")
        self.offset_control = OffsetControl(self)
        popover.add_child(self.offset_control, "offset")
        # self.orientation_control = OrientationControl(self)
        # popover.add_child(self.orientation_control, "orientation")

        w, h = self.settings.get_value("window-size")
        self.set_default_size(w, h)

    def draw(self, da, ctx, width: int, height: int) -> None:
        """Gtk.DrawingArea drawing function."""

        self.context.ctx = ctx
        self.context.width = width
        self.context.height = height
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

    def _on_enter_monitor(self, surface, monitor):
        """Retrieve the Gdk.Monitor object from the Gdk.Surface.

        The Gdk.Monitor object provides the physical monitor details. This
        object is used to retrieve the screen size in pixels and the physical
        size of the monitor.
        When the selected unit is centimeters or inches, these values are
        used to compute the number of pixels per unit.

        In some environments, the physical size of the monitor is not
        reported. In that case the monitor-size configuration parameter is used.
        """
        self.context.set_monitor(monitor)
        self.drawing_area.set_draw_func(self.draw)

    @Gtk.Template.Callback()
    def on_map(self, win) -> None:
        """Retrieve the Gdk.Surface object for the ruler window, and listen to
        the enter-monitor signal to retrieve the Gdk.Monitor object."""
        surface = win.get_surface()
        surface.connect("enter-monitor", self._on_enter_monitor)

    @Gtk.Template.Callback()
    def on_close(self, *args) -> None:
        """Save the window side in GSettings on exit."""
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
        elif key_val == Gdk.KEY_t:
            self.context.track_locked = False
            self.context.track_pointer = not self.context.track_pointer
            self.settings.set_boolean("track-pointer", self.context.track_pointer)
            self.drawing_area.queue_draw()
        elif key_val == Gdk.KEY_p:
            if self.context.track_pointer:
                self.context.track_locked = not self.context.track_locked
                self.context.track_pos = (
                    self.context.pointer_x
                    if self.context.is_horizontal
                    else self.context.pointer_y
                )
                self.drawing_area.queue_draw()

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
            self.context.pointer_x = self.context.pointer_x = 0.0
            self.drawing_area.queue_draw()

    @Gtk.Template.Callback()
    def _on_button_pressed_event(self, gesture, n_press: int, x: float, y: float) -> None:
        # Middle button
        if gesture.get_current_button() == 2 and self.context.track_pointer:
            self.context.track_locked = not self.context.track_locked
            self.context.track_pos = x if self.context.is_horizontal else y
            self.drawing_area.queue_draw()
