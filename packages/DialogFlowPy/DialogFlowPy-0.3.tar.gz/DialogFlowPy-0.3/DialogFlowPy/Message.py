from typing import Union, List

from DialogFlowPy import PlatformEnum, ImageDisplayOptions, ResponseMediaType
from DialogFlowPy.BasicCard import BasicCard
from DialogFlowPy.BrowseCarouselCard import BrowseCarouselCard
from DialogFlowPy.BrowseCarouselCardItem import BrowseCarouselCardItem
from DialogFlowPy.Button import Button
from DialogFlowPy.Card import Card
from DialogFlowPy.CarouselItem import CarouselItem
from DialogFlowPy.CarouselSelect import CarouselSelect
from DialogFlowPy.ColumnProperties import ColumnProperties
from DialogFlowPy.Image import Image
from DialogFlowPy.LinkOutSuggestion import LinkOutSuggestion
from DialogFlowPy.ListItem import ListItem
from DialogFlowPy.ListSelect import ListSelect
from DialogFlowPy.MediaContent import MediaContent
from DialogFlowPy.MediaObject import MediaObject
from DialogFlowPy.Payload import Payload
from DialogFlowPy.QuickReplies import QuickReplies
from DialogFlowPy.SimpleResponse import SimpleResponse
from DialogFlowPy.SimpleResponses import SimpleResponses
from DialogFlowPy.Suggestion import Suggestion
from DialogFlowPy.Suggestions import Suggestions
from DialogFlowPy.TableCard import TableCard
from DialogFlowPy.TableCardRow import TableCardRow
from DialogFlowPy.Text import Text


class Message(dict):
    """
    {
      "platform": enum(Platform),

      // Union field message can be only one of the following:
      "text": {
        object(Text)
      },
      "image": {
        object(Image)
      },
      "quickReplies": {
        object(QuickReplies)
      },
      "card": {
        object(Card)
      },
      "payload": {
        object
      },
      "simpleResponses": {
        object(SimpleResponses)
      },
      "basicCard": {
        object(BasicCard)
      },
      "suggestions": {
        object(Suggestions)
      },
      "linkOutSuggestion": {
        object(LinkOutSuggestion)
      },
      "listSelect": {
        object(ListSelect)
      },
      "carouselSelect": {
        object(CarouselSelect)
      },
      "browseCarouselCard": {
        object(BrowseCarouselCard)
      }.
      "tableCard": {
        object(TableCard)
      },
      "mediaContent": {
        object(MediaContent)
      }
      // End of list of possible types for union field message.
    }
    """

    def __init__(self, platform: PlatformEnum,
                 message_object: Union[Text, Image, QuickReplies, Card, SimpleResponses, BasicCard, Suggestions,
                                       LinkOutSuggestion, ListSelect, CarouselSelect, Payload, MediaContent, TableCard,
                                       BrowseCarouselCard]):
        super().__init__()

        self._message_type = None

        self.platform = platform

        self.message_object = message_object

    @property
    def platform(self):
        return PlatformEnum[self.get('platform')]

    @platform.setter
    def platform(self, platform: PlatformEnum):
        self['platform'] = platform.name

    @property
    def message_object(self):
        for item in self.values():
            if not isinstance(item, str):
                return item

    @message_object.setter
    def message_object(self, message_object):

        if isinstance(message_object, Text):
            self['text'] = message_object
            self._message_type = 'text'

        elif isinstance(message_object, Image):
            self['image'] = message_object
            self._message_type = 'image'

        elif isinstance(message_object, QuickReplies):
            self['quick_replies'] = message_object
            self._message_type = 'quick_replies'

        elif isinstance(message_object, Card):
            self['card'] = message_object
            self._message_type = 'card'

        elif isinstance(message_object, SimpleResponses):
            self['simple_responses'] = message_object
            self._message_type = 'simple_responses'

        elif isinstance(message_object, BasicCard):
            self['basic_card'] = message_object
            self._message_type = 'basic_card'

        elif isinstance(message_object, Suggestions):
            self['suggestions'] = message_object
            self._message_type = 'suggestions'

        elif isinstance(message_object, LinkOutSuggestion):
            self['link_out_suggestion'] = message_object
            self._message_type = 'link_out_suggestion'

        elif isinstance(message_object, ListSelect):
            self['list_select'] = message_object
            self._message_type = 'list_select'

        elif isinstance(message_object, CarouselSelect):
            self['carousel_select'] = message_object
            self._message_type = 'carousel_select'

        elif isinstance(message_object, BrowseCarouselCard):
            self['browse_carousel_card'] = message_object
            self._message_type = 'browse_carousel_card'

        elif isinstance(message_object, TableCard):
            self['tableCard'] = message_object
            self._message_type = 'table_card'

        elif isinstance(message_object, MediaContent):
            self['media_content'] = message_object
            self._message_type = 'media_content'

        elif isinstance(message_object, Payload):
            self['payload'] = message_object
            self._message_type = 'payload'

    @property
    def message_type(self):
        return self._message_type

    def add_text_message(self, platform: PlatformEnum, text_to_speech: str) -> Text:
        self.platform = platform
        text = Text(text_to_speech)
        self.message_object = text
        return text

    def add_image(self, platform: PlatformEnum, uri: str = '', accessibility_text: str = '') -> Image:
        self.platform = platform
        image = Image(image_uri=uri, accessibility_text=accessibility_text)
        self.message_object = image
        return image

    def add_quick_replies(self, platform: PlatformEnum, title, quick_replies: str) -> QuickReplies:
        self.platform = platform
        list_quick_replies: QuickReplies = QuickReplies(title=title, quick_replies=quick_replies)
        self.message_object = list_quick_replies
        return list_quick_replies

    def add_card(self, platform: PlatformEnum, title: str, subtitle: str, image_uri: str,
                 buttons: List[Button]) -> Card:
        self.platform = platform

        card: Card = Card(title=title, subtitle=subtitle, image_uri=image_uri, buttons=buttons)
        self.message_object = card
        return card

    # Google Actions Functions
    def add_simple_responses(self, platform: PlatformEnum, simple_responses: List[SimpleResponse]):
        self.platform = platform
        simple_responses: SimpleResponses = SimpleResponses(simple_responses)
        self.message_object = simple_responses
        return simple_responses

    def add_simple_response(self, platform: PlatformEnum, text_to_speech: str = '', ssml: str = '',
                            display_text: str = '') -> SimpleResponse:
        simple_response = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml,
                                         display_text=display_text)
        self.add_simple_responses(platform=platform, simple_responses=[simple_response])
        return simple_response

    def add_basic_card(self, platform: PlatformEnum, title: str = '', formatted_text: str = '', subtitle: str = '',
                       image_uri: str = '', image_text: str = '', buttons: List[Button] = None) -> BasicCard:
        if buttons is None:
            buttons = []

        self.platform = platform
        basic_card: BasicCard = BasicCard(title=title, formatted_text=formatted_text, subtitle=subtitle,
                                          image=Image(image_uri=image_uri, accessibility_text=image_text),
                                          buttons=buttons)
        self.message_object = basic_card
        return basic_card

    def add_suggestions(self, platform: PlatformEnum, titles: str) -> Suggestions:
        self.platform = platform
        suggestions_list = [Suggestion(title=item) for item in titles]
        suggestions: Suggestions = Suggestions(suggestions=suggestions_list)
        self.message_object = suggestions
        return suggestions

    def add_link_out_suggestion(self, platform: PlatformEnum, uri: str, destination_name: str) -> LinkOutSuggestion:
        self.platform = platform
        link_out_suggestion: LinkOutSuggestion = LinkOutSuggestion(uri=uri, destination_name=destination_name)
        self.message_object = link_out_suggestion
        return link_out_suggestion

    def add_list_select(self, platform: PlatformEnum, title: str, subtitle: str,
                        list_items: List[ListItem]) -> ListSelect:
        self.platform = platform
        list_select: ListSelect = ListSelect(title=title, subtitle=subtitle, list_items=list_items)
        self.message_object = list_select
        return list_select

    def add_carousel_select(self, platform: PlatformEnum, carousel_items: List[CarouselItem]) -> CarouselSelect:
        self.platform = platform
        carousel_select: CarouselSelect = CarouselSelect(carousel_items=carousel_items)
        self.message_object = carousel_select
        return carousel_select

    def add_browse_carousel_card(self, platform: PlatformEnum, image_display_options: ImageDisplayOptions,
                                 browse_carousel_card_items: List[BrowseCarouselCardItem]):
        self.platform = platform
        browse_carousel_card = BrowseCarouselCard(image_display_options=image_display_options,
                                                  browse_carousel_card_items=browse_carousel_card_items)
        self.message_object = browse_carousel_card
        return browse_carousel_card

    def add_table_card(self, platform: PlatformEnum, title: str, subtitle: str, image: Image,
                       column_properties: List[ColumnProperties], rows: List[TableCardRow], buttons: List[Button]):
        self.platform = platform
        table_card = TableCard(title=title, subtitle=subtitle, image=image, column_properties=column_properties,
                               rows=rows, buttons=buttons)
        self.message_object = table_card
        return table_card

    def add_media_content(self, platform: PlatformEnum, media_type: ResponseMediaType,
                          media_objects: List[MediaObject]):
        self.platform = platform
        media_content = MediaContent(media_type=media_type, media_objects=media_objects)
        self.message_object = media_content
        return self
