import pygame
import requests
import os

if __name__ == '__main__':
    running = True
    pygame.init()
    coords = input().replace(' ', ',')
    scale = int(input())
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_file = 'map.png'
    screen = pygame.display.set_mode((600, 450))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        map_params = {
            "ll": coords,
            "spn": ",".join([str(scale), str(scale)]),
            "l": "map"
        }
        response = requests.get(map_api_server, params=map_params)
        with open(map_file, 'wb') as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)
