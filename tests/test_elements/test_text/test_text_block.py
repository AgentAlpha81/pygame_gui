import os
import pytest
import pygame
import pygame_gui

from tests.shared_fixtures import _init_pygame, default_ui_manager, default_display_surface, _display_surface_return_none

from pygame_gui.elements.text.html_parser import CharStyle
from pygame_gui.elements.text.styled_chunk import StyledChunk
from pygame_gui.elements.text.text_block import TextBlock
from pygame_gui.core.ui_font_dictionary import UIFontDictionary


class TestTextBlock:
    def test_creation(self, _init_pygame):
        dictionary = UIFontDictionary()
        style = CharStyle()
        styled_chunk = StyledChunk(font_size=14, font_name='fira_code',
                                   chunk='text', style=style, color=pygame.Color('#FFFF00'),
                                   bg_color=pygame.Color('#000000'),
                                   is_link=False, link_href='test', link_style=CharStyle(),
                                   position=(0, 0), font_dictionary=dictionary)

        TextBlock(text='test', rect=pygame.Rect(0, 0, 100, 100),
                  indexed_styles={0: styled_chunk}, font_dict=dictionary, link_style=style,
                  bg_colour=pygame.Color('#FF0000'), wrap_to_height=True)

    def test_creation_scale_to_text(self, _init_pygame):
        dictionary = UIFontDictionary()
        style = CharStyle()
        styled_chunk = StyledChunk(font_size=14, font_name='fira_code',
                                   chunk='text', style=style, color=pygame.Color('#FFFF00'),
                                   bg_color=pygame.Color('#000000'),
                                   is_link=False, link_href='test', link_style=CharStyle(),
                                   position=(0, 0), font_dictionary=dictionary)

        TextBlock(text='test', rect=pygame.Rect(0, 0, -1, -1),
                  indexed_styles={0: styled_chunk}, font_dict=dictionary, link_style=style,
                  bg_colour=pygame.Color('#FF0000'), wrap_to_height=True)

    def test_creation_scale_vert_to_text(self, _init_pygame):
        dictionary = UIFontDictionary()
        style = CharStyle()
        styled_chunk = StyledChunk(font_size=14, font_name='fira_code',
                                   chunk='text', style=style, color=pygame.Color('#FFFF00'),
                                   bg_color=pygame.Color('#000000'),
                                   is_link=False, link_href='test', link_style=CharStyle(),
                                   position=(0, 0), font_dictionary=dictionary)

        TextBlock(text='test', rect=pygame.Rect(0, 0, -1, 100),
                  indexed_styles={0: styled_chunk}, font_dict=dictionary, link_style=style,
                  bg_colour=pygame.Color('#FF0000'), wrap_to_height=True)
