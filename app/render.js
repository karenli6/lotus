
// flask server link
var serverhost = 'http://127.0.0.1:5000';
chrome.runtime.sendMessage('get-user-data', (response) => {
  console.log('got content: ', response);
  if (response){
    var url_req = serverhost + '/links';
    console.log("sending to this API: ", url_req)
    // fetch API
    fetch(url_req, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "urls": response })
    }).then(function (response) {
      return response.text();
    })
      .then(function (text) {
        console.log('POST response: ');
        // Should be 'OK' if everything was good
        console.log(text);
      });
  } else{
    console.log("NO NEW INFO WAS GOTTEN");
  }

});

/////
// visualize D3

// if want zoom: add this after d3.select("svg")
// .call(d3.zoom().on("zoom", function () {
//   svg.attr("transform", d3.event.transform)
// }))
var width = window.innerWidth * 0.5
var height =  window.innerHeight * 0.8

var svg = d3.select("svg");
  width = width,
  height = height;

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().distance(60).id(function (d) { return d.id; }))
  // .force("link", d3.forceLink().distance(function (d) { return d.size; }))
  .force("charge", d3.forceManyBody())
  .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("D3_graph_input.json", function (error, graph) {

  if (error) throw error;

  var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .style("stroke-width", 2)
    .style("stroke", "#709995");

  var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")

  var circles = node.append("circle")
    .attr("r", function (d) { return d.size; })
    .attr("fill", function (d) { return color(d.group); })
    .style("stroke", "white");


  // Create a drag handler and append it to the node object instead
  var drag_handler = d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);

  drag_handler(node);

  var label = node.append("text")
    .text(function (d) {
      return d.id;
    })
    .attr('x', 6)
    .attr('y', 3)
    .attr("font-size","14px");;

  node.append("title")
    .text(function (d) { return d.id; });

  simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

  simulation.force("link")
    .links(graph.links);

  function ticked() {
    link
      .attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    node
      .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      })
      .attr("cx", function(d) { return d.x = Math.max(d.size, Math.min(width - d.size, d.x)); })
      .attr("cy", function(d) { return d.y = Math.max(d.size, Math.min(height - d.size, d.y)); })

  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.1).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}