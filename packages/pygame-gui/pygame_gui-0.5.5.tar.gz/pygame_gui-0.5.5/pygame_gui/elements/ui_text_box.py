import warnings
import math

from typing import Union, Tuple, Dict

import pygame

from pygame_gui._constants import UI_TEXT_BOX_LINK_CLICKED
from pygame_gui._constants import TEXT_EFFECT_TYPING_APPEAR
from pygame_gui._constants import TEXT_EFFECT_FADE_IN, TEXT_EFFECT_FADE_OUT

from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core.ui_element import UIElement
from pygame_gui.core.drawable_shapes import RectDrawableShape, RoundedRectangleShape

from pygame_gui.elements.ui_vertical_scroll_bar import UIVerticalScrollBar
from pygame_gui.elements.text import TextBlock, TextHTMLParser
from pygame_gui.elements.text import TypingAppearEffect, FadeInEffect, FadeOutEffect


class UITextBox(UIElement):
    """
    A Text Box element lets us display word-wrapped, formatted text. If the text to display is
    longer than the height of the box given then the element will automatically create a vertical
    scroll bar so that all the text can be seen.

    Formatting the text is done via a subset of HTML tags. Currently supported tags are:

    - <b></b> or <strong></strong> - to encase bold styled text.
    - <i></i>, <em></em> or <var></var> - to encase italic styled text.
    - <u></u> - to encase underlined text.
    - <a href='id'></a> - to encase 'link' text that can be clicked on to generate events with the
                          id given in href.
    - <body bgcolor='#FFFFFF'></body> - to change the background colour of encased text.
    - <br> - to start a new line.
    - <font face='verdana' color='#000000' size=3.5></font> - To set the font, colour and size of
                                                              encased text.

    More may be added in the future if needed or frequently requested.

    NOTE: if dimensions of the initial containing rect are set to -1 the text box will match the
    final dimension to whatever the text rendering produces. This lets us make dynamically sized
    text boxes depending on their contents.


    :param html_text: The HTML formatted text to display in this text box.
    :param relative_rect: The 'visible area' rectangle, positioned relative to it's container.
    :param manager: The UIManager that manages this element.
    :param wrap_to_height: False by default, if set to True the box will increase in height to
                           match the text within.
    :param layer_starting_height: Sets the height, above it's container, to start placing the text
                                  box at.
    :param container: The container that this element is within. If set to None will be the root
                      window's container.
    :param parent_element: The element this element 'belongs to' in the theming hierarchy.
    :param object_id: A custom defined ID for fine tuning of theming.
    :param anchors: A dictionary describing what this element's relative_rect is relative to.

    """

    def __init__(self,
                 html_text: str,
                 relative_rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 wrap_to_height: bool = False,
                 layer_starting_height: int = 1,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[str, None] = None,
                 anchors: Dict[str, str] = None):

        new_element_ids, new_object_ids = self._create_valid_ids(container=container,
                                                                 parent_element=parent_element,
                                                                 object_id=object_id,
                                                                 element_id='text_box')
        super().__init__(relative_rect, manager, container,
                         starting_height=layer_starting_height,
                         layer_thickness=2,
                         element_ids=new_element_ids,
                         object_ids=new_object_ids,
                         anchors=anchors
                         )
        self.html_text = html_text
        self.font_dict = self.ui_theme.get_font_dictionary()

        self.wrap_to_height = wrap_to_height
        self.link_hover_chunks = []  # container for any link chunks we have

        self.active_text_effect = None
        self.scroll_bar = None
        self.scroll_bar_width = 20

        self.border_width = None
        self.shadow_width = None
        self.padding = None
        self.background_colour = None
        self.border_colour = None

        self.link_normal_colour = None
        self.link_hover_colour = None
        self.link_selected_colour = None
        self.link_normal_underline = False
        self.link_hover_underline = True
        self.link_style = None

        self.rounded_corner_offset = None
        self.formatted_text_block = None  # TextLine()
        self.text_wrap_rect = None
        self.background_surf = None

        self.drawable_shape = None
        self.shape_type = 'rectangle'
        self.shape_corner_radius = None

        self.should_trigger_full_rebuild = True
        self.time_until_full_rebuild_after_changing_size = 0.2
        self.full_rebuild_countdown = self.time_until_full_rebuild_after_changing_size

        self.rebuild_from_changed_theme_data()

    def kill(self):
        """
        Overrides the standard sprite kill method to also kill any scroll bars belonging to this
        text box.
        """
        if self.scroll_bar is not None:
            self.scroll_bar.kill()
        super().kill()

    def rebuild(self):
        """
        Rebuild whatever needs building.

        """
        if self.scroll_bar is not None:
            self.scroll_bar.kill()

        # The text_wrap_area is the part of the text box that we try to keep the text inside
        # of so that none  of it overlaps. Essentially we start with the containing box,
        # subtract the border, then subtract the padding, then if necessary subtract the width
        # of the scroll bar
        self.rounded_corner_offset = int(self.shape_corner_radius -
                                         (math.sin(math.pi / 4) *
                                          self.shape_corner_radius))
        self.text_wrap_rect = [(self.rect[0] +
                                self.padding[0] +
                                self.border_width +
                                self.shadow_width +
                                self.rounded_corner_offset),
                               (self.rect[1] +
                                self.padding[1] +
                                self.border_width +
                                self.shadow_width +
                                self.rounded_corner_offset),
                               max(1, (self.rect[2] -
                                       (self.padding[0] * 2) -
                                       (self.border_width * 2) -
                                       (self.shadow_width * 2) -
                                       (2 * self.rounded_corner_offset))),
                               max(1, (self.rect[3] -
                                       (self.padding[1] * 2) -
                                       (self.border_width * 2) -
                                       (self.shadow_width * 2) -
                                       (2 * self.rounded_corner_offset)))]
        if self.wrap_to_height or self.rect[3] == -1:
            self.text_wrap_rect[3] = -1
        if self.rect[2] == -1:
            self.text_wrap_rect[2] = -1

        # This gives us the height of the text at the 'width' of the text_wrap_area
        self.parse_html_into_style_data()
        if self.formatted_text_block is not None:
            if self.wrap_to_height or self.rect[3] == -1 or self.rect[2] == -1:
                final_text_area_size = self.formatted_text_block.final_dimensions
                new_dimensions = ((final_text_area_size[0] + (self.padding[0] * 2) +
                                   (self.border_width * 2) + (self.shadow_width * 2) +
                                   (2 * self.rounded_corner_offset)),
                                  (final_text_area_size[1] + (self.padding[1] * 2) +
                                   (self.border_width * 2) + (self.shadow_width * 2) +
                                   (2 * self.rounded_corner_offset)))
                self.set_dimensions(new_dimensions)

            elif self.formatted_text_block.final_dimensions[1] > self.text_wrap_rect[3]:
                # We need a scrollbar because our text is longer than the space we
                # have to display it. This also means we need to parse the text again.
                text_rect_width = (self.rect[2] -
                                   (self.padding[0] * 2) -
                                   (self.border_width * 2) -
                                   (self.shadow_width * 2) -
                                   self.rounded_corner_offset - self.scroll_bar_width)
                self.text_wrap_rect = [(self.rect[0] + self.padding[0] + self.border_width +
                                        self.shadow_width + self.rounded_corner_offset),
                                       (self.rect[1] + self.padding[1] + self.border_width +
                                        self.shadow_width + self.rounded_corner_offset),
                                       max(1, text_rect_width),
                                       max(1, (self.rect[3] -
                                               (self.padding[1] * 2) -
                                               (self.border_width * 2) -
                                               (self.shadow_width * 2) -
                                               (2 * self.rounded_corner_offset)))]
                self.parse_html_into_style_data()
                percentage_visible = (self.text_wrap_rect[3] /
                                      self.formatted_text_block.final_dimensions[1])
                scroll_bar_position = (self.relative_rect.right - self.border_width -
                                       self.shadow_width - self.scroll_bar_width,
                                       self.relative_rect.top + self.border_width +
                                       self.shadow_width)

                scroll_bar_rect = pygame.Rect(scroll_bar_position,
                                              (self.scroll_bar_width,
                                               self.rect.height -
                                               (2 * self.border_width) -
                                               (2 * self.shadow_width)))
                self.scroll_bar = UIVerticalScrollBar(scroll_bar_rect,
                                                      percentage_visible,
                                                      self.ui_manager,
                                                      self.ui_container,
                                                      parent_element=self)
            else:
                new_dimensions = (self.rect[2], self.rect[3])
                self.set_dimensions(new_dimensions)

        theming_parameters = {'normal_bg': self.background_colour,
                              'normal_border': self.border_colour,
                              'border_width': self.border_width,
                              'shadow_width': self.shadow_width,
                              'shape_corner_radius': self.shape_corner_radius}

        if self.shape_type == 'rectangle':
            self.drawable_shape = RectDrawableShape(self.rect, theming_parameters,
                                                    ['normal'], self.ui_manager)
        elif self.shape_type == 'rounded_rectangle':
            self.drawable_shape = RoundedRectangleShape(self.rect, theming_parameters,
                                                        ['normal'], self.ui_manager)

        self.background_surf = self.drawable_shape.get_surface('normal')

        if self.scroll_bar is not None:
            height_adjustment = int(self.scroll_bar.start_percentage *
                                    self.formatted_text_block.final_dimensions[1])
        else:
            height_adjustment = 0

        if self.rect.width <= 0 or self.rect.height <= 0:
            return

        drawable_area = pygame.Rect((0, height_adjustment),
                                    (self.text_wrap_rect[2],
                                     self.text_wrap_rect[3]))
        new_image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA, depth=32)
        new_image.fill(pygame.Color(0, 0, 0, 0))
        new_image.blit(self.background_surf, (0, 0))
        new_image.blit(self.formatted_text_block.block_sprite,
                       (self.padding[0] + self.border_width +
                        self.shadow_width + self.rounded_corner_offset,
                        self.padding[1] + self.border_width +
                        self.shadow_width + self.rounded_corner_offset),
                       drawable_area)

        self.set_image(new_image)

        self.formatted_text_block.add_chunks_to_hover_group(self.link_hover_chunks)

        self.should_trigger_full_rebuild = False
        self.full_rebuild_countdown = self.time_until_full_rebuild_after_changing_size

    def update(self, time_delta: float):
        """
        Called once every update loop of the UI Manager. Used to react to scroll bar movement
        (if there is one), update the text effect (if there is one) and check if we are hovering
        over any text links (if there are any).

        :param time_delta: The time in seconds between calls to update. Useful for timing things.

        """
        super().update(time_delta)
        if not self.alive():
            return
        if self.scroll_bar is not None and self.scroll_bar.check_has_moved_recently():
            height_adjustment = int(self.scroll_bar.start_percentage *
                                    self.formatted_text_block.final_dimensions[1])
            drawable_area = pygame.Rect((0, height_adjustment),
                                        (self.text_wrap_rect[2], self.text_wrap_rect[3]))

            if self.rect.width <= 0 or self.rect.height <= 0:
                return

            new_image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA, depth=32)
            new_image.fill(pygame.Color(0, 0, 0, 0))
            new_image.blit(self.background_surf, (0, 0))
            new_image.blit(self.formatted_text_block.block_sprite,
                           (self.padding[0] + self.border_width +
                            self.shadow_width +
                            self.rounded_corner_offset,
                            self.padding[1] + self.border_width +
                            self.shadow_width +
                            self.rounded_corner_offset),
                           drawable_area)
            self.set_image(new_image)

        mouse_x, mouse_y = self.ui_manager.get_mouse_position()
        should_redraw_from_chunks = False

        if self.scroll_bar is not None:
            height_adjustment = (self.scroll_bar.start_percentage *
                                 self.formatted_text_block.final_dimensions[1])
        else:
            height_adjustment = 0
        base_x = int(self.rect[0] + self.padding[0] + self.border_width +
                     self.shadow_width + self.rounded_corner_offset)
        base_y = int(self.rect[1] + self.padding[1] + self.border_width +
                     self.shadow_width + self.rounded_corner_offset - height_adjustment)

        for chunk in self.link_hover_chunks:
            hovered_currently = False

            hover_rect = pygame.Rect((base_x + chunk.rect.x,
                                      base_y + chunk.rect.y),
                                     chunk.rect.size)
            if hover_rect.collidepoint(mouse_x, mouse_y) and self.rect.collidepoint(mouse_x,
                                                                                    mouse_y):
                hovered_currently = True
            if chunk.is_hovered and not hovered_currently:
                chunk.on_unhovered()
                should_redraw_from_chunks = True
            elif hovered_currently and not chunk.is_hovered:
                chunk.on_hovered()
                should_redraw_from_chunks = True

        if should_redraw_from_chunks:
            self.redraw_from_chunks()

        if self.active_text_effect is not None:
            self.active_text_effect.update(time_delta)
            if self.active_text_effect.should_full_redraw():
                self.full_redraw()
            if self.active_text_effect.should_redraw_from_chunks():
                self.redraw_from_chunks()

        if self.should_trigger_full_rebuild and self.full_rebuild_countdown <= 0.0:
            self.rebuild()

        if self.full_rebuild_countdown > 0.0:
            self.full_rebuild_countdown -= time_delta

    def on_fresh_drawable_shape_ready(self):
        """
        Called by an element's drawable shape when it has a new image surface ready for use,
        normally after a rebuilding/redrawing of some kind.
        """
        self.background_surf = self.drawable_shape.get_surface('normal')
        self.redraw_from_text_block()

    def set_relative_position(self, position: Union[pygame.math.Vector2,
                                                    Tuple[int, int],
                                                    Tuple[float, float]]):
        """
        Sets the relative screen position of this text box, updating it's subordinate scroll bar at
        the same time.

        :param position: The relative screen position to set.

        """
        super().set_relative_position(position)

        if self.scroll_bar is not None:
            scroll_bar_position = (self.relative_rect.right - self.border_width -
                                   self.shadow_width - self.scroll_bar_width,
                                   self.relative_rect.top + self.border_width +
                                   self.shadow_width)
            self.scroll_bar.set_relative_position(scroll_bar_position)

    def set_position(self, position: Union[pygame.math.Vector2,
                                           Tuple[int, int],
                                           Tuple[float, float]]):
        """
        Sets the absolute screen position of this text box, updating it's subordinate scroll bar
        at the same time.

        :param position: The absolute screen position to set.

        """
        super().set_position(position)

        if self.scroll_bar is not None:
            scroll_bar_position = (self.relative_rect.right - self.border_width -
                                   self.shadow_width - self.scroll_bar_width,
                                   self.relative_rect.top + self.border_width +
                                   self.shadow_width)
            self.scroll_bar.set_relative_position(scroll_bar_position)

    def set_dimensions(self, dimensions: Union[pygame.math.Vector2,
                                               Tuple[int, int],
                                               Tuple[float, float]]):
        """
        Method to directly set the dimensions of a text box.

        :param dimensions: The new dimensions to set.

        """
        self.relative_rect.width = int(dimensions[0])
        self.relative_rect.height = int(dimensions[1])
        self.rect.size = self.relative_rect.size

        if dimensions[0] >= 0 and dimensions[1] >= 0:
            if self.relative_right_margin is not None:
                self.relative_right_margin = self.ui_container.rect.right - self.rect.right

            if self.relative_bottom_margin is not None:
                self.relative_bottom_margin = self.ui_container.rect.bottom - self.rect.bottom

            self._update_container_clip()

            # Quick and dirty temporary scaling to cut down on number of
            # full rebuilds triggered when rapid scaling
            if self.image is not None:
                if (self.full_rebuild_countdown > 0.0 and
                        (self.relative_rect.width > 0 and
                         self.relative_rect.height > 0)):
                    new_image = pygame.Surface(self.relative_rect.size,
                                               flags=pygame.SRCALPHA,
                                               depth=32)
                    new_image.blit(self.image, (0, 0))
                    self.set_image(new_image)

                    if self.scroll_bar is not None:
                        self.scroll_bar.set_dimensions((self.scroll_bar.relative_rect.width,
                                                        self.relative_rect.height -
                                                        (2 * self.border_width) -
                                                        (2 * self.shadow_width)))
                        scroll_bar_position = (self.relative_rect.right - self.border_width -
                                               self.shadow_width - self.scroll_bar_width,
                                               self.relative_rect.top + self.border_width +
                                               self.shadow_width)
                        self.scroll_bar.set_relative_position(scroll_bar_position)

                self.should_trigger_full_rebuild = True
                self.full_rebuild_countdown = self.time_until_full_rebuild_after_changing_size

    def parse_html_into_style_data(self):
        """
        Parses HTML styled string text into a format more useful for styling pygame.font
        rendered text.
        """
        parser = TextHTMLParser(self.ui_theme, self.element_ids, self.object_ids)
        parser.push_style('body', {"bg_colour": self.background_colour})
        parser.feed(self.html_text)

        self.formatted_text_block = TextBlock(parser.text_data,
                                              self.text_wrap_rect,
                                              parser.indexed_styles,
                                              self.font_dict,
                                              self.link_style,
                                              self.background_colour,
                                              self.wrap_to_height
                                              )

    def redraw_from_text_block(self):
        """
        Redraws the final parts of the text box element that don't include redrawing the actual
        text. Useful if we've just moved the position of the text (say, with a scroll bar)
        without actually changing the text itself.
        """
        if self.rect.width <= 0 or self.rect.height <= 0:
            return
        if self.scroll_bar is not None:
            height_adjustment = int(self.scroll_bar.start_percentage *
                                    self.formatted_text_block.final_dimensions[1])
        else:
            height_adjustment = 0

        drawable_area = pygame.Rect((0, height_adjustment),
                                    (self.text_wrap_rect[2], self.text_wrap_rect[3]))
        new_image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA, depth=32)
        new_image.fill(pygame.Color(0, 0, 0, 0))
        new_image.blit(self.background_surf, (0, 0))
        new_image.blit(self.formatted_text_block.block_sprite,
                       (self.padding[0] + self.border_width +
                        self.shadow_width + self.rounded_corner_offset,
                        self.padding[1] + self.border_width +
                        self.shadow_width + self.rounded_corner_offset),
                       drawable_area)

        self.set_image(new_image)

    def redraw_from_chunks(self):
        """
        Redraws from slightly earlier in the process than 'redraw_from_text_block'. Useful if we
        have redrawn individual chunks already (say, to change their style slightly after being
        hovered) and now want to update the text block with those changes without doing a
        full redraw.

        This won't work very well if redrawing a chunk changed it's dimensions.
        """
        self.formatted_text_block.redraw_from_chunks(self.active_text_effect)
        self.redraw_from_text_block()

    def full_redraw(self):
        """
        Trigger a full redraw of the entire text box. Useful if we have messed with the text
        chunks in a more fundamental fashion and need to reposition them (say, if some of them
        have gotten wider after being made bold).

        NOTE: This doesn't re-parse the text of our box. If you need to do that, just create a
        new text box.

        """
        self.formatted_text_block.redraw(self.active_text_effect)
        self.redraw_from_text_block()
        self.link_hover_chunks = []
        self.formatted_text_block.add_chunks_to_hover_group(self.link_hover_chunks)

    def focus(self):
        """
        Called when we focus the text box (usually by clicking on it). In this case we just pass
        the focus over to the box's scroll bar, if it has one, so that some input events will be
        directed that way.
        """
        if self.scroll_bar is not None:
            self.scroll_bar.focus()

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Deals with input events. In this case we just handle clicks on any links in the text.

        :param event: A pygame event to check for a reaction to.

        :return: Returns True if we consumed this event.

        """
        consumed_event = False
        should_redraw_from_chunks = False
        should_full_redraw = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            scaled_mouse_pos = (int(event.pos[0] * self.ui_manager.mouse_pos_scale_factor[0]),
                                int(event.pos[1] * self.ui_manager.mouse_pos_scale_factor[1]))
            if self.hover_point(scaled_mouse_pos[0], scaled_mouse_pos[1]):
                consumed_event = True
                if self.scroll_bar is not None:
                    text_block_full_height = self.formatted_text_block.final_dimensions[1]
                    height_adjustment = self.scroll_bar.start_percentage * text_block_full_height
                else:
                    height_adjustment = 0
                base_x = int(self.rect[0] + self.padding[0] + self.border_width +
                             self.shadow_width + self.rounded_corner_offset)
                base_y = int(self.rect[1] + self.padding[1] + self.border_width +
                             self.shadow_width + self.rounded_corner_offset - height_adjustment)
                for chunk in self.link_hover_chunks:

                    hover_rect = pygame.Rect((base_x + chunk.rect.x,
                                              base_y + chunk.rect.y),
                                             chunk.rect.size)
                    if hover_rect.collidepoint(scaled_mouse_pos[0], scaled_mouse_pos[1]):
                        consumed_event = True
                        if not chunk.is_selected:
                            chunk.on_selected()
                            if chunk.metrics_changed_after_redraw:
                                should_full_redraw = True
                            else:
                                should_redraw_from_chunks = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.scroll_bar is not None:
                height_adjustment = (self.scroll_bar.start_percentage *
                                     self.formatted_text_block.final_dimensions[1])
            else:
                height_adjustment = 0
            base_x = int(self.rect[0] + self.padding[0] + self.border_width +
                         self.shadow_width + self.rounded_corner_offset)
            base_y = int(self.rect[1] + self.padding[1] + self.border_width +
                         self.shadow_width + self.rounded_corner_offset - height_adjustment)
            scaled_mouse_pos = (int(event.pos[0] * self.ui_manager.mouse_pos_scale_factor[0]),
                                int(event.pos[1] * self.ui_manager.mouse_pos_scale_factor[1]))
            for chunk in self.link_hover_chunks:

                hover_rect = pygame.Rect((base_x + chunk.rect.x,
                                          base_y + chunk.rect.y),
                                         chunk.rect.size)
                if (hover_rect.collidepoint(scaled_mouse_pos[0], scaled_mouse_pos[1]) and
                        self.rect.collidepoint(scaled_mouse_pos[0], scaled_mouse_pos[1])):
                    consumed_event = True
                    if chunk.is_selected:
                        event_data = {'user_type': UI_TEXT_BOX_LINK_CLICKED,
                                      'link_target': chunk.link_href,
                                      'ui_element': self,
                                      'ui_object_id': self.most_specific_combined_id}
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_data))

                if chunk.is_selected:
                    chunk.on_unselected()
                    if chunk.metrics_changed_after_redraw:
                        should_full_redraw = True
                    else:
                        should_redraw_from_chunks = True

        if should_redraw_from_chunks:
            self.redraw_from_chunks()

        if should_full_redraw:
            self.full_redraw()

        return consumed_event

    def set_active_effect(self, effect_name: Union[str, None]):
        """
        Set an animation effect to run on the text box. The effect will start running immediately
        after this call.

        These effects are currently supported:

        - 'typing_appear' - Will look as if the text is being typed in.
        - 'fade_in' - The text will fade in from the background colour (Only supported on Pygame 2)
        - 'fade_out' - The text will fade out to the background colour (only supported on Pygame 2)

        :param effect_name: The name fo the t to set. If set to None instead it will cancel any
                            active effect.

        """
        if effect_name is None:
            self.active_text_effect = None
        elif isinstance(effect_name, str):
            if effect_name == TEXT_EFFECT_TYPING_APPEAR:
                effect = TypingAppearEffect(self.formatted_text_block.characters)
                self.active_text_effect = effect
                self.full_redraw()
            elif effect_name == TEXT_EFFECT_FADE_IN:
                effect = FadeInEffect(self.formatted_text_block.characters)
                self.active_text_effect = effect
                self.redraw_from_chunks()
            elif effect_name == TEXT_EFFECT_FADE_OUT:
                effect = FadeOutEffect(self.formatted_text_block.characters)
                self.active_text_effect = effect
                self.redraw_from_chunks()
            else:
                warnings.warn('Unsupported effect name: ' + effect_name + ' for text box')

    def rebuild_from_changed_theme_data(self):
        """
        Called by the UIManager to check the theming data and rebuild whatever needs rebuilding
        for this element when the theme data has changed.
        """
        has_any_changed = False

        # misc parameters
        shape_type = 'rectangle'
        shape_type_string = self.ui_theme.get_misc_data(self.object_ids, self.element_ids, 'shape')
        if shape_type_string is not None and shape_type_string in ['rectangle',
                                                                   'rounded_rectangle']:
            shape_type = shape_type_string
        if shape_type != self.shape_type:
            self.shape_type = shape_type
            has_any_changed = True

        if self._check_shape_theming_changed(defaults={'border_width': 1,
                                                       'shadow_width': 2,
                                                       'shape_corner_radius': 2}):
            has_any_changed = True

        padding = (5, 5)
        padding_str = self.ui_theme.get_misc_data(self.object_ids,
                                                  self.element_ids,
                                                  'padding')
        if padding_str is not None:
            try:
                padding = (int(padding_str.split(',')[0]), int(padding_str.split(',')[1]))
            except ValueError:
                padding = (5, 5)
        if padding != self.padding:
            self.padding = padding
            has_any_changed = True

        # colour parameters
        background_colour = self.ui_theme.get_colour_or_gradient(self.object_ids,
                                                                 self.element_ids,
                                                                 'dark_bg')
        if background_colour != self.background_colour:
            self.background_colour = background_colour
            has_any_changed = True

        border_colour = self.ui_theme.get_colour_or_gradient(self.object_ids,
                                                             self.element_ids,
                                                             'normal_border')
        if border_colour != self.border_colour:
            self.border_colour = border_colour
            has_any_changed = True

        if self._check_link_style_changed():
            has_any_changed = True

        if has_any_changed:
            self.rebuild()

    def _check_link_style_changed(self) -> bool:
        """
        Checks for any changes in hyper link related styling in the theme data.

        :return: True if changes detected.

        """
        has_any_changed = False
        # link styles
        link_normal_underline = True
        link_normal_underline_string = self.ui_theme.get_misc_data(self.object_ids,
                                                                   self.element_ids,
                                                                   'link_normal_underline')
        if link_normal_underline_string is not None:
            try:
                link_normal_underline = bool(int(link_normal_underline_string))
            except ValueError:
                link_normal_underline = True
        if link_normal_underline != self.link_normal_underline:
            self.link_normal_underline = link_normal_underline
        link_hover_underline = True
        link_hover_underline_string = self.ui_theme.get_misc_data(self.object_ids,
                                                                  self.element_ids,
                                                                  'link_hover_underline')
        if link_hover_underline_string is not None:
            try:
                link_hover_underline = bool(int(link_hover_underline_string))
            except ValueError:
                link_hover_underline = True
        if link_hover_underline != self.link_hover_underline:
            self.link_hover_underline = link_hover_underline
        link_normal_colour = self.ui_theme.get_colour_or_gradient(self.object_ids,
                                                                  self.element_ids,
                                                                  'link_text')
        if link_normal_colour != self.link_normal_colour:
            self.link_normal_colour = link_normal_colour
        link_hover_colour = self.ui_theme.get_colour_or_gradient(self.object_ids,
                                                                 self.element_ids,
                                                                 'link_hover')
        if link_hover_colour != self.link_hover_colour:
            self.link_hover_colour = link_hover_colour
        link_selected_colour = self.ui_theme.get_colour_or_gradient(self.object_ids,
                                                                    self.element_ids,
                                                                    'link_selected')
        if link_selected_colour != self.link_selected_colour:
            self.link_selected_colour = link_selected_colour
        link_style = {'link_text': self.link_normal_colour,
                      'link_hover': self.link_hover_colour,
                      'link_selected': self.link_selected_colour,
                      'link_normal_underline': self.link_normal_underline,
                      'link_hover_underline': self.link_hover_underline}
        if link_style != self.link_style:
            self.link_style = link_style
            has_any_changed = True
        return has_any_changed
