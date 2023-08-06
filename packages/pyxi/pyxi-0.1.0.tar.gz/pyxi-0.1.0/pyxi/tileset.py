from typing import Any, Dict


class Tileset:
    __slots__ = ('fixed_width', 'tile_width', 'tile_height', 'tile_count', 'columns')

    def __init__(self, data: Dict[str, Any]):
        self.fixed_width = data['fixedWidth']
        self.tile_width = data['tileWidth']
        self.tile_height = data['tileHeight']
        self.tile_count = data['numTiles']
        self.columns = data['tilesWide']
