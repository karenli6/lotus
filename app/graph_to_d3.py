# convert node graph to D3 viz
import json

def graph_to_d3(GRAPH, SIZES, ROOTS):
  print('graph to d3:')
  print('sizes:', SIZES)

  D3_obj = {
    "nodes": [], 
    "links": [],
  }

  visited = [] # List to keep track of visited nodes.
  queue = []   # Initialize a queue

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
            D3_obj["links"].append({"source": s, "target": child, "value": 10})

            queue.append(child)


  group = 1
  for root in ROOTS:
    bfs(group, GRAPH, root)
    group +=1

  y = json.dumps(D3_obj)

  with open("D3_graph_input.json", "w") as outfile:
      outfile.write(y)
  
  return True
