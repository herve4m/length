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
        if self.scalable and self.context.scale != 1.0:
            px_per_unit *= self.context.scale

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

        px_per_unit = self.px_per_tick_height * self.unit_multiplier
        if self.scalable and self.context.scale != 1.0:
            px_per_unit *= self.context.scale

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
        show_grid: bool = True,
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

        # If the unit is scalable and the scaling factor is not 1
        if self.scalable and round(self.context.scale, 2) != 1.0:
            px_per_tick *= self.context.scale
            # Scale indicator in the ruler to remind the user that a scale
            # factor is applied.
            # If there is not enough space between two ticks to display the
            # factor, then only display a (x).
            scale_indicator_long = f"(x{self.context.scale:.2f})"
            scale_indicator_short = "(x)"
        else:
            scale_indicator_long = scale_indicator_short = ""

        offset = self.unit2tick(self.context.offset)
        ticks = sorted(self.ticks.keys())
        nb_tick_types = len(self.ticks)
        unit_name_displayed = False
        scale_factor_displayed = False

        # Foreach unit tick
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
                        label = f"{tick_val}"
                        e = ctx_text.get_extents(label)
                        half_text_w = e.width / 2.0
                        # Do not draw the label if it goes beyond the width of
                        # the ruler
                        if pos_x + half_text_w < width:
                            x = pos_x - half_text_w
                            # Do not draw the label if it will overwrite the
                            # menu button
                            if x > self.MIN_LENGTH:
                                ctx_text.draw_text(x, self.tick_max_length, label)
                                # Draw unit after the first label
                                if not unit_name_displayed:
                                    ctx_text.draw_text(
                                        x + e.width + 2, self.tick_max_length, self.short_name
                                    )
                                    unit_name_displayed = True

                                # Draw the scaling factor in the tick
                                # following the unit
                                elif not scale_factor_displayed:
                                    # Compute the position of the next tick
                                    # to verify whether there is enough space
                                    # to draw the scaling factor
                                    if self.context.left2right:
                                        next_pos_x = (
                                            unit_x + ticks[i] - offset
                                        ) * px_per_tick + 0.5
                                    else:
                                        next_pos_x = width - (
                                            (unit_x - ticks[i] - offset) * px_per_tick + 0.5
                                        )
                                    scale_e = ctx_text.get_extents(scale_indicator_long)

                                    # Draw the full factor if enough space is available
                                    if x + e.width + 5 + scale_e.width < next_pos_x - 10:
                                        ctx_text.draw_text(
                                            x + e.width + 5,
                                            self.tick_max_length,
                                            scale_indicator_long,
                                        )

                                    # Otherwise, use the short version "(x)"
                                    else:
                                        ctx_text.draw_text(
                                            x + e.width + 5,
                                            self.tick_max_length,
                                            scale_indicator_short,
                                        )
                                    scale_factor_displayed = True

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
                show_grid
                and show_when_wide
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

    def _draw_vertical(self, ctx_text, min_size: int, show_grid: bool) -> None:
        """Draw the vertical markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window height under which the markings are
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
            show_grid,
            self.px_per_tick_height,
            self.context.height,
            self.context.width,
        )

        # Rotate back
        self.context.ctx.rotate(-math.pi / 2.0)
        self.context.ctx.translate(-self.context.width, 0)

    def px_per_tick_diagonal(self) -> float:
        angle = math.atan2(self.context.height, self.context.width)
        return math.sqrt(
            self.px_per_tick_width**2 * math.cos(angle) ** 2
            + self.px_per_tick_height**2 * math.sin(angle) ** 2
        )

    def _draw_diag_1(self, ctx_text, min_size: int) -> None:
        """Draw the diagonal markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window width and height under which the
                         markings are not drawn.
        :type min_size: int
        """
        if (
            self.context.width < self.MIN_LENGTH
            or self.context.width <= min_size
            or self.context.height < self.MIN_LENGTH
            or self.context.height <= min_size
        ):
            return

        px_per_tick = self.px_per_tick_diagonal()
        if self.scalable and self.context.scale != 1.0:
            px_per_tick *= self.context.scale
        width_per_diag = self.context.width / self.context.diagonal
        height_per_diag = self.context.height / self.context.diagonal
        offset_label_x = height_per_diag * self.tick_max_length / 2
        offset_label_y = width_per_diag * self.tick_max_length / 2

        offset = self.unit2tick(self.context.offset)
        ticks = sorted(self.ticks.keys())
        nb_tick_types = len(self.ticks)

        # Draw the diagonal
        self.context.ctx.set_line_width(0.2)
        # Do not draw on the menu button
        self.context.ctx.move_to(min_size * width_per_diag, min_size * height_per_diag)
        self.context.ctx.line_to(self.context.width, self.context.height)
        self.context.ctx.stroke()
        self.context.ctx.set_line_width(1)

        for unit_x in range(
            1 + offset, math.ceil(self.context.diagonal / px_per_tick) + offset
        ):
            if self.context.left2right:
                pos = (unit_x - offset) * px_per_tick
            else:
                pos = self.context.diagonal - ((unit_x - offset) * px_per_tick)
            # X and Y coordinates
            pos_x = pos * width_per_diag
            pos_y = pos * height_per_diag
            # Do not draw over the menu button
            if pos_x < min_size and pos_y < min_size:
                continue

            i = nb_tick_types - 1
            while i >= 0:
                if unit_x % ticks[i] == 0:
                    length = self.ticks[ticks[i]]["length"]

                    # Draw the label
                    if self.ticks[ticks[i]]["label"]:
                        tick_val = round(unit_x / self.unit_multiplier)
                        label = f"{tick_val}"
                        e = ctx_text.get_extents(label)
                        pos_label_x = pos_x + offset_label_x
                        pos_label_y = pos_y - offset_label_y - e.height
                        # Do not draw the label if it would overwrite the
                        # vertical or horizontal labels
                        if (
                            pos_label_x + e.width
                            < self.context.width - self.tick_max_length - e.height
                            and pos_label_x > self.tick_max_length + e.height
                            and pos_label_y
                            < self.context.height - self.tick_max_length - 2 * e.height
                            and pos_label_y > self.tick_max_length + e.height
                        ):
                            ctx_text.draw_text(pos_label_x, pos_label_y, label)
                    break
                i -= 1
            else:
                continue

            # Draw the tick
            offset_x = height_per_diag * length / 2
            offset_y = width_per_diag * length / 2
            self.context.ctx.move_to(pos_x + offset_x, pos_y - offset_y)
            self.context.ctx.line_to(pos_x - offset_x, pos_y + offset_y)
        self.context.ctx.stroke()

    def _draw_diag_2(self, ctx_text, min_size: int) -> None:
        """Draw the diagonal markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window width and height under which the
                         markings are not drawn.
        :type min_size: int
        """
        if (
            self.context.width < self.MIN_LENGTH
            or self.context.width <= min_size
            or self.context.height < self.MIN_LENGTH
            or self.context.height <= min_size
        ):
            return

        px_per_tick = self.px_per_tick_diagonal()
        if self.scalable and self.context.scale != 1.0:
            px_per_tick *= self.context.scale
        width_per_diag = self.context.width / self.context.diagonal
        height_per_diag = self.context.height / self.context.diagonal
        offset_label_x = height_per_diag * self.tick_max_length / 2
        offset_label_y = width_per_diag * self.tick_max_length / 2

        offset = self.unit2tick(self.context.offset)
        ticks = sorted(self.ticks.keys())
        nb_tick_types = len(self.ticks)

        # Draw the diagonal
        self.context.ctx.set_line_width(0.2)
        self.context.ctx.move_to(0, self.context.height)
        self.context.ctx.line_to(self.context.width, 0)
        self.context.ctx.stroke()
        self.context.ctx.set_line_width(1)

        for unit_x in range(
            1 + offset, math.ceil(self.context.diagonal / px_per_tick) + offset
        ):
            if self.context.left2right:
                pos = (unit_x - offset) * px_per_tick
            else:
                pos = self.context.diagonal - ((unit_x - offset) * px_per_tick)
            # X and Y coordinates
            pos_x = pos * width_per_diag
            pos_y = self.context.height - pos * height_per_diag

            i = nb_tick_types - 1
            while i >= 0:
                if unit_x % ticks[i] == 0:
                    length = self.ticks[ticks[i]]["length"]

                    # Draw the label
                    if self.ticks[ticks[i]]["label"]:
                        tick_val = round(unit_x / self.unit_multiplier)
                        label = f"{tick_val}"
                        e = ctx_text.get_extents(label)
                        pos_label_x = pos_x + offset_label_x
                        pos_label_y = pos_y + offset_label_y
                        # Do not draw the label if it would overwrite the
                        # vertical or horizontal labels
                        if (
                            pos_label_x + e.width
                            < self.context.width - self.tick_max_length - e.height
                            and pos_label_x > self.tick_max_length + e.height
                            and pos_label_y
                            < self.context.height - self.tick_max_length - 2 * e.height
                            and pos_label_y > self.tick_max_length + e.height
                        ):
                            ctx_text.draw_text(pos_label_x, pos_label_y, label)
                    break
                i -= 1
            else:
                continue

            # Draw the tick
            offset_x = height_per_diag * length / 2
            offset_y = width_per_diag * length / 2
            self.context.ctx.move_to(pos_x - offset_x, pos_y - offset_y)
            self.context.ctx.line_to(pos_x + offset_x, pos_y + offset_y)
        self.context.ctx.stroke()

    def _draw_angles(self, ctx_text, min_size: int) -> None:
        """Draw the angle markings.

        :param ctx_text: The text context.
        :type ctx_text: :py:class:``CtxText``
        :param min_size: The minimum window width and height under which the
                         markings are not drawn.
        :type min_size: int
        """
        if (
            self.context.width < self.MIN_LENGTH
            or self.context.width <= min_size
            or self.context.height < self.MIN_LENGTH
            or self.context.height <= min_size
        ):
            return

        width_per_diag = self.context.width / self.context.diagonal
        height_per_diag = self.context.height / self.context.diagonal

        # ________________________________
        # |\    1a                 1b   /|
        # |   \                      /   |
        # | 2a   \                /   2b |
        # |         \     3    /         |
        # |             \  /             |
        # |           4                  |
        # |            /   \             |
        # |         /          \         |
        # | 2c   /                \   2d |
        # |   /                      \   |
        # |/   1c                 1d   \ |
        # --------------------------------

        # Compute the angles
        angle_1 = math.asin(self.context.height / self.context.diagonal)
        angle_deg_1 = math.degrees(angle_1)
        legend_1 = f"{angle_deg_1:.1f}°"
        extend_1 = ctx_text.get_extents(legend_1)
        radius_1 = self.context.width / 3

        angle_2 = math.pi / 2 - angle_1
        angle_deg_2 = 90 - angle_deg_1
        legend_2 = f"{angle_deg_2:.1f}°"
        extend_2 = ctx_text.get_extents(legend_2)
        radius_2 = self.context.height / 3

        legend_3 = f"{2 * angle_deg_2:.1f}°"
        extend_3 = ctx_text.get_extents(legend_3)
        radius_3 = self.context.height / 10

        legend_4 = f"{2 * angle_deg_1:.1f}°"
        extend_4 = ctx_text.get_extents(legend_4)
        radius_4 = self.context.width / 10

        # Compute the legend positions
        legend_x_1a = radius_1 * math.cos(angle_1 / 2)
        legend_y_1a = radius_1 * math.sin(angle_1 / 2)

        legend_x_1b = self.context.width - legend_x_1a - extend_1.width
        legend_y_1b = legend_y_1a

        legend_x_1c = legend_x_1a
        legend_y_1c = self.context.height - legend_y_1a - extend_1.height

        legend_x_1d = self.context.width - legend_x_1a - extend_1.width
        legend_y_1d = self.context.height - legend_y_1a - extend_1.height

        legend_x_2a = radius_2 * math.cos((math.pi - angle_2) / 2)
        legend_y_2a = radius_2 * math.sin((math.pi - angle_2) / 2)

        legend_x_2b = self.context.width - legend_x_2a - extend_2.width
        legend_y_2b = legend_y_2a

        legend_x_2c = legend_x_2a
        legend_y_2c = self.context.height - legend_y_2a - extend_2.height

        legend_x_2d = self.context.width - legend_x_2a - extend_2.width
        legend_y_2d = self.context.height - legend_y_2a - extend_2.height

        legend_x_3 = self.context.width / 2 - extend_3.width / 2
        legend_y_3 = self.context.height / 2 - radius_3 - extend_3.height

        legend_x_4 = self.context.width / 2 + radius_4 + 2
        legend_y_4 = self.context.height / 2 - extend_4.height / 2

        # Draw the diagonals
        self.context.ctx.set_line_width(1)
        # Do not draw on the menu button
        self.context.ctx.move_to(min_size * width_per_diag, min_size * height_per_diag)
        self.context.ctx.line_to(self.context.width, self.context.height)
        self.context.ctx.move_to(0, self.context.height)
        self.context.ctx.line_to(self.context.width, 0)
        self.context.ctx.stroke()

        # 1a
        self.context.ctx.arc(0, 0, radius_1, 0, angle_1)
        ctx_text.draw_text(legend_x_1a, legend_y_1a, legend_1)
        self.context.ctx.stroke()

        # 1b
        self.context.ctx.arc(self.context.width, 0, radius_1, math.pi - angle_1, math.pi)
        ctx_text.draw_text(legend_x_1b, legend_y_1b, legend_1)
        self.context.ctx.stroke()

        # 1c
        self.context.ctx.arc(0, self.context.height, radius_1, -angle_1, 0)
        ctx_text.draw_text(legend_x_1c, legend_y_1c, legend_1)
        self.context.ctx.stroke()

        # 1d
        self.context.ctx.arc(
            self.context.width, self.context.height, radius_1, math.pi, math.pi + angle_1
        )
        ctx_text.draw_text(legend_x_1d, legend_y_1d, legend_1)
        self.context.ctx.stroke()

        # 2a
        self.context.ctx.arc(0, 0, radius_2, angle_1, math.pi / 2)
        ctx_text.draw_text(legend_x_2a, legend_y_2a, legend_2)
        self.context.ctx.stroke()

        # 2b
        self.context.ctx.arc(self.context.width, 0, radius_2, math.pi / 2, math.pi - angle_1)
        ctx_text.draw_text(legend_x_2b, legend_y_2b, legend_2)
        self.context.ctx.stroke()

        # 2c
        self.context.ctx.arc(0, self.context.height, radius_2, 3 * math.pi / 2, -angle_1)
        ctx_text.draw_text(legend_x_2c, legend_y_2c, legend_2)
        self.context.ctx.stroke()

        # 2d
        self.context.ctx.arc(
            self.context.width, self.context.height, radius_2, math.pi + angle_1, -math.pi / 2
        )
        ctx_text.draw_text(legend_x_2d, legend_y_2d, legend_2)
        self.context.ctx.stroke()

        # 3
        self.context.ctx.arc(
            self.context.width / 2,
            self.context.height / 2,
            radius_3,
            math.pi + angle_1,
            -angle_1,
        )
        ctx_text.draw_text(legend_x_3, legend_y_3, legend_3)
        self.context.ctx.stroke()

        # 4
        self.context.ctx.arc(
            self.context.width / 2, self.context.height / 2, radius_4, -angle_1, angle_1
        )
        ctx_text.draw_text(legend_x_4, legend_y_4, legend_4)
        self.context.ctx.stroke()

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

        # Foreground context
        self.context.ctx.set_source_rgba(*self.context.color_fg)
        self.context.ctx.set_line_width(1)

        if self.context.settings.get_boolean("show-markings"):
            # Whether do draw the grid
            show_grid = self.context.settings.get_boolean("show-grid")
            self._draw_horizontal(ctx_text, min_size, show_grid)
            self._draw_vertical(ctx_text, min_size, show_grid)

        if self.context.settings.get_boolean("show-diagonals"):
            self._draw_diag_1(ctx_text, min_size)
            self._draw_diag_2(ctx_text, min_size)

        if self.context.settings.get_boolean("show-angles"):
            self._draw_angles(ctx_text, min_size)

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
