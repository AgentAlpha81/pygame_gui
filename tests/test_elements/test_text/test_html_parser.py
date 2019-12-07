import os
import pytest
import pygame
import pygame_gui

from tests.shared_fixtures import _init_pygame, default_ui_manager, default_display_surface, _display_surface_return_none

from pygame_gui.elements.text.html_parser import CharStyle, TextHTMLParser, TextLineContext, TextStyleData
from pygame_gui.core.ui_appearance_theme import UIAppearanceTheme


class TestCharStyle:
    def test_creation(self, _init_pygame):
        CharStyle()

    def test_comparison(self, _init_pygame):
        assert CharStyle() == CharStyle()


class TestTextLineContext:
    def test_creation(self, _init_pygame):
        TextLineContext(font_size=14, font_name='fira_code', style=CharStyle(),
                        color=pygame.Color('#FFFFFF'), bg_color=pygame.Color('#000000'),
                        is_link=True, link_href='None')

    def test_comparison(self, _init_pygame):
        text_line_1 = TextLineContext(font_size=14, font_name='fira_code', style=CharStyle(),
                                      color=pygame.Color('#FFFFFF'), bg_color=pygame.Color('#000000'),
                                      is_link=True, link_href='None')

        text_line_2 = TextLineContext(font_size=14, font_name='fira_code', style=CharStyle(),
                                      color=pygame.Color('#FFFFFF'), bg_color=pygame.Color('#000000'),
                                      is_link=True, link_href='None')

        assert text_line_1 == text_line_2


class TestHtmlParser:
    def test_creation(self, _init_pygame):
        theme = UIAppearanceTheme()
        parser = TextHTMLParser(theme, [], [])
        parser.feed('<b>text</b>')

    def test_invalid_tag(self, _init_pygame):
        theme = UIAppearanceTheme()
        parser = TextHTMLParser(theme, [], [])
        with pytest.warns(UserWarning, match='Unsupported HTML Tag'):
            parser.feed('<video>text</video>')

    def test_body_gradient(self, _init_pygame):
        theme = UIAppearanceTheme()
        parser = TextHTMLParser(theme, [], [])
        parser.feed('<body bg_color=#FF0000,#FFFF00,0>text</body>')
