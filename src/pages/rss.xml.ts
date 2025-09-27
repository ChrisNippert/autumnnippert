import rss from '@astrojs/rss'
import { getCollection } from 'astro:content'

export async function GET(context) {
  const posts = await getCollection('blog')
  return rss({
    title: 'Autumn – Blog',
    description: 'Notes on CS, AI/ML, and music',
    site: context.site ?? 'https://chrisnippert.com',
    items: posts
      .filter(p => !p.data.draft)
      .sort((a,b) => +new Date(b.data.date) - +new Date(a.data.date))
      .map(p => ({
        link: `/blog/${p.slug}`,
        title: p.data.title,
        pubDate: new Date(p.data.date),
        description: p.data.summary
      }))
  })
}
