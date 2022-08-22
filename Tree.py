# # node
# class Node:
#     def __init__(self, radius=1, name=None, children=[]):
#         self.radius = radius
#         self.name = name
#         self.children = children
import json

graph = {
  'animal' : ['whale','dog'],
  'whale' : [],
  'dog' : [],
  'letters' : ['A'],
  'A' : [],
}

D3_obj = {
  "nodes": [], 
  "links": [],
}

visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue


def bfs(group, graph, node):
  if node not in visited:
    D3_obj["nodes"].append({"id": node, "group": group})
    visited.append(node)
    queue.append(node)

    while queue:
      s = queue.pop(0) 

      for child in graph[s]:
        if child not in visited:
          visited.append(child)
          D3_obj["nodes"].append({"id": child, "group": group})

          # create link between node and neighbor
          D3_obj["links"].append({"source": node, "target": child, "group": 5})

          queue.append(child)

group = 1
for x in graph: 
  # note: graph may not be connected (separate components)
  bfs(group, graph, x)
  group +=1


y = json.dumps(D3_obj)
print(D3_obj)

with open("trial.json", "w") as outfile:
    outfile.write(y)
