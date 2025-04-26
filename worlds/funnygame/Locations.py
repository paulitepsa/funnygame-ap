from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import FunnygameWorld


class FunnygameLocation(Location):
    game = "Funnygame"


class FunnygameLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["FunnygameWorld"], bool] = lambda world: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, FunnygameLocationData] = {
    "The Typing Room": FunnygameLocationData(
        region="The Funny Realm",
        address=3551,
    ),
    "The Player's Fingers": FunnygameLocationData(
        region="The Funny Realm",
        address=3550,
        can_create=lambda world: world.options.hard_mode,
    ),
    "In the Player's Mind": FunnygameLocationData(
        region="The Funny Realm",
        locked_item="The Urge to Type",
    ),
}
location_table = {
    name: data.address
    for name, data in location_data_table.items()
    if data.address is not None
}
locked_locations = {
    name: data for name, data in location_data_table.items() if data.locked_item
}
