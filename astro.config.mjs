import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://kieskeuken.nl',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date()
    }),
    tailwind({
      applyBaseStyles: false
    })
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light'
    }
  },
  trailingSlash: 'always'
});
