# 🚀 Sumaenima — StênioBOT

**Ethnography Platform with Local, Private, Open-Source AI**

[sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net) | [github.com/ceduardorodrig](https://github.com/ceduardorodrig)

---

## 🎯 Overview

**Founder & Product Owner:** Carlos Eduardo Rodrigues

Sumaenima is my life project. It has existed for nearly 10 years as an independent creative entity, running alongside formal employment throughout my entire career. It was born from a conviction: qualitative research — especially with traditional communities, Indigenous peoples, and vulnerable groups — should never depend on big tech infrastructure. But due to lack of funding, it remained a side project for years — until 2024, when I started building **StênioBOT**.

The dream is to raise resources to build a team and create a **Data Bureau** with an anthropological soul: a structure that produces projects like Tô no Mapa, data visualizations, and ethnographic research at scale — uniting science, territory, and technology in a sovereign way.

**StênioBOT** is an AI-assisted ethnography platform running 100% offline on local hardware, with zero data sent to the cloud. Four integrated modules cover the complete qualitative research cycle: from field collection to analysis and visualization.

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

- **StênioREC** — Real-time transcription via Whisper large-v3-turbo with VAD, Gemma 3 Neural Flow purification, collaborative Google Docs export
- **StênioPANEL** — Physical workshop scanner with GroundingDINO + SAM 2 + PaddleOCR, generating Obsidian-compatible `.canvas` schemas
- **StênioDIVE** — Cross-semantic mining of wikilinks, tags, and notes in an interactive graph; local embeddings and semantic search
- **DataVis** — Real-time climate visualizations (PM2.5, energy matrix, floods) with particle physics

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
| **Monitoring** | Grafana · Loki · Promtail |

---

## 🏗️ Engineering & Governance

### Documentation as a Product

- **185 documentation files**, **~74,000 lines**
- **28 Architecture Decision Records (ADRs)** documenting every architectural decision
- **17 engineering imperatives** (I1-I17) with automated CI enforcement
- **29 business invariants** formally specified

### Steniokernel — QA Framework

- **66 automated check drivers** covering 12 domains (frontend, backend, security, infrastructure, GPU, documentation, dependencies, governance, data, CMS, performance, scenarios)
- **103 static checks** per git push
- Plugin architecture: drivers with auto-discovery via `CHECK_METADATA`
- Auto-healing, continuous learning (`--learn`), flaky test detection
- Pre-commit and GitHub Actions integration

### Resilience

- **Living FMEA**: 54 failure nodes (A-BB) with real-time logging (`fmea_events.jsonl`) and LLM auditing (`gemma_audit.jsonl`)
- **Audio WAL**: Write-Ahead Log with AES-GCM 256 encryption + IndexedDB, 3-layer failure detection, silent network resilience
- **Adaptive circuit breaker** via Valkey for Google Docs, Mercado Pago, OAuth, and Umami
- **Neural Flow**: dual-stage Whisper (sub-500ms draft) + Gemma (refinement) with zero-tolerance hallucination policy
- **Cross-worker handoff**: session state persisted in Valkey with 8h TTL, any worker can restore context

---

## 🖥️ Infrastructure — Mnemocine Homelab

The **Mnemocine Homelab** IS the **Sumaenima** infrastructure. They are indistinguishable — proof of concept running on real hardware with zero commercial cloud dependency for sensitive data.

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

## 👤 Founder

**Carlos Eduardo Rodrigues** · Anthropologist (UnB), founder and PO.

Nearly a decade combining ethnographic research, technology, and data — with Sumaenima as the thread running through everything he builds. Built the **Tô no Mapa Platform** (integrated with Brazil's Federal Public Ministry) while at ISPN. Experienced firsthand the transformative potential of technology in the socio-environmental space — and also the burnout of using communication in service of others.

His fieldwork at **Fazenda Canadá** (Cavalcante-GO) connected him with **André Aquino** (Lead Environmental Specialist, World Bank) and **Daniel** (Itamaraty diplomat), owners of the **Reserva Natural Veredas dos Buritis** — inside the thesis area. He worked with them on the **Participatory Fauna Monitoring Network**. This experience defined his hybrid perspective.

**Thesis:** *"Uma Assemblage de Projetos de Vida"* (UnB, 2023). **Co-author** in Land Use Policy (Elsevier, 2026). **Mercosur Scientific Journalism Award** winner. Documentary filmmaker ("RUA PARA QUE(M)?"). Architect of the **Mnemocine Homelab**.

**Master's in Anthropology (interrupted):** left to pursue data, product design, and systems architecture.

A hybrid by nature — able to translate qualitative research needs into system requirements, and technical architecture into socio-environmental impact.

---

## 📋 Next Steps

1. Finalize StênioBOT beta for partner institution testing
2. Accelerator program for scale
3. Expand DataVis module with Cerrado and Amazon climate datasets
4. Mobile version for offline-first field collection
5. Marketplace of specialized AI models for qualitative research

---

**Contact:** [ceduardorodrig@gmail.com](mailto:ceduardorodrig@gmail.com) · +55 (61) 9-9803-3546
**Sumaenima:** [sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net)
