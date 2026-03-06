# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Six independent projects (not a monorepo) sharing a common AWS account and S3/CloudFront hosting stack. `data-bot` feeds all Gatsby sites; `scripts` is an unstructured staging sandbox.

| Project | Domain | Stack | Priority |
|---------|--------|-------|----------|
| `alphagaldata` | alphagaldata.com | Gatsby 5, React 18, TS, TailwindCSS | PRIMARY |
| `data-bot` | — | Python 3.8+ pipelines | 2 |
| `gatsby-investing` | investing.monkcode.com | Gatsby 5, React 18, TailwindCSS | 3 |
| `gatsby` | monkcode.com | Gatsby 5, React 18, Bootstrap, D3 | 4 |
| `climate-gatsby` | climate.monkcode.com | Gatsby 5, React 18, D3 | 5 |
| `scripts` | — | Python + misc | sandbox |

## Data Flow

```
data-bot (GitHub Actions cron)
  ├── datasets/alphagal/ingredients.json  ──→ alphagaldata (build-time sync)
  ├── market/ (dividends, econ_calendar)  ──→ gatsby-investing (build-time fetch)
  └── geojson/                            ──→ gatsby-investing

climate-gatsby/scripts/fetch-data.js (daily GitHub Action) → src/data/metrics/*.json
```

## Commands

### alphagaldata (PRIMARY)
```bash
npm run dev              # Gatsby dev server
npm run build            # Runs prepare:data first (syncs ingredients from data-bot), then builds
npm run typecheck        # TypeScript validation
npm run lint             # ESLint
npm run format           # Prettier
npm run deploy:s3        # Deploy to S3 bucket: alphagal
# Data tasks (build-time):
npm run tasks:generate-cards
npm run tasks:fetch-pubmed
npm run tasks:cdc-ticks
npm run tasks:county-prep
npm run tasks:build-map
```

### gatsby-investing
```bash
npm run develop          # Dev server
npm run build            # Add ENABLE_EXTERNAL_FETCH=1 to pull live Yahoo Finance data
npm run deploy           # S3 sync to investing.monkcode.com
```

### gatsby / climate-gatsby
```bash
npm run develop          # Dev server
npm run build
npm run deploy           # S3 sync
npm run fetch:data       # climate-gatsby only: pulls NOAA/NASA/CU metrics
```

### data-bot
```bash
python main.py                                         # Run all priority feeds
python data-pipelines/alphagal/ingredients_scraper.py  # Alpha-gal scraper only
python data-pipelines/market/market_data.py            # Market data only
```

### Multi-site deployment
```bash
# From collection root:
./deploy_gatsby_sites.sh   # Deploys all 4 Gatsby sites to S3/CloudFront
```

## alphagaldata Architecture

**Auth:** `react-oidc-context` → Cognito OIDC → `/auth` callback page. Cognito variables come from `.env*` files (see `.env.example`). Auth state wraps the app in `gatsby-browser.js`.

**Config files that matter:**
- `gatsby-config.ts` — plugin registration, S3 bucket (`alphagal`), site metadata
- `gatsby-node.js` — GraphQL node creation at build time
- `config/` — Cognito and analytics configuration objects

**Ingredients data:** `npm run prepare:data` copies `../data-bot/datasets/alphagal/ingredients.json` into `src/data/`. This must run before build in fresh environments.

**Mapping:** Leaflet/React Leaflet with TopoJSON for tick surveillance heatmaps.

**CMS:** Decap CMS writes to S3 bucket `alphagal-decapcms`; Cognito handles editor auth.

**Terraform:** `alphagaldata/tf/` manages CloudFront (E2ME15PLS6E69R), ACM, Route53, Cognito. State is local only (gitignored).

## AWS Context

- **Account:** 904524340593 (us-east-1)
- **Cognito pool:** us-east-1_Gj01zboi3 | App client: alphagal-users (6i65tnlfc53c51cpgem8v5fvne)
- **Cognito hosted domain:** us-east-1gj01zboi3.auth.us-east-1.amazoncognito.com
- **S3 buckets:** `alphagal`, `monkcode.com`, `investing.monkcode.com`, `climate.monkcode.com`, `alphagal-decapcms`
- **CloudFront:** E2ME15PLS6E69R (alphagaldata); others per site via CF_DISTRIBUTION_ID env vars

## GitHub Actions

- `data-bot/.github/workflows/alphagal-ingredients.yml` — nightly ingredient scrape, commits if changed
- `data-bot/.github/workflows/market-data.yml` — market pipeline
- `climate-gatsby/.github/workflows/fetch-data.yml` — daily @ 3:00 UTC climate metrics fetch

## Known Issues / Debt

- `scripts/` contains a `creds.txt` with ~2021-era AWS/DB credentials that needs a git history purge and credential rotation before any public exposure
- `data-bot` dependencies are pinned to ~2020 versions; upgrade to Python 3.11+ and refresh `requirements.txt`
- Cognito Identity Pool (`us-east-1:50c9f758-eb27-481e-96da-595b9c7edb18`) is not yet managed in Terraform
- Terraform state is local only — consider an S3 backend
