---
name: review-astro-seo
description:
  Audit Astro websites for SEO compliance using Astro SEO best practices. Use this skill
  whenever the user asks to review, audit, check, or improve SEO for an Astro site, mentions Astro
  SEO, structured data, canonical URLs, sitemaps, robots.txt, Pagefind, llms.txt, JSON-LD, Core Web
  Vitals, or wants to optimize an Astro site for search engines or AI crawlers. Make sure to trigger
  this skill even if the user doesn't explicitly mention "SEO audit" but is working on an Astro
  site's metadata, schema, crawlability, or indexing.
---

# Review Astro SEO

Audit Astro-based websites against comprehensive Astro SEO best practices, covering 20 key tactics
ranked by impact for both traditional search engines and AI crawlers. This skill guides you through a
structured audit, explains why each tactic matters, and helps you deliver actionable fixes.

## Pre-Audit Check

First, confirm the project is an Astro site:

- Look for `astro.config.mjs` or `astro.config.ts` in the project root
- Check `package.json` for `astro` as a dependency or devDependency
- If the project uses content collections, check the `src/content/` directory and
  `src/content/config.ts`

If it is not an Astro project, inform the user this skill is only for Astro-based sites.

## Audit Workflow

Work through the 20 tactics below in order of impact (highest first). For each, check the relevant
project files, record the result, and note any issues.

### 1. Canonical URLs on Every Page

**Why it matters**: Duplicate URLs (with/without trailing slashes, query params, pagination) split
your ranking signal. Canonical URLs collapse these into a single authoritative URL.

- Check all layout components (e.g., `src/layouts/`) for `<link rel="canonical">` tags
- Verify the canonical URL matches the page's `og:url` meta tag
- Check paginated pages (if using Astro's pagination) use the paginated URL as their canonical
- **Common issue**: Mismatched canonical and `og:url` tags
- **Fix**: Add a canonical URL helper (e.g., `getCanonical()` from `Astro.url.pathname` + site URL)
  and inject it into the head via `<Fragment slot="head">`

### 2. Title Tag Rules

**Why it matters**: Title tags are the biggest click-through rate (CTR) lever for search results.

- Check all pages have unique title tags between 50-60 characters
- Verify the primary keyword is near the start of the title
- Ensure titles do not exactly match the page's `<h1>` (titles are for SERPs, H1s for the page
  itself)
- **Common issue**: Generic titles like "Welcome to my blog"
- **Fix**: Use descriptive, keyword-first titles (e.g., "Astro SEO Checklist: 20 Tactics Ranked
  by Impact")

### 3. Article/BlogPosting JSON-LD with Person & Validation

**Why it matters**: Schema.org structured data enables rich results (star ratings, breadcrumbs) in
Google, and validates your content's authorship for E-E-A-T.

- Check for `application/ld+json` script tags in the head of blog posts/pages
- Verify the schema includes `@type: Article` or `BlogPosting`, `headline`, `description`, `image`
  (as `ImageObject` with width/height), `datePublished`, `dateModified`, `author` (Person schema),
  `publisher` (Organization schema)
- Validate the JSON-LD using [Google Rich Results Test](https://search.google.com/test/rich-results)
  and [Schema.org Validator](https://validator.schema.org/)
- **Common issue**: Using a bare string for `image` instead of `ImageObject`
- **Fix**: Use helper functions (e.g., `getArticleSchema()`, `getPersonSchema()`) in a central file
  like `src/helpers/schema.ts`, inject via `<Fragment slot="head">`

### 4. Per-Post Open Graph & Twitter Cards

**Why it matters**: Social platforms (LinkedIn, Slack, X) use Open Graph/Twitter Card meta tags to
render link previews. Good previews increase CTR when links are shared.

- Check for `og:title`, `og:description`, `og:url`, `og:type`, `og:image` (with width/height) meta
  tags
- Verify Twitter Card tags: `twitter:card` (summary or summary_large_image), `twitter:site`,
  `twitter:creator`
- Check blog posts include Open Graph article extensions: `article:published_time`,
  `article:modified_time`, `article:author`, `article:section`, `article:tag`
- **Common issue**: Missing `og:image` leading to blank preview rectangles
- **Fix**: Default to the post's hero image, fall back to a site-wide default OG image in your
  layout

### 5. Unique Meta Description on Every Key Page

**Why it matters**: Meta descriptions are the snippet under your blue link in Google search results.
Unique, descriptive descriptions increase CTR.

- Check home, blog index, category, tag, and post pages have unique meta descriptions between
  150-160 characters
- Avoid using the site-wide default description for all pages
- **Common issue**: Duplicate meta descriptions across multiple pages
- **Fix**: Write a factual, topic-specific description for each key page that mentions the page's
  content and source

### 6. One `<h1>` Per Page, Logical Heading Order

**Why it matters**: Clear heading structure helps search engines understand page hierarchy, and
improves accessibility.

- Check each page has exactly one `<h1>` tag
- Verify heading order is logical: `<h1>` → `<h2>` → `<h3>` (no skipped levels)
- **Common issue**: Multiple `<h1>` tags (e.g., one for the page title, one for a section header)
- **Fix**: Use a heading component with a `headingLevel` prop to control heading levels, or manually
  enforce one `<h1>` per page

### 7. Sitemap & Robots.txt with AI Crawler List

**Why it matters**: Sitemaps help search engines discover all your pages. Robots.txt controls
crawler access, and AI crawlers need explicit allow rules to index your content.

- Check `@astrojs/sitemap` is installed and added to `astro.config.mjs` integrations
- Verify `sitemap-index.xml` is referenced in `public/robots.txt` via
  `Sitemap: https://<your-site>/sitemap-index.xml`
- Check `robots.txt` includes allow rules for AI crawlers (see
  `references/robots-template.txt` for the full list)
- **Common issue**: Missing AI crawlers in `robots.txt`
- **Fix**: Install `@astrojs/sitemap`, configure it in `astro.config.mjs`, and update `robots.txt`
  with the crawler list from the reference file

### 8. Astro `<Image>` for `src/assets/`, Proper Alt Text

**Why it matters**: Astro's `<Image>` component optimizes images (WebP conversion, srcset, lazy
loading) to improve Core Web Vitals (LCP, CLS, INP). Alt text improves accessibility and SEO.

- Check all images imported from `src/assets/` use the `<Image>` component from `astro:assets`
- Verify every image has descriptive `alt` text (under 125 characters, no "image of" prefixes, empty
  `alt=""` for decorative images)
- Check images in `public/` are only used for static assets that do not need optimization
- **Common issue**: Missing `alt` text or using raw `<img>` tags for `src/assets/` images
- **Fix**: Replace raw `<img>` tags with `<Image>`, add descriptive alt text

### 9. First Paragraph as Definition/Outcome

**Why it matters**: Google's featured snippets and AI Overviews often pull the first paragraph as a
direct answer to user queries.

- Check blog posts answering specific questions have a 1-2 sentence definition/outcome in the first
  paragraph
- Avoid generic opening lines like "Hey everyone, I've been thinking..."
- **Common issue**: First paragraph is a personal anecdote instead of a definition
- **Fix**: Rewrite the first paragraph to directly answer the post's core question or state the
  outcome

### 10. Internal Linking with Descriptive Anchor Text

**Why it matters**: Search engines use anchor text (the visible text in links) to understand what a
page is about. Descriptive anchor text improves topical authority.

- Check internal links use descriptive text (e.g., "10 React patterns") instead of "click here" or
  "read more"
- Verify posts in the same series link to each other inline, not just in a related posts footer
- Link to authoritative external sources (Wikipedia, docs, .gov/.edu sites) where relevant
- **Common issue**: Generic anchor text like "click here"
- **Fix**: Update link text to describe the linked page's content

### 11. BreadcrumbList Schema

**Why it matters**: BreadcrumbList schema replaces the URL in Google SERPs with a clickable
breadcrumb hierarchy, increasing CTR.

- Check for `BreadcrumbList` JSON-LD in page heads
- Verify the breadcrumb matches the site's visible breadcrumb UI (if present)
- **Common issue**: Missing `item` property for the current page (last item in the list should not
  have an `item` URL)
- **Fix**: Generate BreadcrumbList JSON-LD from the page's URL path, inject via
  `<Fragment slot="head">`

### 12. URL Structure & 301 Redirects for Slug Changes

**Why it matters**: Short, descriptive URLs are easier to share and remember, and 301 redirects
preserve ranking equity when slugs change.

- Check URLs are kebab-case, lowercase, no underscores, no `.html` extensions
- Verify 301 redirects are set up for old slugs (using `public/_redirects` for Netlify or
  `redirects` in `astro.config.mjs`)
- **Common issue**: Old slugs return 404 instead of 301 redirects
- **Fix**: Add redirect rules for all changed slugs to preserve backlink equity

### 13. llms.txt & Build-Time llms-full.txt

**Why it matters**: `llms.txt` is the standard for AI models to understand your site's content.
`llms-full.txt` provides all content in a single fetch for AI retrieval.

- Check `llms.txt` exists at the site root with a brief site description, blog/podcast links, and
  RSS feed
- Verify `llms-full.txt` is generated at build time (via a `src/pages/llms-full.txt.ts` route) with
  all blog content concatenated
- **Common issue**: Missing `llms.txt` or `llms-full.txt`
- **Fix**: Create `llms.txt` manually, add a build-time route for `llms-full.txt` that fetches all
  content and returns plain text

### 14. Pagefind for Site Search

**Why it matters**: On-site search helps users find old content, increasing site stickiness (a
ranking signal). Pagefind is a lightweight, build-time search tool for static sites.

- Check Pagefind is installed (`npm install --save-dev pagefind`) and
  `postbuild: "pagefind --site dist"` is added to `package.json`
- Verify content is marked with `data-pagefind-body` and filters (type, category, tags) are added
  via `<meta data-pagefind-filter>`
- Check a `/search` page exists with the Pagefind UI loaded via `import('/pagefind/pagefind-ui.js')`
  (use `is:inline` on the script tag)
- **Common issue**: Forgetting `is:inline` on the Pagefind script tag, causing build errors
- **Fix**: Follow the Pagefind quickstart in `references/schema-examples.json` (or the original
  article)

### 15. HowTo Schema for Tutorial Posts

**Why it matters**: HowTo schema enables step-by-step rich results in Google for tutorial-style
posts (minimum 3 steps required).

- Check tutorial posts include `HowTo` JSON-LD with `name`, `totalTime`, and an array of `HowToStep`
  items
- Verify the post has at least 3 steps to be eligible for rich results
- **Common issue**: HowTo schema with fewer than 3 steps
- **Fix**: Add HowTo schema to all tutorial posts with 3+ sequential steps

### 16. Speakable JSON-LD on Article Schema

**Why it matters**: Speakable specifies which parts of a page voice assistants (Google Assistant,
Alexa) should read aloud.

- Check Article JSON-LD includes a `speakable` property with `@type: SpeakableSpecification` and
  `cssSelector` (e.g., `['h1', '[data-speakable]']`)
- **Common issue**: Missing speakable property
- **Fix**: Add the speakable property to your existing Article schema helper

### 17. Content Collection Schemas

**Why it matters**: Content collection schemas (using Zod) validate frontmatter, catching broken
URLs, missing fields, and formatting issues that hurt SEO.

- Check `src/content/config.ts` defines Zod schemas for all content collections (blog, podcast,
  etc.)
- Verify a Vitest test exists to validate all content files against the schema (see
  `scripts/content-schema-check.js` for a reference)
- **Common issue**: No schema validation, leading to broken frontmatter (e.g., URLs wrapped in
  markdown links)
- **Fix**: Define Zod schemas for all collections, write a validation test

### 18. dateModified Shown to Readers When Distinct

**Why it matters**: Freshness is a ranking signal. Showing `dateModified` when it differs from
`datePublished` builds reader trust.

- Check `dateModified` is included in Article JSON-LD
- Verify the page displays `dateModified` visually only when it differs from `datePublished`
- **Common issue**: Showing `dateModified` even when it is the same as `datePublished` (adds noise)
- **Fix**: Add a conditional check to render `dateModified` only when dates differ

### 19. rel="prev"/rel="next" & Noindex on Pagination

**Why it matters**: `rel=prev/next` helps Bing and other engines understand paginated content.
Noindex on paginated pages (2+) prevents them from competing with the main blog index.

- Check paginated pages include `<link rel="prev">` and `<link rel="next">` in the head (if
  applicable)
- Verify page 2+ of pagination are noindexed (via `robots: { index: false }` in metadata)
- **Common issue**: Indexed pagination pages splitting ranking signals
- **Fix**: Add prev/next links and noindex rules to your pagination layout

### 20. Noindex the 404 Page

**Why it matters**: 404 pages that are indexed create a bad user experience and waste crawl budget.

- Check the 404 page includes `robots: { index: false, follow: false }` in its metadata
- Verify no soft 404s (pages returning HTTP 200 but with empty content) exist
- **Common issue**: 404 page is indexed in search results
- **Fix**: Add noindex metadata to the 404 page layout

## Report Format

After completing the audit, generate a markdown report with the following structure:

```markdown
# Astro SEO Audit Report

## Summary

- Total tactics checked: 20
- Passed: X
- Failed: Y
- High priority fixes: Z

## Detailed Results

For each tactic (1-20):

### [Tactic Number] [Tactic Name]

- Status: Pass/Fail
- Issue (if failed): [Description]
- Recommendation: [Fix steps]

## Priority Action Items

List failed tactics in order of impact (highest first), with concrete fix steps.
```

## Bundled Resources

Refer to these files included with this skill for reference:

- `references/robots-template.txt`: Complete `robots.txt` template with sitemap reference and AI
  crawler rules
- `references/schema-examples.json`: Copy-paste JSON-LD snippets for all schema types (Article,
  Person, BreadcrumbList, HowTo, SearchAction)
