import pygame
from typing import List
import sys
import json

from src.line import Line
from src.vector2d import Vector2D
try:
    from utils import load_img
except:
    from src.utils import load_img


class TileList:
    def __init__(self, path: str, th: int, tw: int):
        self.image: pygame.Surface = load_img(path)

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
    
class Tile:
    def __init__(self, img: pygame.Surface, rect: pygame.Rect):
        self.img: pygame.Surface = img
        self.rect: pygame.Rect = rect
        self.x: int = rect.x
        self.y: int = rect.y
        self.width: int = rect.width
        self.height: int = rect.height

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.img, self.rect)


class GameMap:
    def __init__(self, map_path, tile_list, scale: int):
        with open(map_path, "r") as f:
            self._map = json.load(f)
        self.scale = scale
        self._tile_list: TileList = tile_list
        self._tiles: list[Tile] = self.create_tiles()

    def size(self):
        return (self._map['height'], self._map['width'])
    
    def create_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        layer = self._map['layers'][0]['data']
        for i in range(self._map['height']):
            for j in range(self._map['width']):
                # obtem o tile na posicao (i, j)
                idx = i * self._map['width'] + j
                tile = layer[idx]

                if tile > 0:
                    img = self._tile_list.get(tile - 1)
                    img = pygame.transform.scale(img, (self._tile_list.width*self.scale, self._tile_list.height*self.scale))
                    px = j * self._tile_list.width*self.scale
                    py = i * self._tile_list.height*self.scale
                    rect = pygame.rect.Rect(px, py, self._tile_list.width*self.scale, self._tile_list.height*self.scale)

                    new_tile = Tile(img, rect)
                    tiles.append(new_tile)
        return tiles


    def draw(self, screen: pygame.surface.Surface):
        for tile in self._tiles:
            tile.draw(screen)

    def detect_tile_collision(self, entity_rect: pygame.Rect) -> Tile | None:
        for tile in self._tiles:
            if tile.rect.colliderect(entity_rect):
                return tile
        return None
    
    def detect_line_tile_collision(self, line: Line) -> Vector2D | None:
        for tile in self._tiles:
            positions = tile.rect.clipline(line.start_point.as_tuple(), line.end_point.as_tuple())
            if positions:
                pos1 = positions[0]
                return Vector2D(pos1[0], pos1[1])
        return None



def main():
    TILE_SIZE=16
    SCALE = 2
    pygame.init()
    screen = pygame.display.set_mode((30 * TILE_SIZE*SCALE, 20 * TILE_SIZE*SCALE))

    tile_list = TileList("../projetos/muiraquita/sprites/nature_elements/nature_tileset.png", TILE_SIZE, TILE_SIZE)
    level = GameMap("../projetos/muiraquita/maps/fase0.json", tile_list=tile_list)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        level.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()