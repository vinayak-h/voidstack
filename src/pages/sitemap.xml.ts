import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const articles = await getCollection('articles');
  const siteUrl = context.site?.toString().replace(/\/$/, '') || 'http://localhost:4321';

  const staticPaths = ['/', '/archive/', '/about/'];
  const postPaths = articles.map((article) => `/posts/${article.id}/`);
  const urls = [...staticPaths, ...postPaths];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((path) => `  <url><loc>${siteUrl}${path}</loc></url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
