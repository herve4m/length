# main.py
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


import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gtk, Gio, Adw
from .window import LengthWindow
from .preferences import PreferencesDialog


class LengthApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version: str, application_id: str) -> None:
        """Initialize the object."""
        super().__init__(
            application_id=application_id, flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.create_action("quit", self.on_quit, ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action, ["<Control>comma"])
        self.version = version
        self.win = None
        self.about_dialog = None
        self.preferences_dialog = None

    def do_activate(self) -> None:
        """Called when the application is activated.

        Raise the application's main window, creating it if necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = LengthWindow(application=self)
        self.win.present()

    def on_quit(self, *args) -> None:
        self.win.on_close()
        self.quit()

    def on_about_action(self, *args) -> None:
        """Callback for the app.about action."""
        if not self.about_dialog:
            self.about_dialog = Adw.AboutDialog(
                application_name="Length",
                application_icon=self.get_application_id(),
                developer_name="Hervé Quatremain",
                version=self.version,
                developers=["Hervé Quatremain"],
                copyright="© 2025 Hervé Quatremain",
                issue_url="https://github.com/herve4m/length/issues",
                license_type=Gtk.License.GPL_3_0,
                website="https://github.com/herve4m/length",
            )
            # Translators: Replace "translator-credits" with your name/username,
            # and optionally an email or URL.
            self.about_dialog.set_translator_credits(_("translator-credits"))
        self.about_dialog.present()  # self.props.active_window)

    def on_preferences_action(self, widget, _) -> None:
        """Callback for the app.preferences action."""
        if not self.preferences_dialog:
            self.preferences_dialog = PreferencesDialog(self.win)
        self.preferences_dialog.present()

    def create_action(self, name: str, callback, shortcuts=None) -> None:
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version, application_id):
    """The application's entry point."""
    app = LengthApplication(version, application_id)
    return app.run(sys.argv)
