import requests
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from settings import ACCESS_TOKEN, API_VERSION, my_id

API_URI = 'https://api.vk.com/method/'

# Список одногрупников, по которым будем искать друзей
SCREEN_NAMES = ['amaslo0', 'ruzakovskiy', 'spymsx1337', 'gendorosan', 'shis_213']

# Информация об одногрупниках
df_group = pd.DataFrame(columns=['main_friend', 'id', 'first_name', 'last_name'])
# Информация о друзьях одногрупников
df_friends = pd.DataFrame(columns=['main_friend', 'id', 'first_name', 'last_name'])
# Информация о друзьях друзьей одногрупников
df_friends_of_friends = pd.DataFrame(columns=['main_friend', 'id', 'first_name', 'last_name'])

friends_graph = nx.Graph()


# Вывод графа TODO сделать стилизацию
def print_graph(graph):
    nx.draw(graph, )
    plt.show()


# Получение информации об одногрупниках
def get_data_group(users_id_list):
    # Преобразование полученного списка в string
    users_id_str = ','.join(users_id_list)

    reply = requests.get(API_URI + 'users.get', params={
        'user_ids': users_id_str,
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION
    })

    # Если пришел ответ от сервера
    if reply.json():
        return reply.json()['response']
    else:
        raise Warning('No response from server')


# Получаем список друзей заданного пользователя
def get_friends(user_id):
    reply = requests.get(API_URI + 'friends.get', params={
        'user_id': user_id,
        'fields': 'name',
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION
    })

    # Если получили ответ от сервера
    if reply.json():
        return reply.json()['response']['items']
    else:
        raise Warning('No response from server')


# Построение графа
def build_graph():
    global df_group
    # Получаем информацию об одногрупниках
    group_list = get_data_group(SCREEN_NAMES)

    # Добавление полученной информации об одногрупниках в DataFrame
    if len(group_list) != 0:
        for item in group_list:
            df_group = df_group.append(
                {'main_friend': my_id, 'id': item['id'], 'first_name': item['first_name'],
                 'last_name': item['last_name']}, ignore_index=True)

    # Добавляем и соединяем вершины в графе
    #friends_graph.add_edge(df_group['main_friend'][0], df_group['id'][0])

    # Получаем информацию о друзьях одногрупников


# MAIN
build_graph()
print(df_group)
print_graph(friends_graph)
