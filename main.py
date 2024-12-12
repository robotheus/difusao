import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import json
import random

"""
    Passos para o IC:
        - Definir o grafo: coautoria
        - Definir o seed inicial: 10%, 20%, 30%
        - Definir a probabilidade de cada aresta: p(w, v)/max(p)
"""

graph = nx.read_gml('grafo_clique.gml')

ranks       = ['dados/CG-G.json', 'dados/CI-G.json', 'dados/CP-G.json', 
               'dados/CG-HG-s=1.json', 'dados/CG-HG-s=2.json', 'dados/CG-HG-s=3.json',
               'dados/CI-HG-s=1.json', 'dados/CI-HG-s=2.json', 'dados/CI-HG-s=3.json',
               'dados/CP-HG-s=1.json', 'dados/CP-HG-s=2.json', 'dados/CP-HG-s=3.json',]

for rank in ranks:

    with open(rank, "r") as file:
        data = json.load(file)

    seeds = sorted(data.items(), key=lambda item: item[1], reverse=True)[:496] 
    seeds = [nome for nome, _ in seeds]

    model = ep.IndependentCascadesModel(graph)

    config = mc.Configuration()
    config.add_model_initial_configuration("Infected", seeds)

    # configuração da probabilidade de cada aresta - max = 19
    max_weight = max([data['weight'] for u, v, data in graph.edges(data=True)])

    for e in graph.edges(): 
        config.add_edge_configuration("threshold", e, (graph.edges()[e]['weight']/max_weight))

    model.set_initial_status(config)

    iterations = model.iteration_bunch(100, progress_bar=True, node_status=False)
    print(model.params)

    # limpar coisas que eu nao quero no resultado
    for i in iterations:
        for key in ["status", "status_delta"]:
            i.pop(key, None)

    with open(f"resultados/{rank.split(sep='/')[1]}", "w") as file:
        json.dump(iterations, file, indent=4)