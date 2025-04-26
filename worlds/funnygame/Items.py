from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import FunnygameWorld


class FunnygameItem(Item):
    game = "Funnygame"


class FunnygameItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["FunnygameWorld"], bool] = lambda world: True


item_data_table: Dict[str, FunnygameItemData] = {
    "Guessed Right": FunnygameItemData(
        code=3551,
        type=ItemClassification.progression,
    ),
    "The Ability to Type": FunnygameItemData(
        code=3550,
        type=ItemClassification.progression,
        can_create=lambda world: world.options.hard_mode,
    ),
    "A Cool Filler Item (No Satisfaction Guaranteed)": FunnygameItemData(
        code=3549,
        can_create=lambda world: False,  # Only created from `get_filler_item_name`.
    ),
    "The Urge to Type": FunnygameItemData(
        type=ItemClassification.progression,
    ),
}

item_table = {
    name: data.code for name, data in item_data_table.items() if data.code is not None
}
