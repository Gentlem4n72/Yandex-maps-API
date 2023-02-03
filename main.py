import pygame
import requests
import os


def get_map_parameters(json_response):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "l": "map",
        'z': scale
    }
    return map_params


def map(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    map_params = get_map_parameters(json_response)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response


if __name__ == '__main__':
    running = True
    pygame.init()
    # coords = input().replace(' ', ',')
    scale = 17
    toponym_to_find = 'Санкт-Петербург, набережная Мойки, 14'

    map_file = 'map.png'
    screen = pygame.display.set_mode((600, 450))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if scale < 21:
                    scale += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if scale > 0:
                    scale -= 1
        screen.fill((255, 255, 255))
        response = map(toponym_to_find)
        with open(map_file, 'wb') as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)
