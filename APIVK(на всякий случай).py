import requests
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pprint import pprint
import yadisk
import json
import os
from tqdm import tqdm
from time import sleep
yandex_token = input("Введите токен YANDEX: ")
token = input("Введите токен VK: ")

url = "https://api.vk.com/method/photos.get"
#Первая функция для внесения параметров запроса
def get_params(vk_token):
    params = {
        "owner_id" : "1",
        "access_token" : token,
        "album_id" : "profile",
        "extended" : "1",
        "photo_sizes" : "1",
        "v" : "5.131"
    }
    res = requests.get(url, params=params)
    return res
#Тут просто извлекаем из json количество лайков
def get_likes(vk_token):
    for photos in get_params(vk_token).json()["response"]["items"]:
        file_likes = photos["likes"]["count"]   #кол-во лайков для названия файла
#А тут извлекаем из json дату публикации(на случай повторения количества лайков у двух фотографий)
    return file_likes
def get_date(token):
    for likes in get_params(token).json()["response"]["items"]:
        date_for_file = likes["date"]
    return date_for_file
# Получаем размер аватарки
def get_size(token):
    for sizes in get_params(token).json()["response"]["items"]:
        for size in sizes["sizes"]:
            for type_of_size in size["type"]:
                pass
    return type_of_size
#Получаем URL фотографии
def get_url(token):
    for sizes in get_params(token).json()["response"]["items"]:
        for size in sizes["sizes"]:
            for type_of_size in size["type"]:
                if type_of_size == "z":
                    url2 = size["url"]
                    break
                else:
                    pass
    return url2
#Создаем словарь для преобразования его в json
def create_dict():
    name_of_file = str(get_likes(token)) + "_" + str(get_date(token)) + ".jpg"
    new_dict = [{"file_name" : name_of_file, "size" : get_size(token)}]
    return new_dict
#Создаем json файл
def create_json():
    try:
        with open("new_json.txt", "x"):
            pass
    except:
        os.remove("new_json.txt")
        with open("new_json.txt", "x"):
            pass
create_json()
#JSON файл данного типо требуется на вывод по заданию
def write_and_read(dict, filename):
    dict = json.dumps(dict)
    dict = json.loads(str(dict))
    with open(filename, "w", encoding= "utf-8") as file:
        json.dump(create_dict(), file, indent=3)
    with open(filename, "r", encoding= "utf-8") as file2:
        print(file2.read())
#Производим сохранение фотографии
def save_photo():
    response = requests.get(get_url(token), stream=True).raw
    img = Image.open(response)
    img.save(f'{create_dict()[0]["file_name"]}')
#Отсылаем аватарку на Яндекс Диск
def yandex():
    y = yadisk.YaDisk(token=yandex_token)
    file = {create_dict()[0]["file_name"]}
    direct = "/Photos_From_VK" + "/" + create_dict()[0]["file_name"]
    for file_name in file:
        try:
            y.mkdir("/Photos_From_VK")
            y.upload(file_name, direct)
        except:
            try:
                y.upload(file_name, direct)
                print("\nФотография данного пользователя была успешно загружена")
            except:
                print("\nФотография данного пользователя уже сужествует")
save_photo()
write_and_read(create_dict(), "new_json.txt")
yandex()

