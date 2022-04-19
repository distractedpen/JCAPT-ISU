import { defineConfig } from "vite";
import fs from "fs";

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('/u1/h4/znoble1/ssl_certs/server.key'),
      cert: fs.readFileSync('/u1/h4/znoble1/ssl_certs/server.crt'),
    }
  }
});
