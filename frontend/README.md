## Reason Net – Multi‑Agent Fake‑News Detection (Frontend Focus)

An interactive dashboard for explainable fake‑news detection. This repository currently focuses on the frontend experience (routing, UI states, and visualizations) with a ready-to-connect backend.

### Problem Statement (in short)

- Build a web platform that accepts news via text, URL, or image (OCR) and returns:
  - Verdict: Fake / Real / Uncertain
  - Confidence score with visual representation
  - Key signals/cues influencing the decision
  - External evidence from multiple sources (e.g., X/Twitter, Reddit)
- Present results in an interactive, explainable dashboard with highlights, agent reasoning, and downloadable reports (PDF/JSON).

## High‑Level Workflow

1. User submits content (text, URL, or image for OCR)
2. Backend processes input via multi‑agent pipeline (linguistic, fact‑verification, source/context checks)
3. Platform aggregates agent outputs into a verdict + confidence score
4. UI displays interactive explanations (highlights, cues, agent breakdown)
5. Evidence panel surfaces external corroboration/contradiction
6. User can export a report (PDF/JSON) and explore related news

## App Navigation and Sections

### Landing Page

- Hero, quick stats, key feature cards, CTA to start an analysis.

### About (How It Works + Team)

- Meet the Team (above):
  - Dravvya Jain — Frontend (role, tech bio, GitHub/LinkedIn placeholders)
  - Atharva Deo — Cloud (role, tech bio, GitHub/LinkedIn placeholders)
  - Bhavik Sheth — Backend (role, tech bio, GitHub/LinkedIn placeholders)
  - Akshat Bhalani — AI (role, tech bio, GitHub/LinkedIn placeholders)
- How It Works (below): 7‑step workflow visualization.
- Note: “Data Sources & Credibility Metrics” and “Ethical Use & Transparency Policy” are intentionally excluded for now.

### Dashboard

- Input tabs (Text, URL, Image/OCR)
- Title/body fields with length guidance (target 200–300 words)
- Analyze action → Analysis view → Results

### Results

- Verdict + confidence meter
- Key cues and highlighted text/image
- External evidence panel (social, fact‑checkers, news)
- Agent breakdown and analysis visuals
- Export report (PDF/JSON)

### History & Profile (scaffolded UI)

- History list with verdict/confidence, quick export
- Profile and preferences (UI only)

## Flowchart

flowchart TD

A[🏠 Landing Page] --> B[📰 Input Page]
A --> C[📊 Dashboard Page]
A --> D[ℹ️ About / How It Works]
A --> E[🧠 Model Explainability Page]

B --> B1[✍️ Text Input Form]
B --> B2[🔗 URL Submission]
B --> B3[🖼️ Image Upload (OCR Extraction)]
B --> B4[⚙️ Analyze Button → Routes to Dashboard]

C --> C1[✅ Verdict Display (Fake / Real / Uncertain)]
C --> C2[🧭 Confidence Meter (Speedometer Style)]
C --> C3[📄 Downloadable Report (PDF / JSON)]
C --> C4[🧩 Key Cues & Highlighted Text / Image]
C --> C5[🌐 External Evidence Panel]
C --> C6[📈 Confidence & Analysis Visualization]
C --> C7[🗣️ User Feedback Section]
C --> C8[🔍 Related News Exploration]

E --> E1[🧬 Agent Reasoning Visualization]
E --> E2[🗂️ Feature Importance Heatmap]
E --> E3[🗨️ Reasoning Trail (Agent Logs)]

D --> D1[🎯 Problem Overview]
D --> D2[⚙️ Architecture & Multi-Agent Flow Diagram]
D --> D3[👥 Meet the Team (Above How It Works)]
D --> D4[🛠️ How It Works – 7 Steps (Below Team)]

````

## Tech & Constraints

- Frontend: React + TailwindCSS + Lucide icons
- Routing/State: In‑file state for now; React Router can be added when wiring pages formally
- Charts: Library allowed (e.g., Recharts/ECharts) and should be backend‑connectable
- Exports: PDF and JSON required at MVP (frontend triggers, backend data)
- Limits: article length target 200–300 words; URL fetch timeout 10–20s
- Data retention: Prefer backend with session IDs (Supabase/Firebase if free), else local/browser

## File Map (Where things live)

Repository root

- README.md — This file
- ui/ — Frontend app root
  - src/
    - App.tsx — Entry component that mounts `WebsiteFlow`
    - WebsiteFlow.tsx — All current screens in a single component (navigation bar + pages):
      - LandingPage — hero, stats, features, CTAs
      - FeaturesPage — feature grid and CTA
      - HowItWorksPage — 7‑step process; will also host the Team section above it
      - DashboardPage — inputs (text/url/image), quick stats, recent analyses
      - AnalysisPage — loading/progress simulation view
      - ResultsPage — verdict, confidence, cues, evidence, export controls
      - HistoryPage — list of past analyses, filters, pagination
      - ProfilePage — profile and preferences (UI only)
    - index.css — Tailwind base styles and CSS imports
  - tailwind.config.js — Tailwind configuration
  - postcss.config.js — PostCSS pipeline for Tailwind

Notes:

- For now, all pages are colocated in `ui/src/WebsiteFlow.tsx` for speed of iteration. As the app grows, consider splitting pages into separate files under `ui/src/pages/` and shared components under `ui/src/components/`.

## Local Development

1. Navigate to the UI project

```bash
cd ui
````

2. Install deps

```bash
npm install
```

3. Run dev server

```bash
npm run dev
```

## Backend Integration (when ready)

- Wire frontend actions (analyze, export) to your existing API endpoints
- Persist sessions and feedback via Supabase/Firebase if available; else use local storage
- Ensure CORS and timeouts (10–20s for URL fetch) are configured on the API

## Roadmap (Frontend)

- Add About page section for “Meet the Team” (above) + “How It Works” (below)
- Implement React Router with real routes per page
- Replace placeholders with backend‑driven data
- Add PDF/JSON export and chart visualizations
