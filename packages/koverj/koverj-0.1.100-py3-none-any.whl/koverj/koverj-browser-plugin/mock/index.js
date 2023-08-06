const jsonServer = require("json-server");
const server = jsonServer.create();
const middlewares = jsonServer.defaults();
const port = process.env.PORT || 8086;
const resp = require("./locators.json");

server.use(jsonServer.bodyParser);
server.use(middlewares);

server.get("/locators", (request, response) => {
  if (request.method === "GET") {
    const url = request.query.url;

    const f = filter(resp, (_, v) => {
      return v.urls.includes(url);
    });

    response.status(200).json(f);
  }
});

server.get("/builds", (request, response) => {
  if (request.method === "GET") {
    response.status(200).json([
      {
        id: 1,
        name: "8e1a757f-3496-427a-8a92-daca7c22828e"
      }
    ]);
  }
});

const filter = (obj, fun) =>
  Object.entries(obj).reduce(
    (prev, [key, value]) => ({
      ...prev,
      ...(fun(key, value) ? { [key]: value } : {})
    }),
    {}
  );

server.listen(port, () => {
  console.log("JSON Server is running");
});
