.. _theme-horizontal-slider:

UIHorizontalSlider Theming Parameters
=====================================

.. video:: _static/html/horizontal_slider.mp4
   :width: 340
   :height: 64


The :class:`UIHorizontalSlider <.UIHorizontalSlider>` theming block id is 'horizontal_slider'.

Colours
-------

:class:`UIHorizontalSlider <.UIHorizontalSlider>` makes use of these colour parameters in a 'colours' block. All of these colours can
also be a colour gradient:

 - "**dark_bg**" - The background colour/gradient of the 'back' of the slider, the colour of the track that the sliding part moves along.
 - "**normal_border**" - The border colour/gradient of the slider.

Misc
----

:class:`UIHorizontalSlider <.UIHorizontalSlider>` accepts the following miscellaneous parameters in a 'misc' block:

 - "**shape**" - Can be one of 'rectangle' or 'rounded_rectangle'. Different shapes for this UI element.
 - "**shape_corner_radius**" - Only used if our shape is 'rounded_rectangle'. It sets the radius used for the rounded corners.
 - "**border_width**" - the width in pixels of the border around the slider. Defaults to 1.
 - "**shadow_width**" - the width in pixels of the shadow behind the slider. Defaults to 1.

Sub-elements
--------------

You can reference all of the buttons that are sub elements of the slider with a theming block id of
'horizontal_slider.button'. You can also reference the buttons individually by adding their object IDs:

 - 'horizontal_slider.#left_button'
 - 'horizontal_slider.#right_button'
 - 'horizontal_slider.#sliding_button'

There is more information on theming buttons at :ref:`theme-button`.

Example
-------

Here is an example of a horizontal slider block in a JSON theme file, using the parameters described above (and some from UIButton).

.. code-block:: json
   :caption: horizontal_slider.json
   :linenos:

    {
        "horizontal_slider":
        {
            "colours":
            {
                "normal_bg": "#25292e",
                "hovered_bg": "#35393e",
                "disabled_bg": "#25292e",
                "selected_bg": "#25292e",
                "active_bg": "#193784",
                "dark_bg": "#15191e,#202020,0",
                "normal_text": "#c5cbd8",
                "hovered_text": "#FFFFFF",
                "selected_text": "#FFFFFF",
                "disabled_text": "#6d736f"
            }
        },
        "horizontal_slider.button":
        {
            "misc":
            {
               "border_width": "1"
            }
        },
        "horizontal_slider.#sliding_button":
        {
            "colours":
            {
               "normal_bg": "#FF0000"
            }
        }
    }