import json
import zipfile
from typing import Any, Dict, List, Union

import PIL
from PIL import Image

from pyxi.canvas import Canvas
from pyxi.palette import Palette
from pyxi.tileset import Tileset


class PyxelImage:
    __slots__ = ('_path', 'version', 'name', 'settings', 'canvas', 'palette', 'tileset', 'animations')

    def __init__(self, file: str):
        super().__init__()
        data = self._convert(file)
        self._path = file
        self.version = data['version']
        self.name = data['name']
        self.settings = {}
        self.canvas = Canvas(data['canvas'])
        self.palette = Palette(data['palette'])
        self.tileset = Tileset(data['tileset'])
        self.animations = data['animations']

    def get_tile(self) -> PIL.Image.Image:
        img = self.merge_layers()
        return img

    def merge_layers(self, skip_layers: List[Union[str, int]] = None) -> PIL.Image.Image:
        if skip_layers is None:
            skip_layers = []

        with zipfile.ZipFile(self._path, 'r') as f:
            base = Image.open(f.open(f'layer0.png'))

            for layer in range(self.canvas.layer_count):
                if layer not in skip_layers:
                    next_layer = Image.open(f.open(f'layer{layer}.png'))
                    base.paste(next_layer, (0, 0), next_layer.convert('RGBA'))

            return base

    def extract(self):
        with zipfile.ZipFile(self._path, 'r') as f:
            f.extractall('converted')

    @staticmethod
    def _convert(file: str) -> Dict[str, Any]:
        with zipfile.ZipFile(file, 'r') as f:
            doc_file = f.read('docData.json')
            return json.loads(doc_file)
