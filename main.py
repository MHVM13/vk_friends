import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from settings import ACCESS_TOKEN, API_VERSION, my_id

API_URI = 'https://api.vk.com/method/'

# Список одногрупников, по которым будем искать друзей
SCREEN_NAMES = ['amaslo0', 'ruzakovskiy', 'spymsx1337', 'gendorosan', 'shis_213']

# Все информация о друзьях
df_group = pd.DataFrame(columns=['main_friend', 'id', 'first_name', 'last_name'])

friends_graph = nx.Graph()


# Вывод графа TODO сделать стилизацию
def print_graph():
    pos = nx.spring_layout(friends_graph, scale=40, k=0.30, iterations=20)
    nx.draw(friends_graph, pos, with_labels=True, font_size=1)
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


# Функция добавления данных в DataFrame
def add_to_df(friends_list, main_id):
    global df_group

    if len(friends_list) != 0:
        for item in friends_list:
            df_group = df_group.append({'main_friend': main_id, 'id': item['id'], 'first_name': item['first_name'],
                                        'last_name': item['last_name']}, ignore_index=True)


# Функция построения графа и его отображения
def build_graph():
    global friends_graph

    for i in range(len(df_group)):
        friends_graph.add_edge(df_group['main_friend'][i], df_group['id'][i])

    print_graph()


# Основная логика
# group_list = get_data_group(SCREEN_NAMES)  # Список с информаций об одногрупниках
#
# # Добавление полученной информации об одногрупниках в DataFrame
# add_to_df(group_list, my_id)
# build_graph()
#
# friends_list = []  # Список с информаций о друзьях одногрупников
#
# for item in group_list:
#     friends_list = get_friends(str(item['id']))
#     add_to_df(friends_list, item['id'])
#
# build_graph()

# Добавляем и соединяем вершины в графе

    # Получаем информацию о друзьях одногрупников
