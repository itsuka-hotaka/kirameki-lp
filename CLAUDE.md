# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`kirameki-lp` is a one-page Japanese marketing landing page for **KIRAMEKI FARM (煌めきファーム)**, a fruit farm in Takayama Village, Nagano. Built with **Astro 6**, output is a fully static site served at `https://kirameki-farm.pages.dev`. It is a design/animation-driven promo page, not an application — there is no data layer, no API, and no client framework.

## Commands

Requires **Node >= 22.12.0**.

| Command | Action |
| :-- | :-- |
| `npm install` | Install dependencies |
| `npm run dev` | Dev server at `localhost:4321` |
| `npm run build` | Build to `./dist/` |
| `npm run preview` | Preview the production build |

There is **no test suite, linter, or formatter**. `npm run build` is the only check that runs out of the box — treat a clean build as the bar before committing.

Type-checking is *not* preinstalled: `npx astro check` prompts to add `@astrojs/check` and `typescript` on first run. Install them explicitly (`npm i -D @astrojs/check typescript`) if you want to type-check `.astro` files; `tsconfig.json` extends `astro/tsconfigs/strict`.

## Architecture

**One route, one stylesheet, one script.** That is the whole mental model, and each of the three is a single file:

- `src/pages/index.astro` — the only page. It imports the nine section components (`Header`, `Hero`, `Concept`, `Philosophy`, `Marquee`, `Products`, `Village`, `LineCTA`, `Footer`) and renders them in order inside `<Layout>`. All section content is hardcoded Japanese markup in the components; components take no props and have no frontmatter.
- `src/styles/global.css` (~1700 lines) — every style on the site. There are no scoped `<style>` blocks in any component. Organized as 22 numbered sections with a comment banner each (1. Custom Properties → 22. Selection); sections 4–13 map one-to-one onto the section components, so find the banner for the component you're editing rather than searching by selector.
- The inline `<script>` at the bottom of `index.astro` — **all** interactivity: the hero load sequence, `IntersectionObserver` scroll reveals, header show/hide, hamburger toggle, smooth-scroll anchors, and a jQuery hero parallax. No component ships its own JS.

**Layout and the anti-FOUC gate.** `src/layouts/Layout.astro` owns `<head>` (SEO/OGP/Twitter meta, Google Fonts, favicons), pulls in **jQuery 3.7.1 from CDN**, `@import`s `global.css`, and wraps `<slot />` in `#l-wrapper`. The wrapper is inlined as `visibility:hidden; opacity:0` and revealed by adding `.is-loaded` — done twice, once in `Layout.astro` on `DOMContentLoaded` and again in `index.astro` on `load`. Anything that hides the page on error will look like a blank white screen, so check this path first if the site renders empty.

**The animation system is class-driven.** Add a hook class to an element and it opts into a reveal; the CSS pairs each hook with an `.is-visible` end state (section 14 of `global.css`).

- `js-fade-up`, `js-scale-in` — the only two the `IntersectionObserver` actually watches. These are what you want in almost every case.
- `js-blur-in` — reveals on page load, but the load handler queries `.p-hero .js-blur-in` specifically, so it **only works inside the hero**. Elsewhere the element stays invisible forever.
- `js-slide-left`, `js-slide-right` — styled in CSS but **observed by nothing**; an element using them never becomes visible. Either extend the observer's selector list or use a different hook.
- `js-delay-1` … `js-delay-6` — stagger helpers (`transition-delay`, `!important`). `Hero.astro` predates these and uses inline `style="transition-delay"` instead; prefer the classes for new work.

**Class naming (FLOCSS-style) must be preserved.** `l-` layout (`l-header`, `l-footer`, `l-wrapper`) · `p-` section-specific, BEM-style (`p-hero__bg-img`, `p-concept__item--reverse`) · `c-` reusable components (none exist yet) · `u-` utilities (`u-section` is the 85%/max-940px content container used by every section, plus `u-vertical`, `u-en`, `u-serif`, `u-sr-only`) · `js-` animation hooks · `is-` state (`is-visible`, `is-loaded`, `is-active`, `is-scrolled`, `is-menuopen`).

**Adding a section** means: create the component, import and slot it into `index.astro`, add a numbered banner + styles to `global.css`, give the `<section>` an `id`, and add that anchor to **both** navs — `Header.astro` and `Footer.astro` each hardcode the list (`#hero #concept #philosophy #products #village #cta`).

**Responsive work happens in three places at the end of the stylesheet**, not next to the component rules: sections 16–18 are `max-width` 1200px / 768px / 480px blocks that restate selectors from earlier sections. A layout change usually needs edits in the base section *and* the breakpoint blocks. Section 19 holds `prefers-reduced-motion` and print overrides — keep new animations covered by the reduced-motion block.

## Dependencies worth knowing

Three `package.json` entries are not what they appear:

- **`@astrojs/cloudflare`** is installed but **not registered as an adapter** in `astro.config.mjs`. The build reports `output: "static"` and emits plain HTML. Do not assume SSR, middleware, or Cloudflare runtime APIs are available; wiring the adapter is a deliberate change, not a given.
- **`gsap`** is a dependency but is **imported nowhere**. Animations are CSS transitions + `IntersectionObserver` + jQuery.
- **`jquery`** as an npm package is unused at runtime — jQuery arrives via the CDN `<script>` in `Layout.astro` and is read off `window` (`(window as any).jQuery`). The npm entry matters only for `@types/jquery`.

## Assets

Images live in `public/images/` and are referenced root-relative (`/images/…`). Every image is currently an **SVG placeholder**, not real photography.

- `scripts/create-placeholders.sh` regenerates those placeholders. It contains a **hard-coded absolute `IMAGES_DIR`** pointing at another machine — fix that line before running it anywhere else.
- `scripts/generate-images.py` produces real imagery via Google Gemini / Imagen 3. Needs `GEMINI_API_KEY` and `pip install google-generativeai Pillow`.

`Layout.astro` references `/og-image.jpg` and `/apple-touch-icon.png`, neither of which exists in `public/` yet.

## Content conventions

- All copy, `alt` text, headings, and meta descriptions are Japanese — keep them that way.
- Page title/description are defaults in `Layout.astro`'s `Props`; override per-page by passing props, not by editing the layout.
- Known copy inconsistency: the meta description says 標高**600m** while `Concept.astro` and `Village.astro` both say 標高**700m**. Confirm the real figure with the user before "fixing" either side.
- The LINE CTA button in `LineCTA.astro` is still `href="#"` — a placeholder awaiting the real LINE friend-add URL.
- New interactive behavior should follow the existing pattern: add a `js-`/`is-` class and wire it into the single inline script in `index.astro`, rather than introducing per-component scripts or a client framework.
