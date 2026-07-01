# 👤 Carlos Eduardo Rodrigues

**Data & Product Architect** | Anthropology meets Local AI Engineering

[ceduardorodrig@gmail.com](mailto:ceduardorodrig@gmail.com) | +55 (61) 9-9803-3546 | Brasília-DF, Brazil

[linkedin.com/in/c-eduardo-rodrigues](https://linkedin.com/in/c-eduardo-rodrigues) | [github.com/ceduardorodrig](https://github.com/ceduardorodrig) | [sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net)

---

## 👤 Profile

Data and product architect who bridges open-source technology and qualitative research. Proven track record designing local AI pipelines (Whisper, LLMs), orchestrating multi-node Docker Swarm clusters, and building data products from scratch. Ingenious use of repurposed hardware and free software to deliver private, offline, cost-effective AI solutions — with zero dependency on big tech infrastructure. Designed the StênioKernel — a proprietary AI Agent Governance Kernel (21.435 lines, 132 check drivers, 10 anti-bypass layers) that enforces agent behavior through cryptographic integrity, self-healing, and predictive governance. Anthropology degree from UnB as the foundation for human-centered product design.

---

## 💼 Experience

### 🚀 Sumænimá — Founder & Product Owner
*2016 — present · Brasília-DF / Remote*

Sumænimá is my life project. It has existed for nearly 10 years as an independent creative entity, running alongside formal employment throughout my entire career. What keeps me going is the dream of one day raising resources to build a team and create a **Data Bureau** with an anthropological soul.

**StênioBOT** (2024–present): an AI-assisted data capture platform running 100% local inference. Four modules:

- **StênioREC**: real-time transcription (Whisper large-v3-turbo) with VAD, Gemma 3 purification pipeline, Google Docs export
- **StênioPANEL**: physical workshop scanner with computer vision (GroundingDINO + SAM 2 + PaddleOCR)
- **StênioDIVE**: cross-semantic mining of wikilinks, tags, and notes in an interactive graph
- **DataVis**: interactive climate visualizations with particle physics and real-time data

Stack: FastAPI (async) + React 19 + TypeScript 6 + PostgreSQL 16 + Valkey 8 + Docker Swarm (3 nodes). SaaS with Mercado Pago billing, Google OAuth, Grafana/Loki observability. Fully offline, private, LGPD-compliant.

**StênioKernel — Agent Governance Kernel:**
- Proprietary kernel (21.435 lines, 22 kernel modules, 132 check drivers) governing every AI agent on the project. Total ecosystem: **~8M+ lines and growing**, 1,227+ files, 10 years of development
- 10-layer anti-bypass architecture: pre-commit gates, bypass guard, scope guard, kernel immutability, cryptographically-signed agent laws, knowledge protocol, repetition→rule, universal file jurisdiction ("A Teia"), WARN→FAIL promotion, automated re-signing blockade
- Self-healing with negative registry, Knowledge Graph, auto-commit on fix
- Predictive governance: trend detection via linear regression, auto-suppress, flakiness detection, canary promotion
- Memory & learning: history persistence, continuous learning (`--learn`), curated bug patterns with auto-fix commands, proactive suggestions
- Full documentation ecosystem: 185 files, DocBot
- Living FMEA, Audio WAL, Neural Flow, adaptive circuit breaker

**Reporting & Data Systematization** (alongside StênioBOT):
- Independent consultant for reporting, data systematization, and strategic planning
- **3rd National Youth Meeting of Extractive and Traditional Populations** — Sociobiodiversity Week 2025 (IEB/CNS/MCM/CONFREM). Produced with **Stênio v1** — the first operational version of the platform in production
- **Module II — "Formar Protagonistas"** (IEB/APAFE/Rainforest Trust): 39 leadership members from FLONA de Tefé in Brasília
- **IPEA Strategic Planning** (2026) — reporting and systematization

### 🗺️ ISPN — Institute for Society, Population and Nature
*2017 — 2021 · Brasília-DF, Brazil*

**Junior Technical Advisor** (2019–2021) · **Trainee** (2017–2019)

- **Tô no Mapa**: the project that defined my hybrid career. Started as an ethnographic field researcher with traditional Cerrado communities and helped transform a data collection initiative into the **Tô no Mapa Platform** — now integrated with Brazil's **Federal Public Ministry**, empowering thousands of communities to self-map their territories
- Created the Institute's first public communications strategy in years
- Produced maps (QGIS), reports, and photographic coverage during field expeditions
- Provided technical support for large-scale events: Acampamento Terra Livre, Encontro e Feira dos Povos do Cerrado, Latin American Agroecology Congress

### 🦎 Participatory Fauna Monitoring Network
*2020 — 2022 · Cavalcante-GO, Brazil*

**Communications Specialist**

Worked directly with **André Rodrigues de Aquino** (Lead Environmental Specialist at the World Bank, former Senior Natural Resources Manager) and **Daniel Ferreira** (Itamaraty diplomat), owners of the **Reserva Natural Veredas dos Buritis** — located **inside** the Fazenda Canadá area, the subject of my undergraduate thesis. Supported the facilitation of the network's inaugural meeting, bringing together ICMBio, UnB, NGOs, and rural landowners to structure a wildlife corridor between Chapada dos Veadeiros National Park and the Kalunga Historical Site. Produced the complete executive report.

### 🌳 IPAM — Amazon Environmental Research Institute
*2022 — 2025 · Brasília-DF, Brazil*

**Communication Analyst** (2024–2025) · **Communication Assistant** (2023–2024) · **Trainee** (2022–2023)

- Implemented Agile/Scrum as Scrum Master for the communications team
- Managed audience data across 5 social networks: **2+ million users** reached
- Administered Google Ad Grants (US$ 10K/month) and Meta Ads with A/B testing
- Co-directed **"Manaus Extrema"** documentary (premiered at INPA / 2024 PROTEJA Talks)
- **Mercosur Scientific Journalism Award — 1st place, Social Networks** (2024)
- Served as CIPA president for two terms

---

## 🎓 Education

**University of Brasília (UnB)** — Bachelor's Degree in Social Sciences / Anthropology (2016–2023)

- **Thesis:** *"Uma Assemblage de Projetos de Vida: mudanças organizacionais na Fazenda Canadá, Cavalcante-GO"* (2023). Advisor: Prof. Henyo Trindade Barretto Filho. Ethnography on land subdivision, memory, and life projects in Chapada dos Veadeiros. Field research conducted in the same region as the Veredas dos Buritis reserve and the Fauna Monitoring Network — all interconnected.

**Master's in Anthropology** — University of Brasília (2024–2025)
Two semesters completed. Chose to leave the program to dedicate myself fully to data, product design, and systems architecture. This decision defined my career transition.

---

## 📡 Infrastructure — Sumænimá & Mnemocine

The **Mnemocine Homelab** is the **Sumænimá** infrastructure. They are indistinguishable — a multi-node cluster orchestrated via Docker Swarm providing AI, database, cache, DNS, monitoring, and web edge services.

| Node | Hardware | Role |
|------|----------|------|
| **psicopompo** 🧠 | Dell Frankenstein · Xeon E-2246G 6C/12T · RTX 5050 · 46GB RAM · CachyOS (Arch) | Core — AI, database, Swarm manager. **Sensitive data stays here.** |
| **ybyra** 🌐 | Oracle Cloud · 1GB RAM | Primary edge — nginx, SPA frontend, Umami analytics |
| **ybytu** ☁️ | Oracle Cloud · 1GB RAM | DNS (AdGuard), Homepage dashboard, Syncthing |
| **kuaray** ♻️ | Repurposed Dell laptop · i5-4200U · 6GB RAM · Linux Mint | Standby edge — warm failover + media |

> 🔒 **Data sovereignty**: Oracle nodes run **only** non-sensitive edge services (nginx, DNS, analytics). Data processing, AI inference, and storage are 100% local on psicopompo and kuaray. Community data never leaves your control.

- **Tailscale** mesh network as backbone (CGNAT bypass, public funnels)
- **30+ containers** in production (PostgreSQL, Valkey, nginx, AdGuard, Home Assistant, *arr stack)
- Monitoring: **Grafana + Loki + Promtail**, backups: Borg + pg_dump
- Daily driver: Arch Linux (CachyOS)

---

## 📚 Publications

- **Co-author** — Moser, P. et al. *"Institutional Invisibility Threatens the Lands and Livelihoods of Traditional Communities in the Northern Brazilian Cerrado"* — Submitted to **Land Use Policy** (Elsevier, 2026). Field research conducted during undergraduate studies in Anthropology at UnB.
- **Documentary** — *RUA PARA QUE(M)?* (85min, 2020) — Direction, photography, editing. Visual ethnography of Brasília's neo-fanfarre movement. Published by Sumænimá.
- **Documentary** — *Manaus Extrema* (2024) — Co-direction. Climate change in urban Amazonia. Premiered at INPA / 2024 PROTEJA Talks.

---

## 🛠️ Skills

| Category | Technologies |
|----------|-------------|
| **Backend** | FastAPI, Python, SQLAlchemy, asyncpg, REST APIs, WebSockets |
| **Frontend** | React, TypeScript, Vite, Tailwind, Material Web Components |
| **Database** | PostgreSQL, Alembic, SQL, data modeling |
| **Infrastructure** | Docker Swarm, Nginx, Tailscale, Linux (Arch), GPU passthrough |
| **AI/ML** | Whisper (transcription), LLMs (Gemma), GroundingDINO, SAM 2, embeddings |
| **QA & Governance** | StênioKernel (21K lines, 132 drivers, 22 kernel modules), FMEA, ADRs, docs-first CI/CD |
| **Agent Governance** | StênioKernel anti-bypass architecture (10 layers), agent workflow design, cryptographic agent law enforcement, self-healing governance |
| **Observability** | Grafana, Loki, Promtail, health endpoints |
| **Methods** | Agile/Scrum (Scrum Master), ethnographic research, UX Research, OKRs |
| **Tools** | Git, Adobe Creative Suite, QGIS, Google Earth Engine |

---

## 🌐 Languages

- **Portuguese** — Native
- **English** — Fluent (reading, writing, technical and academic conversation)
