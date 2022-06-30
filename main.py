# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import patternInGraph as pInG

if __name__ == '__main__':
    g = pInG.create_test_graph()
    pInG.plot_graph(g)
    sub_graphs = pInG.find_all_sub_graphs(g)
    pInG.visualize_graphs(sub_graphs)
    print(sub_graphs[8].nodes)
    print(pInG.count_isomorphic_graphs_in_list(sub_graphs[8], sub_graphs))

# def calculate cases add_deges is ende in obj.py
