from typing import List, Dict, Any

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import FunnygameItem, item_data_table, item_table
from .Locations import (
    FunnygameLocation,
    location_data_table,
    location_table,
    locked_locations,
)
from .Options import FunnygameOptions
from .Regions import region_data_table
from .Rules import get_letter_rule


class FunnygameWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing the funny game.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Pake"],
    )

    tutorials = [setup_en]
    game_info_languages = ["en", "de"]


class FunnygameWorld(World):
    """The greatest game of all time."""

    game = "Funnygame"
    web = FunnygameWebWorld()
    options: FunnygameOptions
    options_dataclass = FunnygameOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> FunnygameItem:
        return FunnygameItem(
            name, item_data_table[name].type, item_data_table[name].code, self.player
        )

    def create_items(self) -> None:
        item_pool: List[FunnygameItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations(
                {
                    location_name: location_data.address
                    for location_name, location_data in location_data_table.items()
                    if location_data.region == region_name
                    and location_data.can_create(self)
                },
                FunnygameLocation,
            )
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(
                location_data_table[location_name].locked_item
            )
            self.get_location(location_name).place_locked_item(locked_item)

        # Set priority location for the Big Red Button!
        self.options.priority_locations.value.add("The Typing Room")

    def get_filler_item_name(self) -> str:
        return "A Cool Filler Item (No Satisfaction Guaranteed)"

    def set_rules(self) -> None:
        letter_rule = get_letter_rule(self)
        self.get_location("The Typing Room").access_rule = letter_rule
        # self.get_location("In the Player's Mind").access_rule = button_rule

        # Do not allow button activations on buttons.
        self.get_location("The Typing Room").item_rule = (
            lambda item: item.name != "The Ability to Type"
        )

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "The Urge to Type", self.player
        )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"color": self.options.tb_color.current_key}
