import pygame
import requests
import os


def get_map_parameters(json_response):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])

    map_params = {
        "ll": ll,
        "l": ['map', 'sat', 'sat,skl'][map_type],
        'pt': f'{ll},pm2ywm',
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


def draw_map_type_selection(screen):
    pygame.draw.rect(screen, 'black', (5, 455, 200, 40), 3)
    text = pygame.font.Font(None, 30).render(['Схема', 'Спутник', 'Гибрид'][map_type], True, 'black')
    screen.blit(text, (103 - text.get_width() // 2, 478 - text.get_height() // 2))


if __name__ == '__main__':
    running = True
    pygame.init()
    # coords = input().replace(' ', ',')
    font = pygame.font.Font(None, 20)
    font1 = pygame.font.Font(None, 25)
    flag = False
    scale = 17
    map_type = 0
    toponym_to_find = 'Санкт-Петербург, набережная Мойки, 14'
    input_field = pygame.Rect(220, 455, 300, 40)
    search_button = pygame.Rect(522, 455, 70, 40)
    map_file = 'map.png'
    screen = pygame.display.set_mode((600, 500))
    text = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if scale < 21:
                    scale += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if scale > 0:
                    scale -= 1
            if event.type == pygame.MOUSEBUTTONDOWN and 5 <= event.pos[0] <= 205 and 455 <= event.pos[1] <= 495:
                map_type = (map_type + 1) % 3
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_field.collidepoint(event.pos):
                    flag = True
                else:
                    flag = False
                if search_button.collidepoint(event.pos):
                    if text != '':
                        toponym_to_find = text
            if event.type == pygame.KEYDOWN and flag:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill((255, 255, 255))
        draw_map_type_selection(screen)
        screen.blit(font.render(text, True, 'black'), (input_field.x + 5, input_field.y + 5))
        screen.blit(font1.render('search', True, 'red'), (search_button.x + 8, search_button.y + 10))
        pygame.draw.rect(screen, 'black', input_field, 1)
        pygame.draw.rect(screen, 'black', search_button, 1)
        response = map(toponym_to_find)
        with open(map_file, 'wb') as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)
