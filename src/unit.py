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

    # The minimum ruler length for drawing the markings. If the width or height
    # of the drawing area is lower than this value, then the markings are
    # not drawn.
    MIN_LENGTH = 40

    def __init__(self, context) -> None:
        """Initialize the object.

        :param context: Object that stores the parameters for drawing the ruler
        :type context: :py:class:``DrawContext``
        """
        self.context = context

    def unit2tick(self, offset: float) -> int:
        """Convert an offset in ruler units into unit ticks."""
        return round(offset * self.unit_multiplier)

    def _draw_track_horizontal(self, min_size: int) -> None:
        """Draw the pointer tracking horizontal line.

        :param min_size: The minimum window width under which the pointer
                         tracking line is not drawn.
        :type min_size: int
        """
        if self.context.width < self.MIN_LENGTH or self.context.width <= min_size:
            return

        x = self.context.track_pos_x if self.context.track_locked else self.context.pointer_x
        if x <= 0 or x >= self.context.width:
            return

        px_per_unit = self.px_per_tick_width * self.unit_multiplier

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
        # background box.
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
            x - extends.width / 2, self.context.height / 2 - extends.height / 2, label
        )
        self.context.ctx.stroke()

    def _draw_track_vertical(self, min_size: int):
        """Draw the pointer tracking vertical line.

        :param min_size: The minimum window height under which the pointer
                         tracking line is not drawn.
        :type min_size: int
        """
        if self.context.height < self.MIN_LENGTH or self.context.height <= min_size:
            return

        y = self.context.track_pos_y if self.context.track_locked else self.context.pointer_y
        if y <= 0 or y >= self.context.height:
            return

        px_per_unit = self.px_per_tick_width * self.unit_multiplier

        # Convert the y coordinate into unit coordinate
        if self.context.left2right:
            unit_y = y / px_per_unit + self.context.offset
        else:
            unit_y = (self.context.height - y) / px_per_unit + self.context.offset
        max_y = self.context.height / px_per_unit
        if px_per_unit == 1:
            # Do not show decimals
            label = str(round(unit_y))
            # Add a white space to get a little bit wider background box
            label_max = str(round(max_y)) + " "
        else:
            # Keep two decimals
            label = f"{unit_y:.2f}"
            # Add a white space to get a little bit wider background box
            label_max = f"{max_y:.2f} "

        ctx_text = CtxText(self.context.ctx, self.context.font_desc_small)
        # Compute the width of the widest label. This is used to draw the
        # background box.
        extends_bg = ctx_text.get_extents(label_max)

        # Background box, which uses the foreground color
        self.context.ctx.set_source_rgba(*(self.context.color_fg))
        self.context.ctx.rectangle(
            self.context.width / 2 - extends_bg.width / 2,
            y - extends_bg.height / 2,
            extends_bg.width,
            extends_bg.height,
        )
        self.context.ctx.fill()

        # Line
        self.context.ctx.move_to(0, y)
        self.context.ctx.line_to(self.context.width, y)
        self.context.ctx.stroke()

        if self.context.track_locked:
            # Background box border highlight when the pointer track is locked
            self.context.ctx.set_source_rgba(*(self.context.color_track))
            self.context.ctx.rectangle(
                self.context.width / 2 - extends_bg.width / 2 - 1,
                y - extends_bg.height / 2 - 1,
                extends_bg.width + 2,
                extends_bg.height + 2,
            )
            self.context.ctx.stroke()

        # Label in the box, which uses the background color
        extends = ctx_text.get_extents(label)
        self.context.ctx.set_source_rgba(*(self.context.color_bg))
        ctx_text.draw_text(
            self.context.width / 2 - extends.width / 2, y - extends.height / 2, label
        )
        self.context.ctx.stroke()

    def _draw_horizontal(
        self,
        ctx_text,
        min_size: int,
        px_per_tick: float = 0.0,
        width: int = 0,
        height: int = 0,
    ) -> None:
        """Draw the horizontal markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window width under which the markings are
                         not drawn.
        :type min_size: int
        :param px_per_tick: Number of pixels per unit tick.
        :type px_per_tick: float
        :param width: Width of the drawing area.
        :type width: int
        :param height: Height of the drawing area.
        :type height: int
        """
        if width == 0:
            width = self.context.width
        if height == 0:
            height = self.context.height
        if px_per_tick == 0.0:
            px_per_tick = self.px_per_tick_width
        if width < self.MIN_LENGTH or width <= min_size:
            return

        offset = self.unit2tick(self.context.offset)
        ticks = sorted(self.ticks.keys())
        nb_tick_types = len(self.ticks)
        unit_name_displayed = False

        for unit_x in range(1 + offset, math.ceil(width / px_per_tick) + offset):
            # pos_x is the X coordinate of the tick
            if self.context.left2right:
                pos_x = (unit_x - offset) * px_per_tick + 0.5
            else:
                pos_x = width - ((unit_x - offset) * px_per_tick + 0.5)

            i = nb_tick_types - 1
            while i >= 0:
                if unit_x % ticks[i] == 0:
                    show_when_wide = self.ticks[ticks[i]]["show_when_wide"]
                    length = self.ticks[ticks[i]]["length"]

                    # Draw the label
                    if self.ticks[ticks[i]]["label"]:
                        tick_val = round(unit_x / self.unit_multiplier)
                        # Append the unit name to the label if the unit name
                        # has not been displayed yet
                        if not unit_name_displayed:
                            label = f"{tick_val} {self.short_name}"
                            e = ctx_text.get_extents(label)
                            half_text_w = e.width / 2.0
                            # If the label would overwrite the menu button,
                            # then do not show the unit name
                            if pos_x - half_text_w <= self.MIN_LENGTH:
                                label = f"{tick_val}"
                            else:
                                unit_name_displayed = True
                        else:
                            label = f"{tick_val}"

                        e = ctx_text.get_extents(label)
                        half_text_w = e.width / 2.0
                        # Do not draw the label if it goes beyound the width of
                        # the ruler
                        if pos_x + half_text_w < width:
                            x = pos_x - half_text_w
                            if x > self.MIN_LENGTH:
                                ctx_text.draw_text(x, self.tick_max_length, label)

                            # If the ruler is wide, then draw also the label at
                            # the bottom
                            if height > 6 * e.height:
                                ctx_text.draw_text(
                                    x, height - self.tick_max_length - e.height, label
                                )

                    break
                i -= 1
            else:
                continue

            # Draw the tick at the top
            self.context.ctx.move_to(pos_x, 0)
            self.context.ctx.line_to(pos_x, length)

            # Draw the tick at the bottom
            self.context.ctx.move_to(pos_x, height - length)
            self.context.ctx.line_to(pos_x, height)
            self.context.ctx.stroke()

            # Draw the grid
            if (
                show_when_wide
                and pos_x > self.MIN_LENGTH
                and width - pos_x > self.MIN_LENGTH
                and height > 10 * ctx_text.default_height
            ):
                self.context.ctx.set_line_width(0.2)
                self.context.ctx.move_to(
                    pos_x, self.tick_max_length + ctx_text.default_height + 5
                )
                self.context.ctx.line_to(
                    pos_x,
                    height - self.tick_max_length - ctx_text.default_height - 5,
                )
                self.context.ctx.stroke()
                self.context.ctx.set_line_width(1)

    def _draw_vertical(self, ctx_text, min_size: int) -> None:
        """Draw the vertical markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window heigh under which the markings are
                         not drawn.
        :type min_size: int
        """
        if self.context.height < self.MIN_LENGTH or self.context.height <= min_size:
            return

        # Rotate 90° and call the horizontal drawing method
        self.context.ctx.translate(self.context.width, 0)
        self.context.ctx.rotate(math.pi / 2.0)
        self._draw_horizontal(
            ctx_text,
            min_size,
            self.px_per_tick_height,
            self.context.height,
            self.context.width,
        )

        # Rotate back
        self.context.ctx.rotate(-math.pi / 2.0)
        self.context.ctx.translate(-self.context.width, 0)

    def draw(self):
        """Draw the ruler.

        Return a list (width, height) that provides the size that is required
        to draw the ruler. The caller can use this information to resize the
        drawing area.
        This returned parameter can be 0 if no resize is required.
        """
        ctx_text = CtxText(self.context.ctx, self.context.font_desc)

        # Minimum drawing area size to draw the labels and the ticks
        min_size = ctx_text.default_height + 2 * self.tick_max_length
        if min_size > self.context.width or min_size > self.context.height:
            return (
                min_size if min_size > self.context.width else 0,
                min_size if min_size > self.context.height else 0,
            )

        # Background
        self.context.ctx.set_source_rgba(*self.context.color_bg)
        self.context.ctx.rectangle(0, 0, self.context.width, self.context.height)
        self.context.ctx.fill()

        # Foreground context
        self.context.ctx.set_source_rgba(*self.context.color_fg)
        self.context.ctx.set_line_width(1)

        self._draw_horizontal(ctx_text, min_size)
        self._draw_vertical(ctx_text, min_size)

        if self.context.track_pointer:
            self._draw_track_horizontal(min_size)
            self._draw_track_vertical(min_size)

        return (min_size, min_size)


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
