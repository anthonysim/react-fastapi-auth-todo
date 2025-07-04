import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// No router plugin here
export default defineConfig({
  plugins: [react()],
});
