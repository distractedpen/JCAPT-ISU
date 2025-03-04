// source: https://www.digitalocean.com/community/tutorials/nodejs-serving-static-files-in-express

// eslint-disable-next-line no-undef
const express = require("express");
const fs = require("fs");
const https = require("node:https");
const dotenv = require("dotenv");
dotenv.config();

const app = express();
const HOST = process.env.EXPRESS_CLIENT_HOST;
const PORT = process.env.EXPRESS_CLIENT_PORT;

app.use(express.static("dist"));

app.get("/", (req, res) => {
  res.send("CAPT-ISU");
});

const key = fs.readFileSync("../ssl/server.key");
const cert = fs.readFileSync("../ssl/server.crt");

console.log(`Frontend hosted at https://${HOST}:${PORT}/`);

https
  .createServer(
    {
      key: key,
      cert: cert,
    },
    app
  )
  .listen(PORT);
