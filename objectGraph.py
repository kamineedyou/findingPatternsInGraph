import itertools
from operator import itemgetter

import networkx
import networkx as nx
import ocpa.objects.log.importer.ocel.factory as ocel_import_factory
import pandas as pd

import patternInGraph


##Notizen akutell funktioniert es schlecht für Graphen mit vielen nodes

def filter_graph_nodes(graphs: list[networkx.Graph], node_count: int) -> list[networkx.Graph]:
    return filter(lambda p: len(p) > node_count)


def read_oc_csv(log_path: str) -> pd.DataFrame:
    types = ["order", "delivery", "item"]
    event_df = pd.read_csv(log_path)
    print(event_df)
    for t in types:
        event_df[t] = event_df[t].map(
            lambda x: [y.strip() for y in x.split(',')] if isinstance(x, str) else [])
    event_df["event_id"] = list(range(0, len(event_df)))
    event_df.index = list(range(0, len(event_df)))
    return event_df


def get_object_graph(log: pd.DataFrame) -> networkx.Graph:
    log["event_index"] = log["event_id"]
    log.set_index("event_index")
    object_types = [c for c in log.columns if not c.startswith("event_")]
    print(object_types)
    ocel = log.copy()
    ocel["event_objects"] = ocel.apply(lambda x: set([(ot, o) for ot in object_types for o in x[ot]]),
                                       axis=1)
    OG = nx.Graph()
    things = ocel["event_objects"].explode(
        "event_objects").to_list()
    attributes = {(x, y): {"type": x} for (x, y) in things}
    OG.add_nodes_from(things)
    object_index = list(ocel.columns.values).index("event_objects")
    id_index = list(ocel.columns.values).index("event_id")
    edge_list = []
    # build object graph
    arr = ocel.to_numpy()
    for i in range(0, len(arr)):
        edge_list += list(itertools.combinations(
            arr[i][object_index], 2))
    edge_list = [x for x in edge_list if x]
    OG.add_edges_from(edge_list)
    nx.set_node_attributes(OG, attributes)
    return OG


df, _ = ocel_import_factory.apply(
    f"simulated-logs.jsonocel", parameters={'return_df': True})

df2 = read_oc_csv("order_process.csv")
df2.head(5)
print(len(df))
object_graph_json = get_object_graph(df)
sampled_df = df2.sample(frac=0.01, random_state=1)
print(len(sampled_df))
object_graph = get_object_graph(sampled_df)

sub_graphs = patternInGraph.find_all_sub_graphs(object_graph)
print("founda ll patterns")
count_sub_graph_list = [(current_graph, patternInGraph.count_isomorphic_graphs_in_list(current_graph, sub_graphs)) for
                        current_graph in
                        sub_graphs]
print("counting subgraph")
# count_sub_graph_list.sort(key=lambda x: (len(x[0].nodes), x[1]), reverse=True)

subgraph_count = filter_graph_nodes(count_sub_graph_list(count_sub_graph_list, 4))
print("filerred subgraph")
max_count_graph = max(subgraph_count, key=itemgetter(1))[0]
print("printing sub graphs")
print(max_count_graph)
patternInGraph.plot_graph(max_count_graph[0])
