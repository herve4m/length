# settings.py
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

from gi.repository import Gio


class Settings(Gio.Settings):
    def __init__(self) -> None:
        """Initialize the object."""
        super().__init__()

    @classmethod
    def new(cls, schema_id: str, path: str):
        # The schema is relocatable (it does not declare a fixed path), so the
        # storage path must be provided at run time. This is what allows each
        # instance to keep its settings separate.
        settings = Gio.Settings.new_with_path(schema_id, path)
        settings.__class__ = Settings
        return settings
