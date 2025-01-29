# unit.py
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

import math

from gi.repository import Pango, PangoCairo


class Unit:

    def __init__(self, monitor, context) -> None:
        """Initialize the object.

        :param monitor: The object that the method uses to convert the unit
                        into pixels.
        :type monitor: :py:class:``Gdk.Monitor``
        :param context: Object that stores the parameters for drawing the ruler
        :type monitor: :py:class:``DrawContext``
        """

        self._monitor = monitor
        self._monitor_geometry = monitor.get_geometry() if monitor else None
        self._ppmm = None

        self.context = context

    def _compute_ppmm(self) -> float:
        """Compute and return the number of pixels per millimeter (ppmm).

        The computation uses the user provided monitor diagonal size (in the
        ``monitor-size`` GSettings parameter).
        """

        if self._ppmm:
            return self._ppmm
        ppi = self.monitor_width / math.sqrt(
            (self.context.monitor_diagonal_inch**2)
            / (1 + (self.monitor_height / self.monitor_width) ** 2)
        )
        self._ppmm = ppi / 25.4  # Convert from inch to millimeter
        return self._ppmm

    @property
    def monitor_width(self) -> int:
        """Return the monitor width in pixels."""
        return self._monitor_geometry.width if self._monitor_geometry else 1280

    @property
    def monitor_height(self) -> int:
        """Return the monitor height in pixels."""
        return self._monitor_geometry.height if self._monitor_geometry else 720

    @property
    def ppmm_width(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the width."""

        # If the user specifies their monitor size through the Preferences
        # dialog, then use that size for computing the ppmm.
        if not self.context.compute_monitor_size:
            return self._compute_ppmm()

        if self._monitor and (mm := self._monitor.get_width_mm()):
            return self.monitor_width / mm
        else:
            # Some environments do not provide the monitor size (mm == 0).
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user
            self.context.warning()
            return self._compute_ppmm()

    @property
    def ppmm_height(self) -> float:
        """Return the number of pixels per millimeter (ppmm) for the height."""

        # If the user specifies their monitor size through the Preferences
        # dialog, then use that size for computing the ppmm.
        if not self.context.compute_monitor_size:
            return self._compute_ppmm()

        if self._monitor and (mm := self._monitor.get_height_mm()):
            return self.monitor_height / mm
        else:
            # Some environments do not provide the monitor size (mm == 0).
            # In that case, use a default monitor size of 24 inches, and
            # warn the the user
            self.context.warning()
            return self._compute_ppmm()

    def unit2tick(self, offset: float) -> int:
        """Convert an offset in ruler units into unit ticks."""
        return round(offset * self.unit_multiplier)

    def _draw_track(self, px_per_unit: int) -> None:
        """Draw the pointer tracker label and tick."""

        if not self.context.track_pointer:
            return

        if self.context.track_locked:
            x = self.context.track_pos
        elif self.context.is_horizontal:
            x = self.context.pointer_x
        else:
            x = self.context.pointer_y

        if x <= 0 or x >= self.context.width:
            return

        # Convert the x coordinate into unit coordinate
        if self.context.left2right:
            unit_x = x / px_per_unit + self.context.offset
        else:
            unit_x = (self.context.width - x) / px_per_unit + self.context.offset
        max_x = self.context.width / px_per_unit
        if px_per_unit == 1:
            # Do not show decimals
            label = str(round(unit_x))
            # Add a white space to get a little bit wider background box
            label_max = str(round(max_x)) + " "
        else:
            # Keep two decimals
            label = f"{unit_x:.2f}"
            # Add a white space to get a little bit wider background box
            label_max = f"{max_x:.2f} "

        ctx_text = CtxText(self.context.ctx, self.context.font_desc_small)
        # Compute the width of the widest label. This is used to draw the
        # background box
        extends_bg = ctx_text.get_extents(label_max)

        # Background box, which uses the foreground color
        self.context.ctx.set_source_rgba(*(self.context.color_fg))
        self.context.ctx.rectangle(
            x - extends_bg.width / 2,
            self.context.height / 2 - extends_bg.height / 2,
            extends_bg.width,
            extends_bg.height,
        )
        self.context.ctx.fill()

        # Line
        self.context.ctx.move_to(x, 0)
        self.context.ctx.line_to(x, self.context.height)
        self.context.ctx.stroke()

        if self.context.track_locked:
            # Background box border highlight when the pointer track is locked
            self.context.ctx.set_source_rgba(*(self.context.color_track))
            self.context.ctx.rectangle(
                x - extends_bg.width / 2 - 1,
                self.context.height / 2 - extends_bg.height / 2 - 1,
                extends_bg.width + 2,
                extends_bg.height + 2,
            )
            self.context.ctx.stroke()

        # Label in the box, which uses the background color
        extends = ctx_text.get_extents(label)
        self.context.ctx.set_source_rgba(*(self.context.color_bg))
        ctx_text.draw_text(
            x - extends.width / 2,
            self.context.height / 2 - extends.height / 2,
            label,
        )
        self.context.ctx.stroke()

    def draw(self):
        """Draw the ruler.

        Return a list (width, height) that provides the size that is required
        to draw the ruler. The caller can use this information to resize the
        drawing area.
        This returned parameter can be 0 if no resize is required.
        """

        ctx_text = CtxText(self.context.ctx, self.context.font_desc)
        self.context.ctx.set_line_width(1)
        self.context.ctx.set_source_rgba(*self.context.color_bg)
        self.context.ctx.rectangle(0, 0, self.context.width, self.context.height)
        self.context.ctx.fill()

        if self.context.height > self.context.width:
            self.context.is_horizontal = False
            self.context.ctx.translate(self.context.width, 0)
            self.context.ctx.rotate(math.pi / 2.0)
            self.context.height, self.context.width = (
                self.context.width,
                self.context.height,
            )
            px_per_tick = self.px_per_tick_height
        else:
            self.context.is_horizontal = True
            px_per_tick = self.px_per_tick_width

        offset = self.unit2tick(self.context.offset)

        # Verify whether the context height is sufficient for the drawing
        total_height = ctx_text.default_height + 2 * self.tick_max_length
        if total_height > self.context.height:
            return (0, total_height) if self.context.is_horizontal else (total_height, 0)

        ticks = sorted(self.ticks.keys())
        nb_tick_types = len(self.ticks)
        self.context.ctx.set_source_rgba(*self.context.color_fg)
        unit_name_displayed = False
        for unit_x in range(1 + offset, math.ceil(self.context.width / px_per_tick) + offset):

            # pos_x is the X coordinate of the tick
            if self.context.left2right:
                pos_x = (unit_x - offset) * px_per_tick + 0.5
            else:
                pos_x = self.context.width - ((unit_x - offset) * px_per_tick + 0.5)

            i = nb_tick_types - 1
            while i >= 0:
                if unit_x % ticks[i] == 0:
                    show_when_wide = self.ticks[ticks[i]]["show_when_wide"]
                    length = self.ticks[ticks[i]]["length"]
                    if self.ticks[ticks[i]]["label"]:
                        i = round(unit_x / self.unit_multiplier)
                        # Do not draw the unit if x < 50 to prevent it from
                        # being hidden by the menu button
                        if unit_name_displayed or pos_x < 50:
                            label = f"{i}"
                        else:
                            label = f"{i} {self.short_name}"
                            unit_name_displayed = True
                    else:
                        label = None
                    break
                i -= 1
            else:
                continue

            # Draw the tick
            self.context.ctx.move_to(pos_x, 0)
            self.context.ctx.line_to(pos_x, length)

            if label:
                e = ctx_text.get_extents(label)
                half_text_w = e.width / 2.0
                if pos_x + half_text_w < self.context.width:
                    x = pos_x - half_text_w
                else:
                    x = self.context.width - e.width - 1

                ctx_text.draw_text(x, self.tick_max_length, label)

                if self.context.height > 6 * e.height:
                    ctx_text.draw_text(
                        x, self.context.height - self.tick_max_length - e.height, label
                    )

            self.context.ctx.move_to(pos_x, self.context.height - length)
            self.context.ctx.line_to(pos_x, self.context.height)
            self.context.ctx.stroke()

            if show_when_wide and self.context.height > 10 * ctx_text.default_height:
                self.context.ctx.set_line_width(0.2)
                self.context.ctx.move_to(
                    pos_x, self.tick_max_length + ctx_text.default_height + 5
                )
                self.context.ctx.line_to(
                    pos_x,
                    self.context.height - self.tick_max_length - ctx_text.default_height - 5,
                )
                self.context.ctx.stroke()
                self.context.ctx.set_line_width(1)

        self.context.ctx.stroke()
        self._draw_track(px_per_tick * self.unit_multiplier)

        return (0, total_height) if self.context.is_horizontal else (total_height, 0)


class CtxText:
    def __init__(self, ctx, pango_font_description) -> None:
        """Initialize the object."""

        self.ctx = ctx
        self.font_desc = pango_font_description

        self.layout = PangoCairo.create_layout(self.ctx)
        self.layout.set_font_description(self.font_desc)

        # Compute the text height by using a sample string
        self.default_height = self.get_extents("0123456789pl").height

    def get_extents(self, text: str):
        """Return the size of the provided text in pixels."""

        self.layout.set_text(text)
        _, logical_extents = self.layout.get_extents()
        logical_extents.width = logical_extents.width / Pango.SCALE
        logical_extents.height = logical_extents.height / Pango.SCALE
        return logical_extents

    def draw_text(self, x: float, y: float, text: str) -> None:
        """Draw the text.

        :param x: X coordinate in Cairo units.
        :param y: Y coordinate in Cairo units.
        :param text: Text to display.
        """
        self.layout.set_text(text)
        self.ctx.move_to(x, y)
        PangoCairo.show_layout(self.ctx, self.layout)
