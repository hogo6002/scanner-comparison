var StaticServer = require('static-server');
var server = new StaticServer({
  rootPath: 'public',            // required, the root of the server file tree
  name: 'my-http-server',   // optional, will set "X-Powered-by" HTTP header
  port: 3000,               // optional, defaults to a random port
  host: '0.0.0.0',       // optional, defaults to any interface
  cors: '*',                 // optional, defaults to undefined
  followSymlink: true,      // optional, defaults to a 404 error
  templates: {
    index: 'foo.html',      // optional, defaults to 'index.html'
    notFound: '404.html'    // optional, defaults to undefined
  }
});

server.start(function () {
  console.log('Server listening to', server.port);
});
