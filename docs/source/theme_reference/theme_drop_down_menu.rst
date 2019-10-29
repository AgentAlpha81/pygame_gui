.. _theme-drop-down-menu:

UIDropDownMenu Theming Parameters
=================================

The :class:`UIDropDownMenu <.UIDropDownMenu>` theming block id is 'drop_down_menu'.

Misc
----

:class:`UIDropDownMenu <.UIDropDownMenu>` accepts the following miscellaneous parameters in a 'misc' block:

 - "**expand_direction**" - Can be set to **'up'** or **'down'**. Defaults to 'down'. Changing this parameter will change the direction that the menu will expand away from the initial starting point.

Sub-elements
--------------

You can reference all of the buttons that are sub elements of the drop down menu with a theming block id of
'drop_down_menu.button'. You can also reference the buttons individually by adding their object IDs:

 - 'drop_down_menu.#expand_button'
 - 'drop_down_menu.#selected_option'
 - 'drop_down_menu.#option'

There is more information on theming buttons at :ref:`theme-button`.

Example
-------

Here is an example of a drop down menu block in a JSON theme file, using the parameters described above (and a couple from UIButton).

.. code-block:: json
   :caption: drop_down_menu.json
   :linenos:

    {
        "drop_down_menu":
        {
            "misc":
            {
                "expand_direction": "down"
            },

            "colours":
            {
                "normal_bg": "#25292e",
                "hovered_bg": "#35393e"
            }
        },
        "drop_down_menu.#selected_option":
        {
            "misc":
            {
               "border_width": "1"
            }
        }
    }
