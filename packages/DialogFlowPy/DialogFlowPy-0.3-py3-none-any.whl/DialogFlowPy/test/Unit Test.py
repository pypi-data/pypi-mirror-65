import json
import unittest
from DialogFlowPy.Button import Button
from DialogFlowPy.CarouselItem import CarouselItem
from DialogFlowPy import PlatformEnum, ImageDisplayOptions, ResponseMediaType, UrlTypeHint
from DialogFlowPy.BrowseCarouselCard import BrowseCarouselCard
from DialogFlowPy.BrowseCarouselCardItem import BrowseCarouselCardItem
from DialogFlowPy.DialogFlow import DialogFlow
from DialogFlowPy.Image import Image
from DialogFlowPy.OpenUrlAction import OpenUrlAction
from DialogFlowPy.SelectOptionInfo import SelectOptionInfo
from GoogleActions.MediaObject import MediaObject
from DialogFlowPy.ListItem import ListItem
from DialogFlowPy.OpenUriAction import OpenUriAction


class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_browse_carouse():
        image_uri = 'https://favpng.com/png_view/button-red-button-download-icon-png/pFR9zznr'
        accessibility_text = 'test image text'
        image = Image(image_uri=image_uri,
                      accessibility_text=accessibility_text)
        uri = 'www.google.com'
        browse_carousel_card = BrowseCarouselCardItem(
            open_uri_action=OpenUrlAction(url=uri, url_type_hint=UrlTypeHint.AMP_ACTION),
            title='browse carousel card', description='test browse carousel', image=image, footer='test footer')
        b = BrowseCarouselCard(image_display_options=ImageDisplayOptions.BLURRED_BACKGROUND,
                               browse_carousel_card_items=[browse_carousel_card])
        print(b)

    @staticmethod
    def test_something():
        with open('request_data.json', 'r') as f:
            request_json = json.load(f)
        image_uri = 'https://favpng.com/png_view/button-red-button-download-icon-png/pFR9zznr'
        accessibility_text = 'test image text'
        image = Image(image_uri=image_uri,
                      accessibility_text=accessibility_text)
        select_option_info = SelectOptionInfo(key='select info key', synonyms=['synonym 1', 'synonym 2'])
        uri = 'www.google.com'

        dialog_flow = DialogFlow(request_json)

        dialog_flow.add_text_message(platform=PlatformEnum.ACTIONS_ON_GOOGLE, text_to_speech='this is test message')
        print('dialog_flow:', dialog_flow)

        dialog_flow.add_card(platform=PlatformEnum.ACTIONS_ON_GOOGLE, title='test card', subtitle='testing card',
                             image_uri=image_uri, formatted_text='test card', image_text='image text',
                             buttons=[Button(title='Button Title', open_uri_action=OpenUriAction(uri=uri))])
        print('dialog_flow:', dialog_flow)

        browse_carousel_card = BrowseCarouselCardItem(
            open_uri_action=OpenUrlAction(url=uri, url_type_hint=UrlTypeHint.AMP_ACTION), title='browse carousel card',
            description='test browse carousel', image=image, footer='test footer')
        dialog_flow.add_carousel_browse_card(platform=PlatformEnum.ACTIONS_ON_GOOGLE,
                                             image_display_options=ImageDisplayOptions.BLURRED_BACKGROUND,
                                             browse_carousel_card_items=[browse_carousel_card])
        print('dialog_flow:', dialog_flow)

        carousel_item = CarouselItem(title='carousel item', description='test carousel item', image=image,
                                     option_info=select_option_info)
        dialog_flow.add_carousel_select(platform=PlatformEnum.ACTIONS_ON_GOOGLE, carousel_items=[carousel_item])
        print('dialog_flow:', dialog_flow)

        dialog_flow.add_image(platform=PlatformEnum.ACTIONS_ON_GOOGLE, uri=uri, accessibility_text=accessibility_text)
        print('dialog_flow:', dialog_flow)

        list_item = ListItem(title='list item', description='list item test', image=image,
                             option_info=select_option_info)
        print('dialog_flow:', dialog_flow)

        dialog_flow.add_list_select(platform=PlatformEnum.ACTIONS_ON_GOOGLE, title='list select', subtitle='list',
                                    list_items=[list_item])
        print('dialog_flow:', dialog_flow)

        media_object = MediaObject(name='media object', description='test media object',
                                   content_url='https://s2.radio.co/se5e166e2f/listen#.mp3',
                                   large_image=Image(image_uri=uri, accessibility_text=accessibility_text),
                                   icon=image)
        dialog_flow.add_media(platform=PlatformEnum.ACTIONS_ON_GOOGLE, media_type=ResponseMediaType.AUDIO,
                              media_objects=[media_object])
        print('dialog_flow:', dialog_flow)

        dialog_flow.add_context(context_name='test context', lifespan=1, test_parameter='test parameter value')

        print('dialog_flow:', dialog_flow)
        dialog_flow.add_quick_replies(platform=PlatformEnum.ACTIONS_ON_GOOGLE, title='test_quick_replies',
                                      quick_replies=['suggestion1', 'suggestion2'])
        print('dialog_flow:', dialog_flow)

        dialog_flow.add_link_out_suggestion(platform=PlatformEnum.ACTIONS_ON_GOOGLE, uri=uri,
                                            destination_name='google search')
        print('dialog_flow:', dialog_flow)
        assert isinstance(dialog_flow, dict)
        assert json.dumps(dialog_flow)


if __name__ == '__main__':
    unittest.main()
