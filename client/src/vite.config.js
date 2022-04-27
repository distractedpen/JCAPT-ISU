import { defineConfig } from "vite";
import fs from "fs";

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('/home/pengu/ssl_certs/server.key'),
      cert: fs.readFileSync('/home/pengu/ssl_certs/server.crt'),
    }
  }
});
