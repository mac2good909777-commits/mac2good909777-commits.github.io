import { defineCollection, z } from 'astro:content';

const articleSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  tags: z.array(z.string()).default([]),
  excerpt: z.string(),
  coverImage: z.string().optional(),
  author: z.string().default('張現傑'),
  sourceNote: z.string().optional(),
  draft: z.boolean().default(false),
  properties: z.array(z.string()).default([]),
});

export const collections = {
  'industry-data': defineCollection({ type: 'content', schema: articleSchema }),
  'market-view': defineCollection({ type: 'content', schema: articleSchema }),
  insights: defineCollection({ type: 'content', schema: articleSchema }),
};
