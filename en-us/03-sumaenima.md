# 🚀 Sumænimá — StênioBOT

**Data Capture Platform with Local, Private, Open-Source AI**

[sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net) | [github.com/ceduardorodrig](https://github.com/ceduardorodrig)

<p align="center">
  <img src="../assets/logo-sumaenima.svg" width="400" alt="Sumænimá Logo" />
</p>

---

## 🎯 Overview

**Founder & Product Owner:** Carlos Eduardo Rodrigues

Sumænimá is my life project. It has existed for nearly 10 years as an independent creative entity, running alongside formal employment throughout my entire career. It was born from a conviction: qualitative research — especially with traditional communities, Indigenous peoples, and vulnerable groups — should never depend on big tech infrastructure. But due to lack of funding, it remained a side project for years — until 2024, when I started building **StênioBOT**.

The dream is to raise resources to build a team and create a **Data Bureau** with an anthropological soul: a structure that produces projects like Tô no Mapa, data visualizations, and ethnographic research at scale — uniting science, territory, and technology in a sovereign way.

But the deepest and most valuable layer of Sumænimá is invisible: the **StênioKernel** — a proprietary AI Agent Governance Kernel (21.435 lines, 22 kernel modules, 132 automated check drivers, 10 anti-bypass layers) that governs every AI agent working on the project. It cryptographically enforces absolute laws, self-heals violations, detects bypass attempts, and ensures no agent can escape governance. It is the operating system that makes AI reliable, auditable, and accountable.

**StênioBOT** is an AI-assisted data capture platform running 100% offline on local hardware, with zero data sent to the cloud. Four integrated modules cover the complete qualitative research cycle: from field collection to analysis and visualization.

The entire Sumænimá ecosystem totals **~8M+ lines and growing** — across 1,227+ files, built over 10 years as a life project.

---

## 🖥️ Design & Experience

The StênioBOT interface follows **Material Design 3** with glassmorphism, Lexend typography, and dynamic theming — fully responsive across every device.

| Mobile · iPhone SE | Tablet · iPad Pro | Desktop |
|:---:|:---:|:---:|
| <img src="../assets/hub-mobile.png" width="220" alt="Mobile" /> | <img src="../assets/hub-tablet.png" width="280" alt="Tablet" /> | <img src="../assets/hub-desktop.png" width="400" alt="Desktop" /> |

---

## ❓ The Problem

Researchers, NGOs, and institutions working with sensitive data face a dilemma:
- Cloud services (Google, OpenAI, AWS) are expensive and require sending data to external servers
- Local alternatives are fragmented, poorly documented, and require deep technical expertise
- LGPD, GDPR, and ethics committees increasingly restrict cloud solutions for research data

There is no integrated, local, private, and accessible platform for AI-assisted qualitative research.

---

## 💡 The Solution — StênioBOT

### Modules

#### StênioREC — Real-Time Transcription
<p align="center">
  <img src="../assets/hub-rec.png" width="600" alt="StênioREC" />
</p>

Real-time transcription via Whisper large-v3-turbo with VAD, Gemma 3 Neural Flow purification, collaborative Google Docs export.

#### StênioPANEL — Workshop Scanner
<p align="center">
  <img src="../assets/hub-panel.png" width="600" alt="StênioPANEL" />
</p>

Physical workshop scanner with GroundingDINO + SAM 2 + PaddleOCR, generating Obsidian-compatible `.canvas` schemas.

#### StênioDIVE — Semantic Mining
<p align="center">
  <img src="../assets/hub-dive.png" width="600" alt="StênioDIVE" />
</p>

Cross-semantic mining of wikilinks, tags, and notes in an interactive graph; local embeddings and semantic search.

#### DataVis — Climate Visualizations
<p align="center">
  <img src="../assets/hub-datavis.png" width="600" alt="DataVis" />
</p>

Real-time climate visualizations (PM2.5, energy matrix, floods) with particle physics.

#### Admin — Platform Management
<p align="center">
  <img src="../assets/hub-admin.png" width="600" alt="Admin" />
</p>

Administrative panel with organization, member, contract, and billing management. SaaS with Mercado Pago, OAuth, and integrated CMS.

### Cross-Cutting Features

- SaaS with Mercado Pago subscription billing, Google OAuth with encrypted tokens
- CMS with TipTap WYSIWYG editor and image library
- ERP: organizations, members, leads, contracts, invoices, projects
- Observability: Grafana + Loki + Promtail

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI (async) · Python 3.12+ · SQLAlchemy 2.0 (asyncpg) |
| **Frontend** | React 19 · Vite 8 · TypeScript 6 · Material Web Components (MD3) · Tailwind |
| **Database** | PostgreSQL 16 · Alembic (migrations) |
| **Cache/Queue** | Valkey 8 (Redis-compatible) · Streams, Pub/Sub, arq job queues |
| **AI Audio** | Whisper large-v3-turbo (transformers/PyTorch) · Gemma 3 (1B) |
| **AI Vision** | GroundingDINO · SAM 2 · PaddleOCR · Gemma 4B |
| **Infra** | Docker Swarm multi-node · Docker Compose · NVIDIA GPU (RTX 5050) |
| **Network** | Tailscale Funnel · Nginx reverse proxy |
| **Payments** | Mercado Pago SDK |
| **Analytics** | Umami (self-hosted, privacy-first) |
| **Governance** | StênioKernel (21.435 lines, 132 drivers, 22 kernel modules) |
| **Monitoring** | Grafana · Loki · Promtail |
| **Ecosystem** | **~8M+ lines and growing** · 1,227+ files · 10 years |

---

## 🏗️ StênioKernel — AI Agent Governance Kernel

This is Sumænimá's deepest and most valuable asset. The StênioKernel is not a QA framework — it is a **proprietary AI Agent Governance Kernel** (purpose-built, not forked from any open-source project) designed to govern AI agents across the entire software lifecycle: code, documentation, infrastructure, and agent behavior itself.

- **22 kernel modules** (scheduler, guardian, healer, docbot, learner, registry, self-test, history, flakiness, classifier, impact, more)
- **132 check drivers** (governance, security, frontend, infrastructure, documentation, backend, data, GPU, API, CMS)
- **21.435 lines** of Python, zero external QA framework dependencies
- **Plugin architecture**: auto-discovery via `CHECK_METADATA` in each driver, ThreadPoolExecutor + asyncio scheduler

### 🛡️ Anti-Bypass Architecture (10 Layers)

| Layer | Mechanism | What It Prevents |
|-------|-----------|------------------|
| 1. **Pre-Commit Hooks** | `pre-commit-config.yaml` — gates P0+sec+doc | Commit without static checks |
| 2. **Bypass Guard** | `sec_ai_bypass_guard` — P0 driver | `--no-verify`, `\|\| true`, `2>/dev/null`, CI `continue-on-error` |
| 3. **No-Bypass Ops** | `sec_no_bypass` — P0 driver | Manual `rsync+ssh`, `docker compose`, `npm run build`, `pg_dump` |
| 4. **Scope Guard** | `sec_scope_guard` — P0 driver | Partial runs that hide failures (`--only`, `--tag`, `--scope`) |
| 5. **Kernel Immutability** | SHA256 hashes of critical files | Agents modifying the kernel itself |
| 6. **Agent Laws Integrity** | SHA256 hash of AGENTS.md Laws | Agents altering or removing rules |
| 7. **Knowledge Protocol** | Mandatory handoff inheritance | Agents ignoring context from previous sessions |
| 8. **Repetition → Rule** | Promotes repeated instructions | Recurring instructions staying ad-hoc |
| 9. **A Teia (The Web)** | `pm_omniscience` — universal jurisdiction | Any file escaping governance |
| 10. **Warning Promotion** | `__main__.py` promotes P0/sec WARN→FAIL | Agents dismissing critical warnings |
| + **Re-Signing Blockade** | TTY+API-key detection | Automated agents re-signing security baselines |

### 🔧 Self-Healing

The Healer doesn't just report violations — it autonomously fixes them:
1. Extracts `filepath:line` from violation strings
2. Queries the **Knowledge Graph** (docs/external + registry + git log) for candidate fixes
3. Checks the **Negative Registry** (`.steniocheck-negative-registry.json`) to skip previously failed attempts
4. Applies the fix with line-level precision
5. Re-executes the check in real context to verify
6. On pass: `git add + git commit` automatically, adds to permanent registry
7. On fail: reverts, records failure in negative registry, tries next candidate

### 📊 Predictive Governance

The kernel doesn't just report current failures — it predicts future ones:
- **Trend detection**: linear regression on violation counts over the last 10 runs
- **Auto-suppress**: suppresses warnings persisting for N consecutive runs (adaptive threshold)
- **Baseline comparison**: `.steniocheck-baseline.json` for noise reduction
- **Flakiness detection**: identifies checks that oscillate between pass/fail
- **Canary promotion**: auto-promotes drivers with >80% pass rate over 5+ runs

### 🧠 Memory & Learning

- **History persistence** (`.steniocheck-history.json`): caches results, tracks file hashes, records durations
- **Continuous learning**: `--learn`, `--learn --interactive`, `--learn-auto` (auto-detects corrections from `git diff`)
- **Registry**: curated bug patterns with `id`, `title`, `pattern`, `fix`, `auto_fix_commands`
- **Proactive suggestions**: `--suggest <fingerprint>` queries registry for known solutions
- **Knowledge Graph**: indexes `docs/external/` (MD3, Tailwind, MWC, FastAPI), registry patterns, and git history for similarity-based correction

### 📚 Documentation as a Product

- **185 documentation files**, **~74,000 lines**
- **DocBot**: auto-downloads READMEs from GitHub/GitLab, archives unused docs, reindexes Knowledge Graph

### 🔄 Resilience

- **Living FMEA**: documented failure nodes with real-time logging and LLM auditing
- **Audio WAL**: Write-Ahead Log with AES-GCM 256 encryption + IndexedDB, 3-layer failure detection, silent network resilience
- **Adaptive circuit breaker** via Valkey for Google Docs, Mercado Pago, OAuth, and Umami
- **Neural Flow**: dual-stage Whisper (sub-500ms draft) + Gemma (refinement) with zero-tolerance hallucination policy
- **Cross-worker handoff**: session state persisted in Valkey with 8h TTL, any worker can restore context

### 🔍 Self-Diagnosis

The kernel audits itself:
- `--blame`: traces every violation to the specific commit, author, and date via `git blame`
- `--self-test`: self-tests validating driver imports, registry format, Knowledge Graph, healer, history cycle
- `--guardian`: self-audit that detects hash drift, registry gaps, suspicious violation drops, canary candidates, performance degradation, timeout anomalies
- `.steniocheck-driver-hashes.json`: cryptographically seals every driver file against unauthorized modification

---

## 🖥️ Infrastructure — Mnemocine Homelab

The **Mnemocine Homelab** is the **Sumænimá** infrastructure. They are indistinguishable — proof of concept running on real hardware with zero commercial cloud dependency for sensitive data.

| Node | Hardware | Role |
|------|----------|------|
| **psicopompo** 🧠 | Dell Frankenstein · Xeon E-2246G 6C/12T · RTX 5050 · 46GB RAM · CachyOS (Arch) | Core — AI Workers, PostgreSQL, Valkey, API. **Sensitive data.** |
| **ybyra** 🌐 | Oracle Cloud · 1GB RAM | Primary edge — nginx, SPA frontend, Umami |
| **ybytu** ☁️ | Oracle Cloud · 1GB RAM | DNS (AdGuard), Homepage dashboard, Syncthing |
| **kuaray** ♻️ | Repurposed Dell laptop · i5-4200U · 6GB RAM · Linux Mint | Standby edge — warm failover + media |

> 🔒 **Data sovereignty**: Oracle nodes (ybyra/ybytu) run **only** non-sensitive edge services. AI inference, storage, and community data are 100% local on psicopompo and kuaray.

- **Tailscale** mesh network as backbone · CGNAT bypass · Public funnels
- **30+ containers** in production · PostgreSQL 16 · Valkey 8 · Nginx
- Monitoring: **Grafana + Loki + Promtail**
- Automated backups: Borg + pg_dump
- Core↔Edge latency: **19–70ms** via Tailscale
- GPU Management: VRAM mutex, circuit breaker, auto-exit after 180s idle

---

## 📊 Ecosystem Scale

| Metric | Value |
|--------|-------|
| Total lines of code | ~8M+ and growing |
| Files | 1,227+ |
| Years of development | 10 |
| StênioKernel modules | 22 |
| Check drivers | 132 |
| Anti-bypass layers | 10 |
| Documentation files | 185 |
| Containers in production | 30+ |
| Homelab nodes | 4 |

---

## 👤 Founder

**Carlos Eduardo Rodrigues** · Anthropologist (UnB), founder, PO, and StênioKernel architect.

Nearly a decade combining ethnographic research, technology, and data — with Sumænimá as the thread running through everything he builds. Built the **Tô no Mapa Platform** (integrated with Brazil's Federal Public Ministry) while at ISPN. Designed the **StênioKernel** — a proprietary AI Agent Governance Kernel that governs every AI agent on the project through 10 security layers, self-healing, cryptographic integrity, and predictive governance. Experienced firsthand the transformative potential of technology in the socio-environmental space — and also the burnout of using communication in service of others.

His fieldwork at **Fazenda Canadá** (Cavalcante-GO) connected him with **André Aquino** (Lead Environmental Specialist, World Bank) and **Daniel Ferreira** (Itamaraty diplomat), owners of the **Reserva Natural Veredas dos Buritis** — inside the thesis area. He worked with them on the **Participatory Fauna Monitoring Network**. This experience defined his hybrid perspective.

**Thesis:** *"Uma Assemblage de Projetos de Vida"* (UnB, 2023). **Co-author** in Land Use Policy (Elsevier, 2026). **Mercosur Scientific Journalism Award** winner. Documentary filmmaker ("RUA PARA QUE(M)?"). Architect of the **Mnemocine Homelab** and the **StênioKernel**.

**Master's in Anthropology:** chose to leave in pursuit of data, product design, and systems architecture.

A hybrid by nature — able to translate qualitative research needs into system requirements, and technical architecture into socio-environmental impact. One who builds the governance systems that make AI agents reliable, auditable, and accountable.

---

## 📋 Next Steps

1. Finalize StênioBOT beta for partner institution testing
2. Accelerator program for scale
3. Expand DataVis module with Cerrado and Amazon climate datasets
4. Mobile version for offline-first field collection
5. Marketplace of specialized AI models for qualitative research

---

**Contact:** [ceduardorodrig@gmail.com](mailto:ceduardorodrig@gmail.com) · +55 (61) 9-9803-3546
**Sumænimá:** [sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net)
