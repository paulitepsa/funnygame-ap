from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import FunnygameWorld


def get_letter_rule(world: "FunnygameWorld") -> Callable[[CollectionState], bool]:
    if world.options.hard_mode:
        return lambda state: state.has("The Ability to Type", world.player)

    return lambda state: True
