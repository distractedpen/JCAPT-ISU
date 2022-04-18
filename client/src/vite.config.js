import { defineConfig } from "vite";

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('/home/znoble1/ssl_certs/server.key'),
      cert: fs.readFileSync('/home/znoble1/ssl_certs/server.crt'),
    }
  }
});
