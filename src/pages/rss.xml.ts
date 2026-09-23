import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const articles = (await getCollection('articles')).sort(
    (a, b) => b.data.publishedDate.valueOf() - a.data.publishedDate.valueOf(),
  );
  const siteUrl = context.site?.toString().replace(/\/$/, '') || 'http://localhost:4321';

  const items = articles
    .map(
      (article) => `
    <item>
      <title><![CDATA[${article.data.title}]]></title>
      <link>${siteUrl}/posts/${article.id}/</link>
      <guid>${siteUrl}/posts/${article.id}/</guid>
      <description><![CDATA[${article.data.description}]]></description>
      <pubDate>${article.data.publishedDate.toUTCString()}</pubDate>
      <category>${article.data.category}</category>
    </item>`,
    )
    .join('');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>VoidStack</title>
    <link>${siteUrl}/</link>
    <description>Notes and practical lessons from building and investigating software systems.</description>
    ${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
