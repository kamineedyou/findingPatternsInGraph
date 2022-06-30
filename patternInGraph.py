import itertools

import matplotlib.pyplot as plt
import networkx
import networkx as nx


def find_all_sub_graphs2(g: networkx.Graph) -> list[networkx.Graph]:
    all_connected_sub_graphs = []
    # here we ask for all connected sub graphs that have at least 2 nodes AND have fewer nodes than the input graph
    for nb_nodes in range(2, g.number_of_nodes()):
        for sub_graph in (g.subgraph(selected_nodes) for selected_nodes in itertools.combinations(g, nb_nodes)):
            if nx.is_connected(sub_graph):
                all_connected_sub_graphs.append(sub_graph)
            if len(sub_graph.nodes) > 2:
                all_edges = sub_graph.edges
                for edge in all_edges:
                    temp_sg = nx.Graph(sub_graph)
                    temp_sg.remove_edge(*edge)
                    if nx.is_connected(temp_sg) and temp_sg not in all_connected_sub_graphs:
                        all_connected_sub_graphs.append(temp_sg)

    return all_connected_sub_graphs


def create_test_graph() -> networkx.Graph:
    g = nx.Graph()
    g.add_edges_from([("o1", "item2"), ("o1", "item3"), ("item3", "item2"), ("item2", "div3"), ("item3", "div3")])
    attributes = {"o1": {"type": "order"},
                  "item3": {"type": "item"},
                  "item2": {"type": "item"},
                  "div3": {"type": "delivery"}}
    nx.set_node_attributes(g, attributes)
    return g


def plot_graph(g: networkx.Graph) -> None:
    labels = nx.get_node_attributes(g, "type")
    print("priting the graph somehow")
    pos = nx.spring_layout(g)
    nx.draw(g, labels=labels, with_labels=True, )
    plt.show()


def find_all_sub_graphs(g: networkx.Graph) -> list[networkx.Graph]:
    all_connected_sub_graphs = []
    # here we ask for all connected sub graphs that have at least 2 nodes AND have fewer nodes than the input graph
    for nb_nodes in range(2, g.number_of_nodes()):
        for sub_graph in (g.subgraph(selected_nodes) for selected_nodes in itertools.combinations(g, nb_nodes)):
            if nx.is_connected(sub_graph):
                all_connected_sub_graphs.append(sub_graph)

    return all_connected_sub_graphs


def find_all_sub_graphs_dfs(g: networkx.Graph) -> list[networkx.Graph]:
    pass


def count_isomorphic_graphs_in_list(g: networkx.Graph, graphs: list[networkx.Graph]) -> int:
    counter: int = 0
    nm = nx.isomorphism.categorical_node_match("type", None)
    for subgraph in graphs:
        if nx.is_isomorphic(g, subgraph, node_match=nm):
            counter = counter + 1
    return counter


def visualize_graphs(graphs: list[networkx.Graph]) -> None:
    for sub_graph in graphs:
        plot_graph(sub_graph)
