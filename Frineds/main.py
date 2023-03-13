import time
import scipy as sp
import networkx as nx
import matplotlib.pyplot as plt
from VK.getFriends import *
from VK.group_list import group_list
from CSV.file_direction import *


def visualize(graph):
    print("start visualize")

    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=50, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    nx.draw_networkx_labels(
        graph, pos, labels={node: graph.nodes[node]['name'] for node in graph.nodes()}, font_size=10)
    plt.axis('off')
    plt.show()
    plt.savefig('Graph')


def count_metrics(graph):
    print("start count metrics")
    print(f"diameter: {nx.diameter(graph)}")
    print(f"radius: {nx.radius(graph)}")
    print(f"central_vertices: {nx.center(graph)}")
    print(f"peripheral_vertices: {nx.periphery(graph)}")


    cliques = nx.find_cliques(graph)
    print(f"cliques: {cliques}")


    degree_centrality = nx.degree_centrality(graph)
    proximity_centrality = nx.closeness_centrality(graph)
    eigenvector_centrality = nx.eigenvector_centrality(graph)

    print(f"max_degree_centrality: {max(degree_centrality.values())}")
    print(f"max_proximity_centrality: {max(proximity_centrality.values())}")
    print(f"max_eigenvector_centrality: {max(eigenvector_centrality.values())}")



def remove_alone_friends(graph):
    to_remove = [node for node in graph.nodes() if graph.degree[node] == 1]
    graph.remove_nodes_from(to_remove)

def fill_graph_from_file(rows):
    before_classmate = ""
    before_friend = ""

    for row in rows:

        if before_classmate != row.classmate_id:
            graph.add_node(row.classmate_id, name=row.classmate_name)

        if before_friend != row.friend_id:
            graph.add_node(row.friend_id, name=row.friend_name)
            graph.add_edge(row.classmate_id, row.friend_id)

        graph.add_node(row.friend_of_friend_id, name=row.friend_of_friend_name)
        graph.add_edge(row.friend_id, row.friend_of_friend_id)

        before_classmate = row.classmate_id
        before_friend = row.friend_id


def parse_friends_from_vk(rows):
    for classmateId in group_list:
        print("--------------------------------------------------------------------------------------------------")
        name = get_name(classmateId)
        personsIds.append(classmateId)

        print(f"{name} {classmateId}")
        print("FRIENDS:")

        graph.add_node(classmateId, name=name)
        time_to_sleep = 0.3
        try:
            friendFriends = get_friends(classmateId)

            for friendId in friendFriends:
                if friendId not in personsIds:
                    time.sleep(time_to_sleep)
                    friend_name = get_name(friendId)


                    print(f"{friend_name} {friendId}")

                    graph.add_node(friendId, name=friend_name)
                    graph.add_edge(classmateId, friendId)
                    personsIds.append(friendId)

                    try:
                        friends_for_friend = get_friends(friendId)

                        for friend_id_for_friend in friends_for_friend:
                            time.sleep(time_to_sleep)
                            friend_for_friend_name = get_name(friend_id_for_friend)

                            print(f"{friend_for_friend_name} {friend_id_for_friend}")

                            graph.add_node(friend_id_for_friend, name=friend_for_friend_name)
                            graph.add_edge(friendId, friend_id_for_friend)
                            personsIds.append(friend_id_for_friend)

                            # собираем список друзей и друзей-друзей в список для дальнейшего сохранения в файл
                            rows.append(
                                Row(classmateId, name, friendId, friend_name, friend_id_for_friend,
                                    friend_for_friend_name))
                    except Exception as e:
                        print(f'{friend_name} is private or deleted')
                        print(e)

        except Exception as e:
            print(f'{name} is private or deleted')
            print(e)

    return rows


personsIds = []
graph = nx.Graph()


def main():
    rows = import_file()

    if len(rows) != 0:
        fill_graph_from_file(rows)
    else:
        rows = parse_friends_from_vk(rows)
        export(rows)

    remove_alone_friends(graph)
    visualize(graph)
    count_metrics(graph)


main()
