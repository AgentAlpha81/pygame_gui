from typing import Optional

import pygame

from pygame_gui.core.text.text_layout_rect import TextLayoutRect
from pygame_gui.core.text.text_line_chunk import TextLineChunkFTFont


class TextBoxLayoutRow(pygame.Rect):
    """
    A single line of text-like stuff to be used in a text box type layout.
    """

    def __init__(self, row_start_x, row_start_y, row_index, line_spacing, layout):
        super().__init__(row_start_x, row_start_y, 0, 0)
        self.line_spacing = line_spacing
        self.row_index = row_index
        self.layout = layout
        self.items = []

        self.letter_count = 0

        self.y_origin = 0
        self.text_chunk_height = 0

        self.target_surface = None
        self.cursor_rect = pygame.Rect(self.x, row_start_y, 2, self.height - 2)
        self.edit_cursor_active = False
        self.cursor_position = 0
        self.cursor_draw_width = 0

    def __hash__(self):
        return self.row_index

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
        item.left = self.right
        self.items.append(item)
        self.width += item.width  # noqa pylint: disable=attribute-defined-outside-init; pylint getting confused

        if item.height > self.text_chunk_height:
            self.text_chunk_height = item.height
            if self.layout.layout_rect.height != -1:
                self.height = min(self.layout.layout_rect.height, # noqa pylint: disable=attribute-defined-outside-init; pylint getting confused
                                  item.height * self.line_spacing)
            else:
                self.height = item.height * self.line_spacing

            self.cursor_rect = pygame.Rect(self.x, self.y, 2, self.height - 2)

        if isinstance(item, TextLineChunkFTFont):
            if item.y_origin > self.y_origin:
                self.y_origin = item.y_origin

        self.letter_count += item.letter_count

    def rewind_row(self, layout_rect_queue):
        """
        Use this to add items from the row back onto a layout queue, useful if we've added
        something to the layout that means that this row needs to be re-run through the
        layout code.

        :param layout_rect_queue: A layout queue that contains items to be laid out in order.
        """
        for rect in reversed(self.items):
            layout_rect_queue.appendleft(rect)
        self.clear()
        self.items.clear()
        self.width = 0  # pylint: disable=attribute-defined-outside-init; pylint getting confused
        self.height = 0  # pylint: disable=attribute-defined-outside-init; pylint getting confused
        self.text_chunk_height = 0
        self.letter_count = 0
        self.y_origin = 0

    def horiz_center_row(self):
        self.centerx = self.layout.layout_rect.centerx
        current_start_x = self.x
        for item in self.items:
            item.x = current_start_x
            current_start_x += item.width

    def align_left_row(self, start_x: int):
        self.x = start_x
        current_start_x = self.x
        for item in self.items:
            item.x = current_start_x
            current_start_x += item.width

    def align_right_row(self, start_x: int):
        self.right = start_x
        current_start_x = start_x
        for item in self.items:
            item.right = current_start_x
            current_start_x += item.width

    def vert_align_items_to_row(self):
        for item in self.items:
            item.y = self.y

    def merge_adjacent_compatible_chunks(self):
        index = 0
        while index < len(self.items)-1:
            current_item = self.items[index]
            next_item = self.items[index+1]
            if (isinstance(current_item, TextLineChunkFTFont) and
                    isinstance(next_item, TextLineChunkFTFont) and
                    current_item.style_match(next_item)):
                current_item.add_text(next_item.text)
                self.items.pop(index+1)
            else:
                index += 1

    def finalise(self, surface, current_end_pos: Optional[int] = None, cumulative_letter_count: Optional[int] = None):
        self.merge_adjacent_compatible_chunks()

        for text_chunk in self.items:
            if isinstance(text_chunk, TextLineChunkFTFont):
                if current_end_pos is not None and cumulative_letter_count is not None:
                    if cumulative_letter_count < current_end_pos:
                        text_chunk.finalise(surface, self.layout.view_rect, self.y_origin,
                                            self.text_chunk_height, self.height,
                                            current_end_pos - cumulative_letter_count)
                        cumulative_letter_count += text_chunk.letter_count
                else:
                    text_chunk.finalise(surface, self.layout.view_rect, self.y_origin,
                                        self.text_chunk_height, self.height)

        if self.edit_cursor_active:
            cursor_surface = pygame.surface.Surface(self.cursor_rect.size,
                                                    flags=pygame.SRCALPHA, depth=32)

            cursor_surface.fill(pygame.Color('#FFFFFFFF'))
            self.cursor_rect = pygame.Rect(self.x + self.cursor_draw_width, self.y, 2, max(0, self.height - 2))
            surface.blit(cursor_surface, self.cursor_rect, special_flags=pygame.BLEND_PREMULTIPLIED)

        self.target_surface = surface

        # pygame.draw.rect(self.target_surface, pygame.Color('#FF0000'), self, 1)

        return cumulative_letter_count

    def set_default_text_colour(self, colour):
        for chunk in self.items:
            if isinstance(chunk, TextLineChunkFTFont):
                if chunk.using_default_text_colour:
                    chunk.colour = colour

    def toggle_cursor(self):
        if self.edit_cursor_active:
            self.edit_cursor_active = False
        else:
            self.edit_cursor_active = True

        if self.target_surface is not None:
            self.clear()
            self.finalise(self.target_surface)

    def clear(self):
        if self.target_surface is not None:
            slightly_wider_rect = pygame.Rect(self.x, self.y, self.width + self.layout.edit_buffer, self.height)
            self.target_surface.fill(pygame.Color('#00000000'), slightly_wider_rect)

    def set_cursor_from_click_pos(self, click_pos):
        letter_acc = 0
        cursor_draw_width = 0
        for chunk in self.items:
            if isinstance(chunk, TextLineChunkFTFont):
                if chunk.collidepoint(click_pos):
                    letter_index = chunk.x_pos_to_letter_index(click_pos.x)
                    cursor_draw_width += sum([char_metric[4]
                                              for char_metric
                                              in chunk.font.get_metrics(chunk.text[:letter_index])])
                    letter_acc += letter_index
                else:
                    cursor_draw_width += sum([char_metric[4] for char_metric in chunk.font.get_metrics(chunk.text)])
                    letter_acc += chunk.letter_count

        self.cursor_draw_width = cursor_draw_width
        self.cursor_position = min(self.letter_count, max(0, letter_acc))

    def set_cursor_position(self, cursor_pos):
        self.cursor_position = min(self.letter_count, max(0, cursor_pos))
        letter_acc = 0
        cursor_draw_width = 0
        for chunk in self.items:
            if cursor_pos <= letter_acc + chunk.letter_count:
                chunk_letter_pos = cursor_pos - letter_acc
                cursor_draw_width += sum([char_metric[4]
                                          for char_metric
                                          in chunk.font.get_metrics(chunk.text[:chunk_letter_pos])])

                break
            else:
                letter_acc += chunk.letter_count
                cursor_draw_width += sum([char_metric[4] for char_metric in chunk.font.get_metrics(chunk.text)])

        self.cursor_draw_width = cursor_draw_width

    def insert_text(self, text: str, letter_row_index: int):
        letter_acc = 0
        for chunk in self.items:
            if letter_row_index <= letter_acc + chunk.letter_count:
                chunk_index = letter_row_index - letter_acc
                chunk.insert_text(text, chunk_index)
                break
            else:
                letter_acc += chunk.letter_count

