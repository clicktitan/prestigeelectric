import { cpSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const __dirname = dirname(fileURLToPath(import.meta.url));

const collectHtmlInputs = (directory) => {
  const inputs = {};

  const walk = (currentDir) => {
    for (const entry of readdirSync(currentDir)) {
      const absolutePath = join(currentDir, entry);
      const stats = statSync(absolutePath);

      if (stats.isDirectory()) {
        if (entry === "node_modules" || entry === "dist" || entry === "scripts" || entry === ".git") {
          continue;
        }
        walk(absolutePath);
        continue;
      }

      if (!entry.endsWith(".html")) {
        continue;
      }

      const relativePath = relative(directory, absolutePath);
      const inputName = relativePath.replace(/\.html$/, "");
      inputs[inputName] = absolutePath;
    }
  };

  walk(directory);
  return inputs;
};

const copyStaticAssets = () => ({
  name: "copy-static-assets",
  closeBundle() {
    const distDir = resolve(__dirname, "dist");
    const copyTargets = [
      ["site-content.json", "site-content.json"],
      ["robots.txt", "robots.txt"],
      ["sitemap.xml", "sitemap.xml"],
      ["llms.txt", "llms.txt"],
      ["assets", "assets"],
    ];

    for (const [source, destination] of copyTargets) {
      cpSync(resolve(__dirname, source), resolve(distDir, destination), { recursive: true });
    }
  },
});

export default defineConfig({
  plugins: [copyStaticAssets()],
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: collectHtmlInputs(__dirname),
    },
  },
});
