// source: https://www.digitalocean.com/community/tutorials/nodejs-serving-static-files-in-express

// eslint-disable-next-line no-undef
const express = require("express");
const app = express();
const HOST = "0.0.0.0";
const PORT = 8001;

app.use(express.static("dist"));

app.get("/", (req, res) => {
  res.send("CAPT-ISU");
});

app.listen(PORT, () =>
  console.log(`Server listening on port: http://${HOST}:${PORT}`)
);
