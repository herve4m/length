# orientation.py
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

from gi.repository import Gtk

logger = logging.getLogger(__name__)


@Gtk.Template(resource_path="/io/github/herve4m/Length/ui/orientation.ui")
class OrientationControl(Gtk.Box):
    __gtype_name__ = "OrientationControl"

    h_toggle = Gtk.Template.Child()
    v_toggle = Gtk.Template.Child()

    def __init__(self, application_window) -> None:
        """Initialize the object."""
        super().__init__()
        self.application_window = application_window

    def update_orientation(self) -> None:
        """Update the toggle buttons according to the current orientation."""
        w, h = self.application_window.get_default_size()
        self.h_toggle.set_active(w > h)
        self.v_toggle.set_active(w <= h)

    @Gtk.Template.Callback()
    def _orientation_toggled(self, toggle) -> None:
        w, h = self.application_window.get_default_size()
        if toggle.get_active():
            if w < h:
                logger.debug(f"Going from vertical to horizontal w={w} h={h}")

                # Although the window should automatically change size when
                # setting the default size, it is not always the case. As a
                # workaround, maximizing, unmaximizing, and presenting the
                # window does the trick.
                self.application_window.set_default_size(h, w)
                self.application_window.maximize()
                self.application_window.unmaximize()
                self.application_window.present()
        else:
            if w > h:
                logger.debug(f"Going from horizontal to vertical w={w} h={h}")

                self.application_window.set_default_size(h, w)
                self.application_window.maximize()
                self.application_window.unmaximize()
                self.application_window.present()
