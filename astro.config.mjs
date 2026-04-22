import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 部署到 user-site repo：mac2good909777-commits.github.io（無子路徑）
export default defineConfig({
  site: 'https://mac2good909777-commits.github.io',
  integrations: [sitemap()],
  build: {
    format: 'directory',
  },
});
