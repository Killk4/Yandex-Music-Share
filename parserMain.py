import os
import requests
from time import sleep
from bs4 import BeautifulSoup

index = open('index.html', 'w', encoding='utf-8')
index.writelines('''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Музик</title>
  <!-- Подключаем файл стилей Bootstrap -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
</head>
<body>
  <div class="container">
    <div class="row">''')

# Функция для получения изображения и названия песни по ссылке на трек в Яндекс.Музыке
def get_song_info(url):
    sleep(.4)
    # Получаем HTML-код страницы с треком
    response = requests.get(f'https://music.yandex.ru/album/{url}')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Получаем название песни
    title_elem = soup.find('a', attrs={'href': f'/album/{url}'})
    title = title_elem.text.strip() if title_elem else ''

    # Получаем ссылку на изображение песни
    image_url_elem = soup.find('img', class_='entity-cover__image deco-pane')
    image_url = image_url_elem.get('src') if image_url_elem else ''
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    # Загружаем изображение и сохраняем в папку
    if image_url:
        response = requests.get(image_url)
        file_name = os.path.basename(image_url)
        with open(f'img/{title}.png', 'wb') as f:
            f.write(response.content)

    index.writelines(f'<div class="col-md-3 col-sm-12"><div class="card"><img src="img/{title}.png" class="card-img-top" alt="..."><div class="card-body"><h5 class="card-title">{title}</h5><a href="https://music.yandex.ru/album/{url}" target="_blank" class="btn btn-primary">Яндекс</a></div></div></div>')


with open('links.txt', 'r') as url:
    for line in url:
        modified_url = line.strip().replace("https://music.yandex.ru/album/", "")
        if(modified_url):
            get_song_info(modified_url)

index.writelines('''</div>
  </div>
  
</body>

<!-- Подключаем библиотеку jQuery (нужно подключить до скриптов Bootstrap) -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<!-- Подключаем файл скриптов Bootstrap (jQuery должен быть подключен раньше) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js" integrity="sha384-cuYeSxntonz0PPNlHhBs68uyIAVpIIOZZ5JqeqvYYIcEL727kskC66kF92t6Xl2V" crossorigin="anonymous"></script>

</html>''')

index.close()