from typing import Dict, List, NamedTuple


class FunnygameRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, FunnygameRegionData] = {
    "Menu": FunnygameRegionData(["The Funny Realm"]),
    "The Funny Realm": FunnygameRegionData(),
}
