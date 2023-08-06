from typing import Any, Dict


class Layer:
    __slots__ = ('layer_id', 'blend_mode', 'alpha', 'hidden', 'name', 'muted', 'tile_references', 'soloed')

    def __init__(self, n: int, data: Dict[str, Any]):
        self.layer_id = n
        self.blend_mode = data['blendMode']
        self.alpha = data['alpha']
        self.hidden = data['hidden']
        self.name = data['name']
        self.muted = data['muted']
        self.tile_references = data['tileRefs']
        self.soloed = data['soloed']
