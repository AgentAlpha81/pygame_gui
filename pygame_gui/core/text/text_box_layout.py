from typing import Deque

import pygame

from pygame.surface import Surface

from pygame_gui.core.text.text_layout_rect import TextLayoutRect
from pygame_gui.core.text.line_break_layout_rect import LineBreakLayoutRect


class TextBoxLayoutRow(pygame.Rect):
    """
    A single line of text-like stuff to be used in a text box type layout.
    """

    def __init__(self, row_start_y):
        super().__init__(0, row_start_y, 0, 0)
        self.items = []

    def at_start(self):
        """
        Returns true if this row has no items in it.

        :return: True if we are at the start of the row.
        """
        return not self.items

    def add_item(self, item: TextLayoutRect):
        """
        Add a new item to the row. Items are added left to right.

        If you wanted to built a right to left writing system layout,
        changing this might be a good place to start.

        :param item: The new item to add to the text row
        """
        if not self.items:
            # first item
            self.left = item.left  # noqa pylint: disable=attribute-defined-outside-init; pylint getting confused
        self.items.append(item)
        self.width += item.width  # noqa pylint: disable=attribute-defined-outside-init; pylint getting confused
        if item.height > self.height:
            self.height = item.height  # noqa pylint: disable=attribute-defined-outside-init; pylint getting confused

    def rewind_row(self, layout_rect_queue):
        """
        Use this to add items from the row back onto a layout queue, useful if we've added
        something to the layout that means that this row needs to be re-run through the
        layout code.

        :param layout_rect_queue: A layout queue that contains items to be laid out in order.
        """
        for rect in reversed(self.items):
            layout_rect_queue.appendleft(rect)

        self.items.clear()
        self.width = 0  # pylint: disable=attribute-defined-outside-init; pylint getting confused
        self.height = 0  # pylint: disable=attribute-defined-outside-init; pylint getting confused
        self.x = 0  # noqa pylint: disable=attribute-defined-outside-init,invalid-name; this name is inherited from the base class


class TextBoxLayout:
    """
    Class to layout multiple lines of text to fit in a defined column.

    The base of the 'column' rectangle is set once the data supplied has been laid out
    to fit in the width provided.
    """
    def __init__(self,
                 input_data_queue: Deque[TextLayoutRect],
                 layout_rect: pygame.Rect):
        # TODO: supply only a width and create final rect shape or just a final height?
        self.imput_data_rect_queue = input_data_queue.copy()
        self.layout_rect = layout_rect.copy()

        self.layout_rect_queue = None
        self.finalised_surface = None
        self.floating_rects = []
        self.layout_rows = []
        self.link_chunks = []

        self._process_layout_queue()

    def reprocess_layout_queue(self, layout_rect):
        """
        Re-lays out already parsed text data. Useful to call if the layout requirements have
        changed but the text data hasn't.

        :param layout_rect: The new layout rectangle.
        """
        self.layout_rect = layout_rect
        self.layout_rect_queue = None
        self.finalised_surface = None
        self.floating_rects = []
        self.layout_rows = []

        self._process_layout_queue()

    def _process_layout_queue(self):
        self.layout_rect_queue = self.imput_data_rect_queue.copy()
        current_row = TextBoxLayoutRow(row_start_y=0)
        while self.layout_rect_queue:

            test_layout_rect = self.layout_rect_queue.popleft()
            test_layout_rect.topleft = tuple(current_row.topright)

            if isinstance(test_layout_rect, LineBreakLayoutRect):
                current_row = self._handle_line_break_rect(current_row, test_layout_rect)
            elif test_layout_rect.should_span():
                current_row = self._handle_span_rect(current_row, test_layout_rect)
            elif test_layout_rect.float_pos() != TextLayoutRect.FLOAT_NONE:
                current_row = self._handle_float_rect(current_row, test_layout_rect)
            else:
                current_row = self._handle_regular_rect(current_row, test_layout_rect)
        # make sure we add the last row to the layout
        self._add_row_to_layout(current_row)

    def _add_row_to_layout(self, current_row):
        self.layout_rows.append(current_row)
        if current_row.bottom > self.layout_rect.height:
            self.layout_rect.height = current_row.bottom

    def _handle_regular_rect(self, current_row, test_layout_rect):

        rhs_limit = self.layout_rect.width
        for floater in self.floating_rects:
            if floater.vertical_overlap(test_layout_rect):
                if (current_row.at_start() and
                        floater.float_pos() == TextLayoutRect.FLOAT_LEFT):
                    # if we are at the start of a new line see if this rectangle
                    # will overlap with any left aligned floating rectangles
                    test_layout_rect.left = floater.right
                elif floater.float_pos() == TextLayoutRect.FLOAT_RIGHT:
                    if floater.left < rhs_limit:
                        rhs_limit = floater.left
        # See if this rectangle will fit on the current line
        if test_layout_rect.right > rhs_limit:
            # move to next line and try to split if we can
            current_row = self._split_rect_and_move_to_next_line(current_row,
                                                                 rhs_limit,
                                                                 test_layout_rect)
        else:
            current_row.add_item(test_layout_rect)
        return current_row

    def _handle_float_rect(self, current_row, test_layout_rect):
        max_floater_line_height = current_row.height
        if test_layout_rect.float_pos() == TextLayoutRect.FLOAT_LEFT:
            test_layout_rect.left = 0
            for floater in self.floating_rects:
                if (floater.vertical_overlap(test_layout_rect)
                        and floater.float_pos() == TextLayoutRect.FLOAT_LEFT):
                    test_layout_rect.left = floater.right
                    if max_floater_line_height < floater.height:
                        max_floater_line_height = floater.height
            if test_layout_rect.right > self.layout_rect.width:
                # If this rectangle won't fit, we see if we can split it
                current_row = self._split_rect_and_move_to_next_line(
                    current_row,
                    self.layout_rect.width,
                    test_layout_rect,
                    max_floater_line_height)
            else:
                self.floating_rects.append(test_layout_rect)
                # expand overall rect bottom to fit if needed
                if test_layout_rect.bottom > self.layout_rect.height:
                    self.layout_rect.height = test_layout_rect.bottom
                # rewind current text row so we can account for new floating rect
                current_row.rewind_row(self.layout_rect_queue)

        else:  # FLOAT_RIGHT
            rhs_limit = self.layout_rect.width
            for floater in self.floating_rects:
                if (floater.vertical_overlap(test_layout_rect)
                        and floater.float_pos() == TextLayoutRect.FLOAT_RIGHT
                        and floater.left < rhs_limit):
                    rhs_limit = floater.left
                    if max_floater_line_height < floater.height:
                        max_floater_line_height = floater.height
            test_layout_rect.right = rhs_limit
            if test_layout_rect.left < 0:
                # If this rectangle won't fit, we see if we can split it
                current_row = self._split_rect_and_move_to_next_line(
                    current_row,
                    self.layout_rect.width,
                    test_layout_rect,
                    max_floater_line_height)
            else:
                self._add_floating_rect(current_row, test_layout_rect)
        return current_row

    def _add_floating_rect(self, current_row, test_layout_rect):
        self.floating_rects.append(test_layout_rect)
        # expand overall rect bottom to fit if needed
        if test_layout_rect.bottom > self.layout_rect.height:
            self.layout_rect.height = test_layout_rect.bottom
        # rewind current text row so we can account for new floating rect
        current_row.rewind_row(self.layout_rect_queue)

    def _handle_span_rect(self, current_row, test_layout_rect):
        if not current_row.at_start():
            # not at start of line so end current row...
            self._add_row_to_layout(current_row)
            # ...and start new one
            current_row = TextBoxLayoutRow(row_start_y=current_row.bottom)

        # Make the rect span the current row's full width & add it to the row
        test_layout_rect.width = self.layout_rect.width  # TODO: floating rects?
        current_row.add_item(test_layout_rect)

        # add the row to the layout since it's now full up after spanning the full width...
        self._add_row_to_layout(current_row)
        # ...then start a new row
        current_row = TextBoxLayoutRow(row_start_y=current_row.bottom)
        return current_row

    def _handle_line_break_rect(self, current_row, test_layout_rect):
        # line break, so first end current row...
        current_row.add_item(test_layout_rect)
        self._add_row_to_layout(current_row)

        # ...then start a new row
        return TextBoxLayoutRow(row_start_y=current_row.bottom)

    def _split_rect_and_move_to_next_line(self, current_row, rhs_limit,
                                          test_layout_rect,
                                          floater_height=None):
        # TODO: move floating rect stuff out of here? Right now there is no splitting and the height
        #       is different

        if test_layout_rect.can_split():
            split_point = rhs_limit - test_layout_rect.left
            new_layout_rect = test_layout_rect.split(split_point)
            if new_layout_rect is not None:
                # split successfully...

                # add left side of rect onto current line
                current_row.add_item(test_layout_rect)
                # put right of rect back on the queue and move layout position down a line
                self.layout_rect_queue.appendleft(new_layout_rect)
            else:
                # failed to split, have to move whole chunk down a line.
                self.layout_rect_queue.appendleft(test_layout_rect)
        else:
            # can't split, have to move whole chunk down a line.
            self.layout_rect_queue.appendleft(test_layout_rect)

        # whether we split successfully or not, we need to end the current row...
        self._add_row_to_layout(current_row)

        # And then start a new one.
        if floater_height is not None:
            return TextBoxLayoutRow(row_start_y=floater_height)
        else:
            return TextBoxLayoutRow(row_start_y=current_row.bottom)

    def finalise_to_surf(self, surface: Surface):
        """
        Take this layout, with everything positioned in the correct place and finalise it to
        a surface.

        May be called again after changes to the layout? Update surf?

        :param surface: The surface we are going to blit the contents of this layout onto.
        """
        for row in self.layout_rows:
            for rect in row.items:
                rect.finalise(surface)

        for floating_rect in self.floating_rects:
            floating_rect.finalise(surface)

    def finalise_to_new(self):
        """
        Finalises our layout to a brand new surface that this method creates.
        """
        self.finalised_surface = pygame.Surface(self.layout_rect.size,
                                                depth=32, flags=pygame.SRCALPHA)
        self.finalised_surface.fill('#00000000')
        self.finalise_to_surf(self.finalised_surface)

        return self.finalised_surface

    def add_chunks_to_hover_group(self, link_hover_chunks):
        """
        TODO: Add me.
        :param link_hover_chunks:
        """
