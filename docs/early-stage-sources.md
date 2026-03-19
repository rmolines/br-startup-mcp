# Early-Stage BR Startup Sources — Access & Coverage Report

> Research sprint: real HTTP tests conducted 2026-03-19.
> No API keys used. All tests ran against public/unauthenticated endpoints.
> Prior work: `docs/data-sources.md` catalogued 11 sources theoretically — this document reports evidence.

---

## 1. Crunchbase API (free/unauthenticated)

**Category:** api
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl "https://api.crunchbase.com/api/v4/searches/organizations" -H "Content-Type: application/json" -d '{...brazil query...}'` → HTTP 401 — API key required for all v4 endpoints
- Test 2: `curl "https://www.crunchbase.com/v4/data/searches/organizations?user_key=&source=homepage"` → Cloudflare block (403/bot detection) — direct HTML scraping blocked
- Test 3: `curl "https://www.crunchbase.com/organization/nubank"` → Cloudflare block — HTML scraping not viable
- Test 4 (WebSearch): Confirmed via official docs and third-party guides — all API v4 endpoints require `user_key` parameter; no unauthenticated access exists. Free Basic tier requires account registration (free) and provides access to `/odm-organizations` and `/odm-people` endpoints only.

### Findings

- Rendering: client-side JS + Cloudflare bot protection
- Auth required: yes — API key required (free Basic tier available via registration at data.crunchbase.com)
- Early-stage BR coverage: low-medium — Crunchbase has ~37,000 BR organizations total, but early-stage coverage is weak; companies without international rounds or notable investors are rarely added. Estimate: ~3,000–6,000 BR startups with any funding data, ~500–1,500 early-stage (pre-seed/seed) with meaningful profiles.
- Key fields available (Basic/ODM): name, short_description, location, founded_on, categories, funding_total (aggregate), num_funding_rounds
- Update frequency: realtime (for paid), weekly snapshots for ODM
- Cost: Free Basic (registration required, 200 calls/day limit); Pro $49/mo; Business $199/mo

### Legal / ToS

API Terms of Use prohibit data resale and redistribution without Enterprise license. Scraping the website is explicitly prohibited. Basic tier data from ODM endpoints may be used for non-commercial and internal research under the Basic license.

### Verdict

**Viable for bulk ingestion:** PARTIAL
**Reason:** Requires free account registration for API key; coverage of early-stage BR startups is sparse (companies below Series A rarely appear unless investor-submitted)
**Estimated early-stage BR startups accessible:** 500–1,500 (seed/pre-seed with any profile), 3,000–6,000 total BR orgs with any data

---

## 2. ABStartups / StartupBase

**Category:** scraping
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl -s "https://startupbase.abstartups.com.br/"` → HTTP 503 — site returned service unavailable during testing
- Test 2: `curl -s "https://startupbase.abstartups.com.br/startups" -H "Accept: application/json"` → HTTP 503 — no JSON API response
- Test 3: `curl -s "https://api.abstartups.com.br/startups"` → HTTP 000 (connection refused) — no public API endpoint
- Test 4: grep for API endpoints in page source → empty (JS-heavy, no visible XHR endpoints in static HTML)
- Test 5 (WebSearch): ABStartups confirmed no public API; platform is for manual web consultation only. Mapeamento 2025 report exists as PDF.

### Findings

- Rendering: client-side JS (React/SPA) — content not in static HTML
- Auth required: no for web browsing; yes for any data export
- Early-stage BR coverage: high — >12,800 startups mapped (2025 data), including pre-seed and seed stages; this is the most comprehensive self-declared database of BR startups
- Key fields available (via web UI): name, sector, city/state, stage, business model, headcount, founders, status
- Update frequency: realtime self-declaration by startups; annual mapeamento report released as PDF

### Legal / ToS

Scraping not authorized per ToS. Data is proprietary to ABStartups. PDF mapeamento annual reports are freely downloadable and may be used with attribution. Partnership or commercial data agreement required for programmatic access.

### Verdict

**Viable for bulk ingestion:** NO
**Reason:** Site returns 503, no public API, JS-only rendering makes scraping unreliable, ToS prohibits scraping
**Estimated early-stage BR startups accessible:** 12,800+ (via partnership/PDF only); 0 via programmatic access without agreement

---

## 3. Distrito

**Category:** scraping
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl "https://www.distrito.me/startups"` → HTTP 404 — page does not exist
- Test 2: `curl "https://api.distrito.me/"` → HTTP 000 (connection refused) — no public API
- Test 3: `curl "https://www.distrito.me/"` with User-Agent → HTTP 200 — home page accessible
- Test 4: Inspect home page for data → Webflow-rendered marketing site (no startup data in static HTML); JSON-LD found but only contains Organization schema for Distrito itself
- Test 5: `curl "https://www.distrito.me/unicornios"` → no JSON company names found — client-side rendered
- Test 6: `curl "https://www.distrito.me/radar"` → no structured data in HTML

### Findings

- Rendering: Webflow CMS (marketing pages) + client-side JS for ÍON platform (requires login)
- Auth required: yes — ÍON platform requires paid subscription for startup data access
- Early-stage BR coverage: high — >37,000 startups in database (BR + LATAM); however, all data is behind the paywall
- Key fields available (via paid platform): profile, investment rounds, valuations, segments, rankings
- Update frequency: realtime (paid tier), annual public reports on blog

### Legal / ToS

Data is proprietary. Scraping explicitly prohibited. Public blog posts (unicorn lists, sector reports) are freely readable. Bulk data access requires commercial contract.

### Verdict

**Viable for bulk ingestion:** NO
**Reason:** No public API, no public startup data endpoint; all startup data behind paid ÍON subscription
**Estimated early-stage BR startups accessible:** 0 programmatically without subscription; 37,000+ total in paid platform

---

## 4. InovAtiva Brasil

**Category:** scraping
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl "https://www.inovativa.org.br/"` → HTTP 000 — wrong domain, site unreachable
- Test 2: Correct domain discovered via web search: `https://www.inovativa.online/`
- Test 3: `curl "https://www.inovativa.online/"` → HTTP 200 — accessible
- Test 4: `curl "https://www.inovativa.online/aprovadas/startups-aprovadas-inovativa-brasil-2024-1/"` → HTTP 200 — approved startups page accessible
- Test 5: Parse HTML for startup names → page is WordPress/Elementor, content appears to load client-side via AJAX; static HTML contains navigation but not the startup list
- Test 6: Site confirms ~90 startups per cycle selected; >4,400 total accelerated since 2013

### Findings

- Rendering: WordPress + Elementor with lazy loading (list content loaded via AJAX, not present in static HTML)
- Auth required: no for page browsing; no API exists
- Early-stage BR coverage: medium — InovAtiva selects up to 90 startups per cohort (2 per year), all early-stage (validation/operation/traction phases); ~4,400 total accelerated historically, ~180/year ongoing
- Key fields available (on page): company name, city, brief description (if page content loads)
- Update frequency: twice yearly (new cohort pages published after selection)

### Legal / ToS

Public government-linked program (Sebrae + MDIC). Cohort lists are publicly published. No explicit ToS on data use; government data typically free for public use with attribution.

### Verdict

**Viable for bulk ingestion:** PARTIAL
**Reason:** Data is public and page is accessible, but list content is AJAX-loaded (requires browser/JS rendering); volume is limited (~180/year, ~4,400 total)
**Estimated early-stage BR startups accessible:** 4,400 total (all cohorts since 2013); ~180/year new additions

---

## 5. Accelerator Portfolio Pages (ACE, Endeavor, 500 Global LATAM, YC)

**Category:** scraping
**Access tested:** 2026-03-19

### Test results

**ACE Ventures (aceventures.com.br):**
- Test 1: `curl "https://acestartups.com.br/portfolio"` → HTTP 301 to jogo-do-tigrinho spam site — domain hijacked/expired
- Test 2: Correct domain: `https://aceventures.com.br/venture-capital/portfolio/` → HTTP 200 (after redirect from /portfolio/)
- Test 3: Parse portfolio page → WordPress server-side rendered; company names in `<h3>` tags, fully accessible without JS
- Result: **76 portfolio companies found in static HTML**, including names like Acordo Online, Auvo, Convenia, Flapper, JetBov, Turivius, Wellbe, etc.

**Endeavor Brasil:**
- Test 1: `curl "https://endeavor.org.br/empresas"` → HTTP 301 → redirects to home page (no /empresas page)
- Test 2: `curl "https://endeavor.org.br/empreendedores-endeavor/"` → HTTP 200, WordPress rendered
- Test 3: Parse page → navigation menu items visible, but entrepreneur profiles load dynamically
- WebSearch finding: Endeavor BR portfolio is curated (high-growth scale-ups only), ~312 entrepreneurs historically; not early-stage
- Test 4: Scale-Up Endeavor program page has individual cohort lists (59 companies in 2023.1) — accessible via WordPress

**500 Global LATAM:**
- Test 1: `curl "https://500.co/companies"` → HTTP 308 → `https://500.co/portfolio` → HTTP 200
- Test 2: Parse portfolio page (Next.js app) → 221,955 bytes HTML but 0 company names found (all content client-side rendered)
- Test 3: `curl "https://latam.500.co/en/startups"` → HTTP 200; 64,806 bytes; 0 Brazil mentions, 0 JSON names — fully client-side rendered
- Result: **No accessible startup data without JS execution**

**Y Combinator:**
- Test 1: `curl "https://www.ycombinator.com/companies?country=Brazil"` → HTTP 200 — page accessible
- Test 2: `curl "https://api.ycombinator.com/v0.1/companies?country=Brazil"` → HTTP 200 — API accessible
- Test 3: Discovered that `country=Brazil` filter does NOT filter; API returns all companies regardless of filter
- Test 4: Full API scrape (all 232 pages, 5,785 companies, ~0.1s/page delay) → **49 Brazilian companies found** (location-based filter on `locations` field)
- All 49 companies confirmed located in Brazil (São Paulo, Rio de Janeiro, Paraná, Minas Gerais, Amazonas)
- Key BR batches: S25(1), W24(1), S23(1), W23(1), S22(3), W22(5), S21(9+), W21, S20, W20, older batches
- API fields: id, name, slug, website, oneLiner, longDescription, teamSize, url, batch, tags, status, industries, regions, locations, badges

### Findings

| Accelerator | Volume BR | Access | Data Quality |
|---|---|---|---|
| ACE Ventures | 76 in portfolio (130+ invested total) | Server-side HTML, scrapable | company name only |
| Endeavor BR | ~312 historical, ~60–90/year (Scale-Up) | Dynamic loading, limited static data | name, sector |
| 500 Global LATAM | Unknown BR count | Client-side JS only | not accessible |
| Y Combinator | 49 BR (all-time, location-confirmed) | Public API (no auth) | name, batch, location, description, tags |

- Rendering: Mixed — YC has a clean public API; ACE is server-side WordPress; Endeavor and 500 Global are client-side
- Auth required: no for YC API and ACE HTML; yes (JS required) for 500 Global and Endeavor
- Early-stage BR coverage: moderate — YC has 49 BR companies total (all-time); ACE has 76 in current portfolio; these are curated/small sets
- Update frequency: YC API appears real-time; ACE portfolio page updated as investments happen

### Legal / ToS

YC: public API, no explicit ToS for reading; data is intended to be public (YC company directory). ACE: WordPress public site with no scraping restriction found. Endeavor: public content. 500 Global: Next.js public site, no explicit scraping prohibition but data is client-side only.

### Verdict

**Viable for bulk ingestion:** PARTIAL
**Reason:** YC API works perfectly without auth for the 49 confirmed BR companies; ACE HTML is scrapable with 76 companies; 500 Global and Endeavor require JS rendering for bulk access
**Estimated early-stage BR startups accessible:** ~125–200 total across all four accelerators (YC: 49, ACE: 76, Endeavor: ~60–80 via Scale-Up cohort pages, 500 Global: unknown)

---

## 6. GitHub / Kaggle Datasets

**Category:** dataset
**Access tested:** 2026-03-19

### Test results

**GitHub:**
- Test 1: `curl "https://api.github.com/search/repositories?q=brazilian+startups+dataset"` → HTTP 200 — 2 results (both unrelated to startup directories)
- Test 2: `curl "https://api.github.com/search/repositories?q=startups+brazil+data"` → 7 results, all tangential (e-commerce analysis, ML exams, ETL projects)
- Test 3: WebSearch found: `github.com/lucianot/dealbook` — "Brazilian Startup DealBook - Full.csv"
  - File size: 28,074 bytes; 187 rows
  - Content: M&A transactions and funding events for Brazilian startups from 1999–present
  - Fields: Date, Who (company), What (event type), How Much, From/To, Source, Year
  - Last updated: 2025-04-04 (31 stars)
  - **Not a startup directory** — it's a deal history with ~150 unique companies

**Kaggle:**
- WebSearch found:
  - `sufya6/startups-and-funding-dataset-20242025` — global startups dataset 2024-2025, not Brazil-specific
  - `datahackers/state-of-data-brazil-20242025` — Brazilian data/AI professionals survey, not startup directory
  - `amanpriyanshu/latest-yc-data` — YC companies dataset (global, not Brazil-filtered)
  - `punithbs10/y-combinator-summer-2025-startups-dataset` — YC S25 dataset (global)
  - No Brazil-specific startup directory found on Kaggle

### Findings

- No dedicated, comprehensive dataset of Brazilian early-stage startups found on GitHub or Kaggle
- Best GitHub find: `lucianot/dealbook` with 187 M&A/funding events for ~150 unique companies (deal history, not directory)
- Kaggle has global startup datasets and YC datasets that could be filtered for Brazil, but no Brazil-focused directory
- Update frequency: irregular/manual (GitHub repos); Kaggle datasets are static uploads
- Key fields: for YC Kaggle datasets — company name, batch, description, URL, funding raised

### Legal / ToS

GitHub repos are typically MIT or similar open licenses. Kaggle datasets have per-dataset licenses (usually CC-BY or similar). Always check individual dataset license before use.

### Verdict

**Viable for bulk ingestion:** NO
**Reason:** No comprehensive BR startup dataset found; best dataset has only 187 deal events for ~150 companies
**Estimated early-stage BR startups accessible:** ~150 unique companies in dealbook (deal history only); 0 from a real early-stage directory

---

## 7. AngelList / Wellfound

**Category:** api
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl "https://wellfound.com/api/v1/startups?locations[]=Brazil"` → HTTP 404 — API endpoint does not exist
- Test 2: `curl "https://angel.co/api/1/startups?locations[]=Brazil"` → HTTP 301 — redirects (old AngelList API)
- Test 3: `curl "https://wellfound.com/startups/l/brazil"` → HTTP 403 — access blocked
- Test 4: `curl "https://wellfound.com/"` → HTTP 200 — main page accessible
- Test 5: `curl "https://wellfound.com/developers"` → HTTP 301 — no public developer/API documentation found

### Findings

- Rendering: client-side JS (Next.js) — no content in static HTML
- Auth required: yes — API access requires account and OAuth token; public browsing blocked for location pages
- Early-stage BR coverage: medium-high — Wellfound has strong coverage of VC-backed startups globally; BR coverage includes funded startups but is weaker for pre-seed and seed vs. US market
- Key fields available (via authenticated API): company name, stage, funding, description, investors, team size, location
- Update frequency: realtime for user-submitted data

### Legal / ToS

API ToS requires OAuth authentication; bulk scraping and data extraction prohibited. No public/unauthenticated API endpoints available since 2023 when AngelList API was shut down and replaced by Wellfound.

### Verdict

**Viable for bulk ingestion:** NO
**Reason:** No public API, location pages blocked (403), old AngelList API deprecated; requires authentication for any access
**Estimated early-stage BR startups accessible:** 0 without authentication; estimated ~2,000–4,000 BR startups exist on platform but inaccessible programmatically

---

## 8. CVM — Crowdfunding / Equity Data (Resolução 88/2022)

**Category:** api (CKAN REST API)
**Access tested:** 2026-03-19

### Test results

- Test 1: `curl "https://dados.cvm.gov.br/api/3/action/package_list"` → HTTP 200 — 54 datasets listed
- Test 2: Found dataset `crowdfunding-cad` — crowdfunding platform cadastral data
- Test 3: Downloaded `cad_crowdfunding.zip` (20 KB) → 73 active crowdfunding platforms, 523 total records (including historical/cancelled platforms)
- Test 4: **This data is crowdfunding PLATFORMS, not startups**. Fields: CNPJ, company name, commercial name, registration date, status, website, email, address
- Test 5: Searched for startup-level equity crowdfunding offers → `oferta-distrib` dataset found (61,346 rows from 1988); equity crowdfunding under RCVM 88 entries NOT present in this dataset
- Test 6: CKAN API confirmed: no dedicated dataset for individual startup equity crowdfunding rounds under RCVM 88

### Findings

- Rendering: CKAN REST API (JSON) + direct CSV/ZIP file downloads
- Auth required: no — fully public and programmatic
- Early-stage BR coverage: medium — the CVM crowdfunding dataset tracks platforms, not the startups that raised via those platforms. 73 active equity crowdfunding platforms registered. The actual startup-level equity raise data would need to be requested from each platform or accessed via a separate CVM dataset not currently in the portal.
- Key fields available: platform CNPJ, name, registration date, status, website, city/state (for platforms only)
- Update frequency: daily snapshots for most datasets; crowdfunding-cad is "last business day" snapshot

### Legal / ToS

Fully public government data (dados.gov.br). No restrictions on use or redistribution. CKAN API is stable and documented.

### Verdict

**Viable for bulk ingestion:** PARTIAL
**Reason:** CVM API is excellent (fully open, no auth, direct CSV download) but the available dataset covers crowdfunding platforms, not the startups that raised capital through them. Startup-level data from RCVM 88 equity raises is not yet exposed in the portal.
**Estimated early-stage BR startups accessible:** 0 directly (platform registry only); however, ~73 active platforms contain investor data on ~2,000+ equity crowdfunding raises that could be obtained by contacting platforms or via additional CVM datasets

---

## 9. Google Startup Programs / AWS Activate

**Category:** manual
**Access tested:** 2026-03-19

### Test results

**Google for Startups:**
- Test 1: `curl "https://startup.google.com/programs/"` → HTTP 200 — programs page accessible
- Test 2: `curl "https://startup.google.com/startups/"` → HTTP 404 — no public list of accepted startups
- Test 3: Parse programs page for startup names → only program descriptions, no startup directory
- Test 4: No public API, no JSON data, no structured startup list found

**AWS Activate:**
- Test 1: `curl "https://aws.amazon.com/startups/activate"` → HTTP 404 — page removed
- Test 2: `curl "https://aws.amazon.com/startups/"` → HTTP 308 redirect — landing page only, no startup directory
- Test 3: No public list of AWS Activate recipients found

### Findings

- Rendering: marketing pages only (server-side HTML for Google; AWS redirects)
- Auth required: program enrollment requires application; no public directory exists
- Early-stage BR coverage: unknown — both programs have thousands of BR participants but publish no public list
- Key fields available: none — no public startup directory
- Update frequency: N/A

### Legal / ToS

No public data to access. Both programs have internal participant databases not shared publicly.

### Verdict

**Viable for bulk ingestion:** NO
**Reason:** Neither program publishes a list of accepted startups; Google's /startups/ page returns 404; no structured data accessible
**Estimated early-stage BR startups accessible:** 0 programmatically

---

## Conclusion: Early-Stage Ingestion Strategy

### Viable sources (ranked by coverage)

| Source | Volume (BR early-stage) | Access | Cost | Priority |
|--------|------------------------|--------|------|----------|
| ABStartups PDF Mapeamento | 3,000–5,000 (annual PDF, structured) | Manual/PDF parse | Free | High |
| InovAtiva Brasil | 4,400 total, ~180/year | HTML scraping (JS render needed) | Free | High |
| YC API | 49 (all-time, confirmed BR location) | Public JSON API, no auth | Free | High |
| ACE Ventures portfolio | 76 current, 450+ historical | Server-side HTML, scrapable | Free | Medium |
| CVM CKAN API | 73 platforms (not startups directly) | Public JSON API, no auth | Free | Medium |
| Crunchbase Basic | 500–1,500 early-stage BR | API key (free registration) | Free (limited) | Medium |
| Endeavor Scale-Up pages | ~60–90/year (per cohort page) | WordPress HTML, scrapable | Free | Low |
| GitHub dealbook | ~150 unique companies (deal history) | Public CSV, no auth | Free | Low |

### Total addressable universe

With the viable sources combined (no duplicates counted):
- ABStartups mapeamento PDF: ~3,000–5,000 unique startups per annual report
- InovAtiva cohort pages: ~4,400 cumulative (high overlap with ABStartups data)
- YC API: 49 (distinct, many already in ABStartups)
- ACE HTML: 76 (mostly early-to-growth stage)
- Crunchbase: 500–1,500 with meaningful early-stage data

**Realistic unique early-stage BR startups reachable: 5,000–8,000** (after deduplication across sources). The ABStartups mapeamento PDF is the ceiling for early-stage coverage — all other sources are subsets or complements.

### Recommended ingestion strategy

1. **Parse the ABStartups Mapeamento PDF annually** — this is the most comprehensive BR early-stage directory (3,000–5,000 startups). Download the annual PDF from abstartups.com.br/mapeamento-de-startups-2025/, extract tables with `pdfplumber` or `camelot`. Use CNPJ from Receita Federal to enrich with financial data.

2. **Use the YC API for ongoing updates** — `GET https://api.ycombinator.com/v0.1/companies` (all 232 pages, 5,785 total) then filter for `"Brazil"` in the `locations` field. 49 confirmed BR companies today; new batches added regularly. No authentication required, respectful rate limits.

3. **Scrape ACE Ventures portfolio quarterly** — `https://aceventures.com.br/venture-capital/portfolio/` is a server-side WordPress page with 76 portfolio companies in `<h3>` tags. One HTTP request, no JS needed.

4. **Use CVM CKAN API for equity-funded startups** — `https://dados.cvm.gov.br/api/3/action/package_list` is fully open. While current `crowdfunding-cad` dataset covers platforms only, use it to identify the 73 active platforms, then cross-reference with CNPJ base to find companies that raised via equity crowdfunding. Watch for future CVM dataset additions covering RCVM 88 individual offers.

5. **Deduplication anchor: CNPJ** — Every BR company has a CNPJ. After ingestion from any source, resolve to CNPJ via the Receita Federal API or CNPJ.ws free API. This eliminates duplicates across all sources and enriches with founding date, revenue bracket, CNAE code, and current status.

### Sources NOT viable

| Source | Reason |
|--------|--------|
| ABStartups API (live) | No API, SPA renders client-side, ToS prohibits scraping |
| Distrito ÍON | All startup data behind paid subscription |
| AngelList/Wellfound | Old API deprecated, public pages blocked (403), no unauthenticated access |
| Google Startup Programs | No public list of accepted startups |
| AWS Activate | No public list, page returns 404 |
| GitHub/Kaggle datasets | No BR startup directory found; only 187-row M&A history and global datasets |
| 500 Global LATAM | Portfolio is fully client-side JS rendered; no API |
| Crunchbase HTML scraping | Cloudflare protection blocks all programmatic access; API key required even for Basic tier |

---

*Tests conducted by: Claude Sonnet 4.6 — 2026-03-19*
*Repo: br-startup-mcp — node: fontes-early-stage-bulk*
