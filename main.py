import pygame
import requests
from io import BytesIO
from PIL import Image

if __name__ == '__main__':
    running = True
    pygame.init()
    coords = input().replace(' ', ',')
    scale = input()
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": coords,
        "spn": ",".join([scale, scale]),
        "l": "map"
    }
    response = requests.get(map_api_server, params=map_params)
    map = Image.open(BytesIO(response.content))

    screen = pygame.display.set_mode((800, 600))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        screen.blit(pygame.image.fromstring(map.tobytes(), map.size, map. mode), (0, 0))
        pygame.display.flip()
    pygame.quit()
