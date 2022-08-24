# python3 graph_generator.py && python -m SimpleHTTPServer

import json
from parameters import GRAPH
from parameters import SIZES

D3_obj = {
  "nodes": [], 
  "links": [],
}

visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue


def bfs(group, graph, node):
  if node not in visited:
    D3_obj["nodes"].append({"id": node, "group": group, "size": SIZES[node]})
    visited.append(node)
    queue.append(node)

    while queue:
      s = queue.pop(0) 

      for child in graph[s]:
        if child not in visited:
          visited.append(child)
          D3_obj["nodes"].append({"id": child, "group": group,"size": SIZES[child]})

          # create link between node and neighbor
          D3_obj["links"].append({"source": node, "target": child, "value": 10})

          queue.append(child)


group = 1
for component in GRAPH: 
  # note: graph may not be connected (separate components)
  bfs(group, GRAPH, component)
  group +=1


y = json.dumps(D3_obj)
print(D3_obj)

with open("D3_input.json", "w") as outfile:
    outfile.write(y)
