from enum import Enum

from DialogFlowPy.Entity import Entity


class EntityOverrideMode(Enum):
    ENTITY_OVERRIDE_MODE_UNSPECIFIED = 'ENTITY_OVERRIDE_MODE_UNSPECIFIED'
    ENTITY_OVERRIDE_MODE_OVERRIDE = 'ENTITY_OVERRIDE_MODE_OVERRIDE'
    ENTITY_OVERRIDE_MODE_SUPPLEMENT = 'ENTITY_OVERRIDE_MODE_SUPPLEMENT'


class SessionEntityType(dict):
    """
            name
        string

        Required. The unique identifier of this session entity type. Format: projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>.

        <Entity Type Display Name> must be the display name of an existing entity type in the same agent that will be overridden or supplemented.

        entity_override_mode
        EntityOverrideMode

        Required. Indicates whether the additional data should override or supplement the developer entity type definition.

        entities[]
        Entity

        Required. The collection of entities associated with this session entity type.
    """

    def __init__(self, name: str, entity_overide_mode: EntityOverrideMode, entities: Entity) -> None:
        super().__init__()

        self['name'] = name
        self['entity_override_mode'] = entity_overide_mode
        self['entities'] = entities
