# main.py
#
# Copyright 2025, 2026 Hervé Quatremain
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
import logging
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gtk, Gio, Adw, GLib, Gdk
from .window import LengthWindow
from .preferences import PreferencesDialog


class LengthApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version: str, application_id: str, instance_id: int = None) -> None:
        """Initialize the object.

        :param version: The application version.
        :param application_id: The base application ID, which is also the
                               GSettings schema ID.
        :param instance_id: When set, run as an independent instance that keeps
                            its settings separate from the other instances. The
                            default instance (``None``) keeps the regular
                            single-instance behavior.
        """
        flags = Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        # Independent instances must be allowed to coexist as separate
        # processes instead of forwarding to the already-running one. Keeping
        # the base application ID (rather than a per-instance ID) ensures the
        # windows still match the installed desktop file and icon.
        if instance_id is not None:
            flags |= Gio.ApplicationFlags.NON_UNIQUE
        super().__init__(application_id=application_id, flags=flags)

        self.set_resource_base_path("/io/github/herve4m/Length")

        # The schema is relocatable and shares the ID of the application. The
        # storage path follows the GNOME convention (the ID with the dots
        # replaced by slashes); independent instances use a dedicated subpath.
        self.schema_id = application_id
        base_path = "/" + application_id.replace(".", "/") + "/"
        if instance_id is None:
            self.settings_path = base_path
        else:
            self.settings_path = f"{base_path}instance{instance_id}/"

        # Command-line options
        opt = GLib.OptionEntry()
        opt.long_name = "version"
        opt.flags = GLib.OptionFlags.NONE
        opt.arg_data = None
        opt.description = "Output version information and exit"
        options = [opt]

        opt = GLib.OptionEntry()
        opt.long_name = "debug"
        opt.flags = GLib.OptionFlags.NONE
        opt.arg_data = None
        opt.description = "Output debug messages"
        options.append(opt)

        # The value of this option is consumed before the application is built
        # (see the main() function). It is still registered here so that it
        # appears in --help and is accepted by the command-line parser.
        opt = GLib.OptionEntry()
        opt.long_name = "instance-id"
        opt.short_name = ord("i")
        opt.flags = GLib.OptionFlags.NONE
        opt.arg = GLib.OptionArg.INT
        opt.arg_data = None
        opt.description = "Run an independent instance with its own settings"
        opt.arg_description = "N"
        options.append(opt)

        self.add_main_option_entries(options)

        self.create_action("preferences", self.on_preferences_action, ["<Control>comma"])
        self.create_action("help", self.on_help_action, ["F1"])
        self.create_action("about", self.on_about_action)
        self.create_action("quit", self.on_quit, ["<primary>q"])
        self.version = version
        self.win = None
        self.preferences_dialog = None
        # self.help_launcher = None
        self.about_dialog = None

    def do_command_line(self, command_line) -> int:
        """Process command-line options.

        :param command_line: The command-line options.
        :type command_line: :py:class:``Gio.ApplicationCommandLine``
        """
        # options type GVariantDict
        options = command_line.get_options_dict()

        # Convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "version" in options:
            print(f"""Length {self.version}
Copyright (C) 2025, 2026 Hervé Quatremain
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""")
            return 0
        if "debug" in options:
            logging.basicConfig(level=logging.DEBUG)

        self.activate()
        return 0

    def do_activate(self) -> None:
        """Called when the application is activated.

        Raise the application's main window, creating it if necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = LengthWindow(application=self)
        self.win.present()

    def on_preferences_action(self, widget, _) -> None:
        """Callback for the app.preferences action."""
        if not self.preferences_dialog:
            self.preferences_dialog = PreferencesDialog(self.win)
        self.preferences_dialog.present()

    # Does not work with flatpak.
    # See https://gitlab.gnome.org/GNOME/gtk/-/issues/6135
    #
    # def _on_help_action_finish(self, obj, res) -> None:
    #     """Callback for the help launcher."""
    #     try:
    #         self.help_launcher.launch_finish(res)
    #     except GLib.GError:
    #         pass
    #
    # def on_help_action(self, *args) -> None:
    #     """Callback for the app.help action."""
    #     if not self.help_launcher:
    #         self.help_launcher = Gtk.UriLauncher()
    #         self.help_launcher.set_uri("help:length")
    #     self.help_launcher.launch(self.win, None, self._on_help_action_finish)

    def on_help_action(self, *args) -> None:
        """Callback for the app.help action."""
        Gtk.show_uri(self.win, "help:length", Gdk.CURRENT_TIME)

    def on_about_action(self, *args) -> None:
        """Callback for the app.about action."""
        if not self.about_dialog:
            self.about_dialog = Adw.AboutDialog(
                application_name="Length",
                application_icon=self.get_application_id(),
                developer_name="Hervé Quatremain",
                version=self.version,
                developers=["Hervé Quatremain"],
                copyright="© 2025, 2026 Hervé Quatremain",
                issue_url="https://github.com/herve4m/length/issues",
                license_type=Gtk.License.GPL_3_0,
                website="https://github.com/herve4m/length",
            )
            # Translators: Replace "translator-credits" with your name/username,
            # and optionally an email or URL.
            self.about_dialog.set_translator_credits(_("translator-credits"))
        self.about_dialog.present()  # self.props.active_window)

    def on_quit(self, *args) -> None:
        self.win.on_close()
        self.quit()

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


def _parse_instance_id(argv):
    """Extract the --instance-id/-i value from the command-line arguments.

    The application ID uniqueness flag and the settings path depend on this
    value, both of which must be known before the application is built and
    registered on the bus. The normal command-line handling (do_command_line)
    runs too late for that, so the value is read directly from ``argv`` here.

    :param argv: The command-line arguments (including the program name).
    :return: The instance number as a positive integer, or ``None`` when the
             option is absent.
    :raises ValueError: When the option is present but its value is not a
                        positive integer.
    """
    raw = None
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--instance-id" or arg == "-i":
            raw = argv[i + 1] if i + 1 < len(argv) else ""
            i += 2
            continue
        if arg.startswith("--instance-id="):
            raw = arg.split("=", 1)[1]
        elif arg.startswith("-i") and len(arg) > 2:
            raw = arg[2:]
        i += 1

    if raw is None:
        return None
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"invalid instance ID '{raw}': expected a positive integer")
    if value < 1:
        raise ValueError(f"invalid instance ID '{raw}': expected a positive integer")
    return value


def main(version, application_id):
    """The application's entry point."""
    try:
        instance_id = _parse_instance_id(sys.argv)
    except ValueError as e:
        print(f"length: {e}", file=sys.stderr)
        return 1
    app = LengthApplication(version, application_id, instance_id)
    return app.run(sys.argv)
