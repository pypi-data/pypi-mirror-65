name = "DialogFlowPy"
from enum import Enum


class PlatformEnum(Enum):
    PLATFORM_UNSPECIFIED = 'PLATFORM_UNSPECIFIED'
    FACEBOOK = 'facebook'
    SLACK = 'slack'
    TELEGRAM = 'telegram'
    KIK = 'kik'
    SKYPE = 'skype'
    LINE = 'line'
    VIBER = 'viber'
    ACTIONS_ON_GOOGLE = 'google'


class ImageDisplayOptions(Enum):
    IMAGE_DISPLAY_OPTIONS_UNSPECIFIED = 'IMAGE_DISPLAY_OPTIONS_UNSPECIFIED'
    GRAY = 'GRAY'
    WHITE = 'WHITE'
    CROPPED = 'CROPPED'
    BLURRED_BACKGROUND = 'BLURRED_BACKGROUND'


class UrlTypeHint(Enum):
    URL_TYPE_HINT_UNSPECIFIED = 'URL_TYPE_HINT_UNSPECIFIED'
    AMP_ACTION = 'AMP_ACTION'
    AMP_CONTENT = 'AMP_CONTENT'


class ResponseMediaType(Enum):
    RESPONSE_MEDIA_TYPE_UNSPECIFIED = 'RESPONSE_MEDIA_TYPE_UNSPECIFIED'
    AUDIO = 'AUDIO'


class HorizontalAlignment(Enum):
    HORIZONTAL_ALIGNMENT_UNSPECIFIED = 'HORIZONTAL_ALIGNMENT_UNSPECIFIED'
    LEADING = 'LEADING'
    CENTER = 'CENTER'
    TRAILING = 'TRAILING'


class HelpersIntents(Enum):
    actions_intent_PERMISSION = "actions_intent_PERMISSION"
    actions_intent_OPTION = "actions_intent_OPTION"
    actions_intent_DATETIME = "actions_intent_DATETIME"
    actions_intent_SIGN_IN = "actions_intent_SIGN_IN"
    actions_intent_PLACE = "actions_intent_PLACE"
    actions_intent_CONFIRMATION = "actions_intent_CONFIRMATION"
    actions_intent_NEW_SURFACE = "actions_intent_NEW_SURFACE"


class TransactionHelpersIntents(Enum):
    actions_intent_DELIVERY_ADDRESS = "actions_intent_DELIVERY_ADDRESS"
    actions_intent_TRANSACTION_REQUIREMENTS_CHECK = "actions_intent_TRANSACTION_REQUIREMENTS_CHECK"
    actions_intent_TRANSACTION_DECISION = "actions_intent_TRANSACTION_DECISION"
    actions_intent_DIGITAL_PURCHASE_CHECK = "actions_intent_DIGITAL_PURCHASE_CHECK"
    actions_intent_COMPLETE_PURCHASE = "actions_intent_COMPLETE_PURCHASE"


class UserEngagementIntents(Enum):
    actions_intent_REGISTER_UPDATE = "actions_intent_REGISTER_UPDATE"
    actions_intent_CONFIGURE_UPDATES = "actions_intent_CONFIGURE_UPDATES"
