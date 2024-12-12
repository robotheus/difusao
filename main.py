import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import json
import matplotlib.pyplot as plt

graph = nx.read_gml('grafo_clique.gml')

with open("CG-G.json", "r") as file:
    data = json.load(file)

model = ep.IndependentCascadesModel(graph)

seeds = dict(sorted(data.items(), key=lambda item: item[1], reverse=True)[:500]) # top 500 no rank

config = mc.Configuration()

for node in graph.nodes():
    if node in seeds:
        config.add_node_configuration("status", node, 1) # 1 é ativado
    else:
        config.add_node_configuration("status", node, 0) # 0 é não ativado

model.set_initial_status(config)

iterations = model.iteration_bunch(200, progress_bar=True, node_status=False)

with open("resultado.json", "w") as file:
    json.dump(iterations, file, indent=4)