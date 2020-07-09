import warnings
import html.parser
from collections import deque
from typing import Union, List, Dict, Any

import pygame

from pygame_gui.core.colour_gradient import ColourGradient
from pygame_gui.core.ui_appearance_theme import UIAppearanceTheme


from pygame_gui.core.text.line_break_layout_rect import LineBreakLayoutRect
from pygame_gui.core.text.horiz_rule_layout_rect import HorizRuleLayoutRect
from pygame_gui.core.text.text_line_chunk import TextLineChunk_Font


class HTMLParser(html.parser.HTMLParser):

    default_style = {
        'font_name': 'fira_code',
        'font_size': 14,
        'font_colour': pygame.Color(255, 255, 255, 255),
        'bg_colour': pygame.Color(0, 0, 0, 0)
    }

    font_sizes = {
        1: 8,
        1.5: 9,
        2: 10,
        2.5: 11,
        3: 12,
        3.5: 13,
        4: 14,
        4.5: 16,
        5: 18,
        5.5: 20,
        6: 24,
        6.5: 32,
        7: 48
    }

    def __init__(self, ui_theme: UIAppearanceTheme, combined_ids: List[str]):

        super().__init__()
        self.ui_theme = ui_theme
        self.combined_ids = combined_ids

        self.element_stack = []

        self.style_stack = []
        self.current_style = {}

        font_info = self.ui_theme.get_font_info(combined_ids)

        self.default_style['font_name'] = font_info['name']
        self.default_style['font_size'] = int(font_info['size'])
        self.default_style['font_colour'] = self.ui_theme.get_colour_or_gradient('normal_text',
                                                                                 combined_ids)
        self.default_style['bg_colour'] = self.ui_theme.get_colour_or_gradient('dark_bg',
                                                                               combined_ids)
        self.default_style['bold'] = False
        self.default_style['italic'] = False
        self.default_style['underline'] = False
        self.default_style['link'] = False
        self.default_style['link_href'] = ''

        # this is the style used before any html is loaded
        self.push_style('default_style', self.default_style)

        self.layout_rect_queue = deque([])

    def handle_starttag(self, tag: str, attrs: Dict[str, str]):
        """
        Process an HTML 'start tag' (e.g. <b>) where we have a start and an end tag enclosing a
        range of text this is the first one of those and controls where we add the 'styling' thing
        to our styling stack.

        Eventually we will want to expand this to handle tags like <img>.

        :param tag: The tag itself
        :param attrs: Attributes of the tag.
        """
        element = tag.lower()

        self.element_stack.append(element)

        attributes = {key.lower(): value for key, value in attrs}
        style = {}
        if element in ('b', 'strong'):
            style['bold'] = True
        elif element == 'a':
            style['link'] = True
            if 'href' in attributes:
                style["link_href"] = attributes['href']
        elif element in ('i', 'em', 'var'):
            style['italic'] = True
        elif element == 'u':
            style['underline'] = True
        elif element == 'font':
            if 'face' in attributes:
                font_name = attributes['face'] if len(attributes['face']) > 0 else None
                style["font_name"] = font_name
            if 'size' in attributes:
                if len(attributes['size']) > 0:
                    font_size = self.font_sizes[float(attributes['size'])]
                else:
                    font_size = None
                style["font_size"] = font_size
            if 'color' in attributes:
                if attributes['color'][0] == '#':
                    style["font_colour"] = pygame.color.Color(attributes['color'])
                else:
                    style["font_colour"] = self.ui_theme.get_colour_or_gradient(attributes['color'],
                                                                                self.combined_ids)
        elif element == 'body':
            if 'bgcolor' in attributes:
                if len(attributes['bgcolor']) > 0:
                    if ',' in attributes['bgcolor']:
                        col_id = attributes['bgcolor']
                        style["bg_colour"] = self.ui_theme.get_colour_or_gradient(col_id,
                                                                                  self.combined_ids)
                    else:
                        style["bg_colour"] = pygame.color.Color(attributes['bgcolor'])
                else:
                    style["bg_colour"] = None

        elif element == 'br':

            current_font = self.ui_theme.get_font_dictionary().find_font(
                                                font_name=self.current_style['font_name'],
                                                font_size=self.current_style['font_size'],
                                                bold=self.current_style['bold'],
                                                italic=self.current_style['italic'])

            dimensions = current_font.size(' ')

            self.layout_rect_queue.append(LineBreakLayoutRect(dimensions=dimensions))
        else:
            warning_text = 'Unsupported HTML Tag <' + element + '>. Check documentation' \
                                                                ' for full range of supported tags.'
            warnings.warn(warning_text, UserWarning)

        self.push_style(element, style)

    def handle_endtag(self, tag: str):
        """
        Handles encountering an HTML end tag. Usually this will involve us popping a style off our
        stack of styles.

        :param tag: The end tag to handle.
        """
        element = tag.lower()

        if element not in self.element_stack:
            return

        self.pop_style(element)

        result = None
        while result != element:
            result = self.element_stack.pop()

    def handle_data(self, data: str):
        """
        Handles parsed HTML that is not a tag of any kind, ordinary text basically.

        :param data: Some string data.
        """
        self.add_text(data)

    def error(self, message):
        """
        Feeds any parsing errors up the chain to the warning system.

        :param message: The message to warn about.
        """
        warnings.warn(message, UserWarning)

    def push_style(self, key: str, styles: Dict[str, Any]):
        """
        Add a new styling element onto the style stack. These are single styles generally (i.e. a
        font size change, or a bolding of text) rather than a load of different styles all at once.
        The eventual style of a character/bit of text is built up by evaluating all styling
        elements currently on the stack when we parse that bit of text.

        Styles on top of the stack will be evaluated last so they can overwrite elements earlier
        in the stack (i.e. a later 'font_size' of 5 wil overwrite an earlier 'font_size' of 3).

        :param key: Name for this styling element so we can identify when to remove it when the
        styling block is closed
        :param styles: The styling dictionary that contains the actual styling.
        """
        old_styles = {name: self.current_style.get(name) for name in styles}
        self.style_stack.append((key, old_styles))
        self.current_style.update(styles)

    def pop_style(self, key: str):
        """
        Remove a styling element/dictionary from the stack by it's identifying key name.

        :param key: The identifier.
        """
        # Don't do anything if key is not in stack
        for match, _ in self.style_stack:
            if key == match:
                break
        else:
            return

        # Remove all innermost elements until key is closed.
        while True:
            match, old_styles = self.style_stack.pop()
            self.current_style.update(old_styles)
            if match == key:
                break

    def add_text(self, text: str):
        """
        Add another bit of text using the current style, and index the text's style appropriately.

        :param text:
        """

        self.layout_rect_queue.append(
            TextLineChunk_Font(text,
                               self.ui_theme.get_font_dictionary().find_font(
                                   font_name=self.current_style['font_name'],
                                   font_size=self.current_style['font_size'],
                                   bold=self.current_style['bold'],
                                   italic=self.current_style['italic']),
                               colour=self.current_style['font_colour']))
