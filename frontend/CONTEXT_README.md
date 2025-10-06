Reason Net – Working Context (Frontend)

Purpose

- This file captures the current state/decisions so work can be resumed in another IDE/agent without chat history.

Stack

- React + TypeScript (Vite) in `ui-app/`
- TailwindCSS + PostCSS
- Lucide icons
- Recharts (charts)

Project Status (What exists today)

- Landing (static, polished)

  - Navbar with “Reason Net” brand, glass-morphism tabs (static buttons)
  - Fonts: Gabarito (global), Darker Grotesque for a highlighted paragraph
  - Effects: ShinyText for brand/paragraph; CountUp for stats; Live Activity mock
  - DarkVeil background: removed (caused layering issues). Not used anywhere
  - Where to tweak Landing stats: `ui-app/src/pages/Landing.tsx`
    - Initial values: inside `setAnimatedStats([...])`
    - Cards config: array under the grid; suffix/prefix can be changed there

- Dashboard (interactive)
  - Pages file: `ui-app/src/pages/Dashboard.tsx`
  - Layout: Input section at top, then Analytics (metrics, charts), then Results preview placeholders
  - Input section (tabs)
    - Tabs: Text | URL | Image
    - Text: Title input + Body textarea (guidance 200–300 words)
    - URL: Single input with link icon and placeholder “Enter URL for the news here”; note: 10–20s timeout guidance
    - Image: File upload control (hidden input) inside dashed drop zone (PNG/JPG placeholder)
    - Analyze button (static for now)
  - Analytics
    - Metrics cards (static)
    - Detection Trends: stacked Area (Real + Fake)
    - Real vs Fake: Line chart
    - Toggles: range (7d/30d/90d) and view (volume vs ratio)
      - Data generator produces smooth, plausible series on toggle
      - Ratio view converts each point to percentages; tooltip values always sum to 100
      - Tooltip items are sorted by value (largest first) and display Total (100% in ratio)
      - Y-axis domain: auto for volume; 0–100 for ratio
  - Extras: Recent Alerts, Confidence meter (mock), Insights chips, External Evidence (mock), Top Topics tags
  - If Recharts missing:
    - `cd ui-app && npm install recharts && npm run dev`

Decisions and Requirements

- About page (future): single page containing two sections in order: “Meet the Team” (top) and “How It Works” (below)
- Keep both pages in nav (About/How It Works naming accepted), but About hosts both sections
- Charts policy: only Area/Line charts (no pie/radar/treemap/bar)
- Landing/CTA/nav are static (no router yet); routing can be added later
- Report export (PDF/JSON) required later; not implemented yet
- Max article length target: 200–300 words; URL fetch timeout: 10–20s (for future backend wiring)
- Data retention preference: backend with session IDs (Supabase/Firebase) else local/browser (future)

Removed/Deprecated

- DarkVeil.tsx and DarkVeil.css removed from `ui-app/src/components/` and all usages cleaned up

Repo Structure

- `README.md` – general project overview
- `CONTEXT_README.md` – this file
- `ui-app/` – Vite app
  - `index.html` – root HTML
  - `src/main.tsx` – React entry
  - `src/index.css` – Tailwind base, utility classes (e.g., `.glass-tab`, `.font-darker-grotesque`)
  - `src/App.tsx` – BrowserRouter with routes: `/` (Landing), `/dashboard`, `/results`
  - `src/components/Navbar.tsx` – brand + router links (Home/Dashboard/Results); ShinyText used for brand
  - `src/components/ShinyText.tsx` and `.css`
  - `src/components/CountUp.tsx` – animated counters (uses motion)
  - `src/pages/Landing.tsx` – hero, stats (CountUp), live feed, feature cards
  - `src/pages/Dashboard.tsx` – input tabs (Text/URL/Image), Analyze button; metrics; area/line charts; alerts; confidence; insights; evidence; topics
  - `src/pages/Results.tsx` – analytics panels under a Results view; verdict header; Detection Trends + Line Compare with same range/ratio toggles and tooltip rules

Local Dev

1. `cd ui-app`
2. `npm install` (and `npm install recharts` if charts error)
3. `npm run dev` → open the printed localhost URL

Where to Edit Common Things

- Brand text: `ui-app/src/components/Navbar.tsx`
- Landing hero/paragraph: `ui-app/src/pages/Landing.tsx`
- Landing stats values/suffixes: same file; see grid config under “Animated Stats”
- Dashboard data behavior: `generateSeries`, `chartData`, and toggles in `ui-app/src/pages/Dashboard.tsx`
  - To change realism: tweak `generateSeries()` base values and sinusoidal terms
  - Tooltip logic: `CustomTooltip` (keeps order and totals consistent)

Changelog (latest first)

- Routing: Installed `react-router-dom`; added routes in App; updated Navbar to Link-based tabs.
- Results.tsx: new Results page; moved analytics panels; added verdict header; trends/line charts with toggles + tooltip logic.
- App.tsx: renders Dashboard then Results for preview.
- Dashboard.tsx: inputs on top; stateful tab switching; URL input with icon/placeholder; image file input; metrics; charts with 7d/30d/90d + volume/ratio; sorted tooltips with totals; alerts, confidence meter, insights, evidence, topics.

Next Tasks (suggested)

- About page: implement Team (roles, bios, GH/LinkedIn placeholders) above How It Works (7 steps)
- Results page wiring (export PDF/JSON placeholders)
- Optional: React Router for real navigation between pages
- Optional: moving average overlay for trends; uncertain series derived from (100 - real% - fake%) if needed in ratio view

Conventions

- UI only; no backend calls yet
- Keep charts logical:
  - Ratio mode: values per point must sum to 100%; tooltip shows ordered series and total
  - Volume mode: consistent units across series

Contact Points (quick reminders)

- Fonts loaded in `index.html` (Gabarito + Darker Grotesque)
- Glass-morphism tab class: `.glass-tab` in `src/index.css`
