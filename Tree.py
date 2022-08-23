# # node
# class Node:
#     def __init__(self, radius=1, name=None, children=[]):
#         self.radius = radius
#         self.name = name
#         self.children = children
import json
graph = {'vintage': ['sf', 'san'],
 'google': ['journey'],
 'restaurant': ['sushi', 'san', 'near'],
 'sushi': ['restaurant'],
 'san': ['restaurant', 'vintage'],
 'harvard': [],
 'princess': ['polly'],
 'polly': ['princess'],
 'near': ['restaurant'],
 'sf': ['vintage'],
 'movie': [],
 'tattoo': ['poker'],
 'food': ['asian'],
 'asian': ['food'],
 'check': [],
 'set': [],
 'target': [],
 'pant': [],
 'tech': [],
 'poker': ['tattoo'],
 'playing': [],
 'quantitative': [],
 'social': ['visualization'],
 'visualization': ['social', 'node'],
 'node': ['visualization'],
 'journey': ['google']}


# graph = {
#   'animal' : ['whale','dog'],
#   'whale' : [],
#   'dog' : [],
#   'letters' : ['A'],
#   'A' : [],
# }

D3_obj = {
  "nodes": [], 
  "links": [],
}

visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue

sizes = {'vintage': 11,
 'google': 10,
 'restaurant': 18,
 'sushi': 15,
 'san': 31,
 'harvard': 19,
 'princess': 13,
 'polly': 12,
 'near': 18,
 'sf': 13,
 'movie': 12,
 'tattoo': 14,
 'food': 26,
 'asian': 15,
 'check': 10,
 'set': 12,
 'target': 10,
 'pant': 15,
 'tech': 14,
 'poker': 17,
 'playing': 13,
 'quantitative': 10,
 'social': 11,
 'visualization': 27,
 'node': 12,
 'journey': 11}

def bfs(group, graph, node):
  if node not in visited:
    D3_obj["nodes"].append({"id": node, "group": group, "size": sizes[node]})
    visited.append(node)
    queue.append(node)

    while queue:
      s = queue.pop(0) 

      for child in graph[s]:
        if child not in visited:
          visited.append(child)
          D3_obj["nodes"].append({"id": child, "group": group,"size": sizes[child]})

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
