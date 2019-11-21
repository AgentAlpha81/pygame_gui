.. _theme-text-entry-line:

UITextEntryLine Theming Parameters
===================================

The :class:`UITextEntryLine <.UITextEntryLine>` theming block id is 'text_entry_line'.

Colours
-------

:class:`UITextEntryLine <.UITextEntryLine>` makes use of these colour parameters in a 'colours' block. All of these colours can
also be a colour gradient:

 - "**normal_bg**" -  The default colour/gradient of the background to the entry line element.
 - "**selected_bg**" - The colour/gradient the background changes to when the text above it is selected.
 - "**normal_text**" - The default colour/gradient of text entered into the element.
 - "**selected_text**" - The colour/gradient of text when it has been selected.
 - "**normal_border**" - The colour/gradient of the border around the text entry element.

Font
-----

:class:`UITextEntryLine <.UITextEntryLine>` accepts a font specified in the theme via a 'font' block. A 'font' block has these parameters:

 - "**name**" - Necessary to make a valid block. This is the name that this font goes by in the UI, if this is a new font then subsequent font instances with different styles or sizes should use the same name.
 - "**size**" - Necessary to make a valid block. This is the point size of the font to use on the text entry line.
 - "**bold**" - Optional parameter. Set it to "1" to make this font bold.
 - "**italic**" - Optional parameter. Set it to "1" to make this font italic.

Only specify paths if this is the first use of this font name in the GUI:

 - "**regular_path**" - The path to this font's file with no particular style applied.
 - "**bold_path**" - The path to this font's file with bold style applied.
 - "**italic_path**" - The path to this font's file with italic style applied.
 - "**bold_italic_path**" - The path to this font's file with bold and italic style applied.

Misc
----

:class:`UITextEntryLine <.UITextEntryLine>` accepts the following miscellaneous parameters in a 'misc' block:

 - "**shape**" - Can be one of 'rectangle' or 'rounded_rectangle'. Different shapes for this UI element.
 - "**shape_corner_radius**" - Only used if our shape is 'rounded_rectangle'. It sets the radius used for the rounded corners.
 - "**border_width**" - the width of the border around the element in pixels. Defaults to "1".
 - "**shadow_width**" - the width of the shadow around the element in pixels. Defaults to "1".
 - "**padding**" - the horizontal and vertical 'padding' between the border and where we render the text. Defaults to "4,2".

Example
-------

Here is an example of a text entry line block in a JSON theme file using all the parameters described above.

.. code-block:: json
   :caption: text_entry_line.json
   :linenos:

    {
        "button":
        {
            "colours":
            {
                "normal_bg": "#25292e",
                "selected_bg": "#55595e",
                "normal_text": "#AAAAAA",
                "selected_text": "#FFFFFF",
                "border": "#FFFFFF"
            },
            "font":
            {
                "name": "montserrat",
                "size": "12",
                "bold": "0",
                "italic": "1",
                "regular_path": "data/fonts/Montserrat-Regular.ttf",
                "bold_path": "data/fonts/Montserrat-Bold.ttf",
                "italic_path": "data/fonts/Montserrat-Italic.ttf",
                "bold_italic_path": "data/fonts/Montserrat-BoldItalic.ttf"
            },
            "misc":
            {
                "border_width": "2",
                "shadow_width": "2",
                "padding": "6,4"
            }
        }
    }
