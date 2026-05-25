import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const productSchema = z.object({
  name: z.string(),
  verdict: z.string(),
  priceRange: z.string(),
  bestFor: z.string(),
  rating: z.number().min(1).max(5),
  affiliateLink: z.string().min(1)
});

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string().min(80).max(180),
    category: z.enum(['huishoudelijk', 'keuken', 'schoonmaken', 'tuin']),
    rating: z.number().min(1).max(5),
    priceRange: z.string(),
    pros: z.array(z.string()).min(2),
    cons: z.array(z.string()).min(2),
    affiliateLinks: z.array(z.string().min(1)).min(1),
    date: z.coerce.date(),
    modelYear: z.number(),
    featuredProduct: z.string(),
    readingTime: z.string(),
    products: z.array(productSchema).min(5),
    related: z.array(z.string()).min(2).max(6),
    draft: z.boolean().default(false)
  })
});

export const collections = { reviews };
