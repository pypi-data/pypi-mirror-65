from typing import List
from DialogFlowPy import ImageDisplayOptions
from GoogleActions import MediaType
from GoogleActions.Button import Button
from GoogleActions.CarouselBrowseItem import CarouselBrowseItem
from GoogleActions.ExpectedIntent import ExpectedIntent
from GoogleActions.Extension import Extension
from GoogleActions.Item import Item
from GoogleActions.LinkOutSuggestion import LinkOutSuggestion
from GoogleActions.MediaObject import MediaObject
from GoogleActions.RichResponse import RichResponse
from GoogleActions.Suggestion import Suggestion
from GoogleActions import UrlTypeHint
from GoogleActions import Permission
from DialogFlowPy.BrowseCarouselCardItem import BrowseCarouselCardItem


class GooglePayload(dict):
    """Google data component to be added to DialogFlowOutput
    {
        'expectUserResponse': boolean,
        'userStorage': string
        'richResponse': GoogleRichResponse,
        'systemIntent': GoogleExpectedIntent,
    }

    """

    def __init__(self, expect_user_response: bool = True, rich_response: RichResponse = None, user_storage: str = '',
                 system_intent: ExpectedIntent = None):
        super().__init__()

        if expect_user_response is not None:
            self['expectUserResponse'] = expect_user_response

        if rich_response is not None:
            self['richResponse'] = RichResponse()

        if rich_response is not None:
            self['richResponse'] = rich_response

        if system_intent is not None:
            self['systemIntent'] = system_intent

        if user_storage is not None:
            self['userStorage'] = user_storage

    @property
    def expect_user_response(self):
        return self.get('expectUserResponse')

    @expect_user_response.setter
    def expect_user_response(self, value: bool):
        self['expectUserResponse'] = value

    @property
    def user_storage(self):
        return self.get('userStorage')

    @user_storage.setter
    def user_storage(self, value: str):
        self['userStorage'] = value

    @property
    def rich_response(self) -> RichResponse:
        return self.get('richResponse')

    @rich_response.setter
    def rich_response(self, value):
        self['richResponse'] = value

    @property
    def system_intent(self) -> ExpectedIntent:
        return self.get('systemIntent')

    @system_intent.setter
    def system_intent(self, system_intent: ExpectedIntent):
        self['systemIntent'] = system_intent

    def add_system_intent(self, intent: str = '', parameter_name: str = '', input_value: Extension = None) \
            -> ExpectedIntent:

        self['systemIntent'] = ExpectedIntent(intent=intent, parameter_name=parameter_name, input_value=input_value)
        return self.system_intent

    def add_rich_response(self, items_list: List[Item] = None, suggestions: List[Suggestion] = None,
                          link_name: str = '',
                          link_url: str = '') -> RichResponse:

        self['richResponse'] = RichResponse(item_list=items_list, suggestions=suggestions,
                                            link_out_suggestion=LinkOutSuggestion(url=link_url,
                                                                                  destination_name=link_name))
        return self.rich_response

    def add_items_to_rich_response(self, items) -> RichResponse:
        if self.rich_response is None:
            self['richResponse'] = RichResponse()
        self.rich_response.add_items(items)
        return self.rich_response

    def add_simple_response(self, text_to_speech: str, ssml: str = '', display_text: str = ''):
        print('richResponse', self['richResponse'])
        if self.rich_response is None:
            self['richResponse'] = RichResponse()

        self.rich_response.add_simple_response(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text)

        return self.rich_response

    def add_basic_card(self, title: str = '', formatted_text: str = '', subtitle: str = '', image_uri: str = '',
                       image_text: str = '', image_height: int = 0, image_width: int = 0,
                       image_display_options: ImageDisplayOptions = None, buttons=None):
        if buttons is None:
            buttons = []

        google_buttons = [Button(title=button.title, open_url_action=button.open_uri_action) for button in buttons]

        if self.rich_response is None:
            self['richResponse'] = RichResponse()
        self.rich_response.add_basic_card(title=title, formatted_text=formatted_text, subtitle=subtitle,
                                          image_url=image_uri, image_text=image_text, image_height=image_height,
                                          image_width=image_width, image_display_options=image_display_options,
                                          buttons=google_buttons)

        return self.rich_response

    def add_carousel_select(self):
        return NotImplementedError('Carousel select doesnt exist in Payload')

    def add_carousel_browse(self, image_display_options, browse_carousel_card_items: List[BrowseCarouselCardItem]):
        if self.rich_response is None:
            self['richResponse'] = RichResponse()

        google_browse_carousel_items = [
            CarouselBrowseItem(title=item.title, description=item.description, footer=item.footer, image=item.image,
                               open_url_action=item.open_uri_action) for item in browse_carousel_card_items]
        self.rich_response.add_carousel_browse(image_display_options=image_display_options,
                                               carousel_browse_items=google_browse_carousel_items)

        return self.rich_response

    def add_table_card(self, title: str, subtitle: str, image_uri: str, accessibility_text: str, image_height: int,
                       image_width: int, column_properties, rows, buttons):
        if self.rich_response is None:
            self['richResponse'] = RichResponse()

        google_buttons = [Button(title=button.title, open_url_action=button.open_uri_action) for button in buttons]

        self.rich_response.add_table_card(title=title, subtitle=subtitle, image_uri=image_uri,
                                          accessibility_text=accessibility_text, image_height=image_height,
                                          image_width=image_width, column_properties=column_properties, rows=rows,
                                          buttons=google_buttons)
        return self.rich_response

    def add_structured_response(self, receipt=None, info_extension=None,
                                return_info=None,
                                user_notification=None, rejection_info=None, update_time=None,
                                line_item_updates=None, fulfillment_info=None,
                                total_price=None,
                                in_transit_info=None, action_order_id=None,
                                cancellation_info=None,
                                order_state=None, google_order_id=None,
                                order_management_actions_list=None) -> RichResponse:

        if self.rich_response is None:
            self['richResponse'] = RichResponse()
        self.rich_response.add_structured_response(receipt=receipt, info_extension=info_extension,
                                                   return_info=return_info, user_notification=user_notification,
                                                   rejection_info=rejection_info, update_time=update_time,
                                                   line_item_updates=line_item_updates,
                                                   fulfillment_info=fulfillment_info, total_price=total_price,
                                                   in_transit_info=in_transit_info, action_order_id=action_order_id,
                                                   cancellation_info=cancellation_info, order_state=order_state,
                                                   google_order_id=google_order_id,
                                                   order_management_actions_list=order_management_actions_list)
        return self.rich_response

    def add_media_response(self, media_type: MediaType, media_objects: List[MediaObject]) -> RichResponse:
        if self.rich_response is None:
            self['richResponse'] = RichResponse()

        self.rich_response.add_media_response(media_type=media_type, media_objects=media_objects)
        return self.rich_response

    def add_html_region(self):
        return NotImplementedError('Not Implemented')

    def add_suggestions(self, titles: str):
        print('adding suggestions inside GooglePayload: ', titles)
        if self.rich_response is None:
            self['richResponse'] = RichResponse()
        self.rich_response.add_suggestions(titles)
        return self.rich_response

    def add_link_out_suggestions(self, url: str, destination_name: str):
        print('adding link_out_suggestions inside GooglePayload: ', url, destination_name)
        if self.rich_response is None:
            self['richResponse'] = RichResponse()
        self.rich_response.add_link_out_suggestion(url=url, destination_name=destination_name)
        return self.rich_response

    # Helper intents

    def request_confirmation(self, request_confirmation_text: str):
        """
        Obtain a confirmation from the user (for example, an answer to a yes or no question).
        :return:  bool
        """

        self.system_intent.request_confirmation(request_confirmation_text=request_confirmation_text)

        return self.system_intent

    def request_date_time(self, date_time_text: str = '', date_text: str = '', time_text: str = ''):
        """
        Obtain a date and time input from the user.
        :return: bool
        """

        self.system_intent.request_date_time(date_time_text=date_time_text, date_text=date_text, time_text=time_text)
        return self.system_intent

    def request_place(self):
        """
        Obtain an address or saved location from the user.
        :return: bool
        """
        self.system_intent.request_place()
        return self.system_intent

    def request_delivery_address(self, reason: str = ''):
        """
        Obtain a delivery address input from the user.
        :return: bool
        """

        self.system_intent.request_delivery_address(reason=reason)
        return self.system_intent

    def request_link(self, url: str = '', package_name: str = '', type_hint: UrlTypeHint = None,
                     version_tuples: tuple = None):
        """
        Requests a deep link flow into another platform.
        :return: bool
        """
        self.system_intent.request_link(url=url, package_name=package_name, type_hint=type_hint,
                                        version_tuples=version_tuples)
        return self.system_intent

    def request_select_option(self):
        """
        Receive the selected item from a list or carousel UI.
        :return: bool
        """
        self.system_intent.request_select_option()
        return self.system_intent

    def request_permission(self, opt_context_text: str = '', permissions: List[Permission] = None):
        """
        Obtain the user's full name, coarse location, or precise location, or all 3.
        :return: bool
        """

        self.system_intent.request_permission(opt_context_text=opt_context_text, permissions=permissions)
        return self.system_intent

    def request_sign_in(self, opt_context_text: str = ''):
        """
        Requests an account linking flow to link a user's account.
        :return: bool
        """
        self.system_intent.request_sign_in(opt_context_text=opt_context_text)
        return self.system_intent

    def request_new_surface(self):
        self.system_intent.request_new_surface()
        return self.system_intent

    def request_transaction_requirements_check(self):
        self.system_intent.request_transaction_requirements_check()
        return self.system_intent

    def request_transaction_decision(self):
        self.system_intent.request_transaction_decision()
        return self.system_intent

    def request_register_update(self):
        self.system_intent.request_register_update()
        return self.system_intent
