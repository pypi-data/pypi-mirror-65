chrome.storage.sync.get(["koverj_url", "activeBuild"], result => {
  const req = new XMLHttpRequest();
  req.open(
    "GET",
    `${result.koverj_url}/sitemap?buildId=${result.activeBuild}`,
    true
  );
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send();

  req.onreadystatechange = function() {
    // Call a function when the state changes.
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      const resp = JSON.parse(this.responseText);

      console.log(resp);
      // // create an array with nodes
      let nodes = new vis.DataSet(resp.nodes);
      console.log("nodes", nodes);
      //
      // // create an array with edges
      let edges = new vis.DataSet(resp.edges);
      console.log("edges", edges);

      const edgeFilters = document.getElementsByName("edgesFilter");

      function startNetwork(data) {
        const container = document.getElementById("mynetwork");
        const options = {
          autoResize: true,
          nodes: {
            shape: "dot",
            size: 20,
            font: {
              size: 15,
              color: "black"
            },
            borderWidth: 1
          },
          edges: {
            width: 2
          },
          physics: {
            barnesHut: {
              gravitationalConstant: -6000,
              springLength: 100,
              avoidOverlap: 1
            },
            stabilization: { iterations: 2500 },
            maxVelocity: 0.6
          },
          groups: {
            1: { color: "rgb(0,255,140)" },
            icons: {
              shape: "icon",
              icon: {
                face: "FontAwesome",
                code: "\uf0c0",
                size: 50,
                color: "orange"
              }
            },
            source: {
              color: { border: "white" }
            }
          }
        };

        let network = new vis.Network(container, data, options);
        network.once("beforeDrawing", function() {
          network.focus(2, {
            scale: 12
          });
        });
        network.once("afterDrawing", function() {
          network.fit({
            animation: {
              duration: 3000,
              easingFunction: "linear"
            }
          });
        });
      }

      /**
       * filter values are updated in the outer scope.
       * in order to apply filters to new values, DataView.refresh() should be called
       */
      let nodeFilterValue = "";
      const edgesFilterValues = {};

      let edgesArray = filteredEdges(resp.edges);
      console.log("edgesArray", edgesArray);
      createTestTitleNode(edgesArray, edgesFilterValues);

      /*
                        filter function should return true or false
                        based on whether item in DataView satisfies a given condition.
                      */
      const nodesFilter = node => {
        if (nodeFilterValue === "") {
          return true;
        }
        // switch (nodeFilterValue) {
        //     case "login":
        //         return node.label === "https://angular.realworld.io/login";
        //     case "register":
        //         return node.label === "https://angular.realworld.io/register";
        //     case "editor":
        //         return node.label === "https://angular.realworld.io/editor";
        //     case "settings":
        //         return node.label === "https://angular.realworld.io/settings";
        //     default:
        //         return true;
        // }
      };

      const edgesFilter = edge => {
        return edgesFilterValues[edge.title];
      };

      const nodesView = new vis.DataView(nodes, { filter: nodesFilter });
      const edgesView = new vis.DataView(edges, { filter: edgesFilter });

      edgeFilters.forEach(filter =>
        filter.addEventListener("change", e => {
          const { value, checked } = e.target;
          edgesFilterValues[value] = checked;
          edgesView.refresh();
        })
      );

      startNetwork({ nodes: nodesView, edges: edgesView });
    }
  };

  function filteredEdges(edges) {
    return edges.reduce((acc, current) => {
      const x = acc.find(item => item.title === current.title);
      if (!x) {
        return acc.concat([current]);
      } else {
        return acc;
      }
    }, []);
  }

  function createTestTitleNode(edgesArray, edgesFilterValues) {
    let testNames = document.getElementById("testNames");

    for (let index in edgesArray) {
      let edge = edgesArray[index];
      console.log(edge);
      let div = document.createElement("li");
      div.classList.add("list-group-item");
      let label = document.createElement("label");
      let input = document.createElement("input");
      input.setAttribute("type", "checkbox");
      input.setAttribute("name", "edgesFilter");
      input.setAttribute("value", edge.title);
      input.checked = true;
      label.appendChild(input);
      let text = document.createTextNode(edge.title);
      edgesFilterValues[edge.title] = true;
      label.appendChild(text);
      div.appendChild(label);
      testNames.appendChild(div);
    }
  }
});
