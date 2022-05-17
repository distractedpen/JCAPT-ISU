import { fileURLToPath, URL } from "url";
import fs from "fs";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    https: {
      key: fs.readFileSync("../ssl/server.key"),
      cert: fs.readFileSync("../ssl/server.crt"),
    },
  },
});
