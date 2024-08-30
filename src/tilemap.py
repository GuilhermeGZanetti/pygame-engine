import pygame
from typing import List
import sys
import json
try:
    from utils import load_img
except:
    from src.utils import load_img


class TileList:
    def __init__(self, path: str, th: int, tw: int):
        self.image = load_img(path)

        self.height = th
        self.width = tw

        w, h = self.image.get_size()
        num_tiles_cols = w // th
        num_tiles_rows = h // tw

        if (h % th != 0) or (w % tw != 0):
            print("Image size in TileList should be proportional to tile size.")
            sys.exit(0)

        self._tiles = []
        for i in range(num_tiles_rows):
            for j in range(num_tiles_cols):
                tile = self.image.subsurface((j * tw, i * th, tw, th))
                self._tiles.append(tile)

    def size(self):
        return (self.height, self.width)

    def get(self, idx: int):
        if idx < 0 or idx >= len(self._tiles):
            print(f"Warning: idx '{idx}' not found in TileList.")

        return self._tiles[idx]


class GameMap:
    def __init__(self, map_path):
        with open(map_path, "r") as f:
            self._map = json.load(f)

    def size(self):
        return (self._map['height'], self._map['width'])

    def draw(self, screen: pygame.surface.Surface, tile_list: TileList, scale: float = 1.0):
        for layer in self._map['layers']:
            self._draw_matrix(screen, layer['data'], tile_list, scale)

    def _draw_matrix(self, screen: pygame.surface.Surface, matrix: List[int], tile_list: TileList, scale: float):
        for i in range(self._map['height']):
            for j in range(self._map['width']):
                # obtem o tile na posicao (i, j)
                idx = i * self._map['width'] + j
                tile = matrix[idx]

                if tile > 0:
                    img = tile_list.get(tile - 1)
                    img = pygame.transform.scale(img, (tile_list.width*scale, tile_list.height*scale))

                    # desenha o tile na tela
                    px = j * tile_list.width*scale
                    py = i * tile_list.height*scale
                    rect = pygame.rect.Rect(px, py, tile_list.width*scale, tile_list.height*scale)
                    screen.blit(img, rect)


def main():
    TILE_SIZE=16
    SCALE = 2
    pygame.init()
    screen = pygame.display.set_mode((30 * TILE_SIZE*SCALE, 20 * TILE_SIZE*SCALE))

    level = GameMap("../projetos/muiraquita/maps/fase0.json")
    tile_list = TileList("../projetos/muiraquita/sprites/nature_elements/nature_tileset.png", TILE_SIZE, TILE_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        level.draw(screen, tile_list, scale=SCALE)
        pygame.display.flip()


if __name__ == "__main__":
    main()