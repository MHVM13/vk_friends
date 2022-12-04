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
        # TODO проверка на существование пользователя и приватный ли у него профиль
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


# ОСНОВНАЯ ЛОГИКА
# Получение данных об одногрупниках и постороение графа с ними
group_list = get_data_group(SCREEN_NAMES)  # Список с информаций об одногрупниках
add_to_df(group_list, my_id)  # Добавление полученной информации об одногрупниках в DataFrame
build_graph()  # Построение графа одногрупников

# Получение данных о друзьях одногрупников и постороение графа с ними
counter = 0
friends_group_list = []  # Список друзей одногрупников

# Получение списка друзей одногрупников
for item in group_list:
    friends_group_list.append(get_friends(str(item['id'])))
    add_to_df(friends_group_list[counter], item['id'])
    counter += 1

build_graph()

# Получение списка друзей друзей одногрупников и построение графа с ними
print(friends_group_list) # TODO delete
for i in friends_group_list:
    for j in i:
        print(j)
        ff_list = get_friends(str(j['id']))
        add_to_df(ff_list, j['id'])



# Оценка центральности по посредничеству
print("Оценка центральности по посредничеству")
close_centrality = nx.closeness_centrality(friends_graph)
# TODO отсортировать значения по убыванию
print(close_centrality)

# Оценка центральности по близости
print("Оценка центральности по близости")
between_centrality = nx.betweenness_centrality(friends_graph, normalized = True, endpoints = False)
# TODO отсортировать значения по убыванию
print(between_centrality)

# Оценка центральности по собственному вектору
print("Оценка центральности по собственному вектору")
eigenvector_centrality = nx.eigenvector_centrality_numpy(friends_graph)
# TODO отсортировать значения по убыванию
print(eigenvector_centrality)