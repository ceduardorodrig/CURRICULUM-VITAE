# 👤 Carlos Eduardo Rodrigues

**Arquiteto de Dados & Produto** | Antropologia + Engenharia de IA Local

[ceduardorodrig@gmail.com](mailto:ceduardorodrig@gmail.com) | +55 (61) 9-9803-3546 | Brasília-DF

[linkedin.com/in/c-eduardo-rodrigues](https://linkedin.com/in/c-eduardo-rodrigues) | [github.com/ceduardorodrig](https://github.com/ceduardorodrig) | [sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net)

---

## 👤 Perfil

Arquiteto de dados e produto que constrói pontes entre tecnologia open-source e pesquisa qualitativa. Experiência comprovada em projetar pipelines de IA local (Whisper, LLMs, GroundingDINO, SAM 2), orquestrar clusters Docker Swarm multi-nó e gerenciar produtos de dados completos, do conceito à entrega. Uso engenhoso de hardware reaproveitado e software livre para entregar soluções de IA privadas, offline e economicamente viáveis — sem depender de infraestrutura de big tech. Projetou o StênioKernel — um Kernel proprietário de Governança para Agentes de IA (21.435 linhas, 132 drivers, 10 camadas anti-bypass) que governa o comportamento de agentes através de integridade criptográfica, correção automatizada com rollback e análise de tendências. Formação em Antropologia pela UnB como base para design de produto centrado em humanos.

---

## 💼 Experiência

### 🚀 Sumænimá — Fundador & Product Owner
*2016 — presente · Brasília-DF / Remoto*

Sumænimá é meu projeto de vida. Existe há quase 10 anos como entidade criativa independente, atravessando toda minha carreira em paralelo aos empregos formais. O que me mantém é o sonho de um dia captar recursos para ter equipe e construir um **Bureau de Dados** com alma antropológica.

**StênioBOT** (2024–presente): plataforma de captura de dados assistida por IA com inferência 100% local. Quatro módulos:

- **StênioREC** 🟢: transcrição em tempo real (Whisper large-v3-turbo) com VAD, purificação via Gemma 3 e exportação Google Docs — **em produção**, validado em relatoria de campo
- **StênioPANEL** 🔴: scanner de workshops com visão computacional (GroundingDINO + SAM 2 + PaddleOCR) — **concepção**, aguardando recursos
- **StênioDIVE** 🔴: mineração semântica cruzada de wikilinks, tags e notas em grafo interativo — **concepção**, aguardando recursos
- **DataVis** 🔴: visualizações climáticas com física de partículas e dados em tempo real — **concepção**, em estágio inicial

Stack: FastAPI (async) + React 19 + TypeScript 6 + PostgreSQL 16 + Valkey 8 + Docker Swarm (3 nós). SaaS com Mercado Pago, Google OAuth, Grafana/Loki. Processamento local com sincronização sob demanda. Privado, LGPD.

**StênioKernel — Kernel de Governança para Agentes de IA:**
- Kernel proprietário (21.435 linhas, 22 módulos kernel, 132 drivers) governando todos os agentes de IA do projeto. Ecossistema total: **~8M+ linhas e crescendo** (inclui código fonte, documentação e assets), 1.227+ arquivos, 10 anos como projeto de vida (~2 de desenvolvimento ativo)
- Arquitetura anti-bypass em 10 camadas: pre-commit gates, bypass guard, scope guard, imutabilidade do kernel, leis de agentes com assinatura criptográfica, protocolo de conhecimento, repetição→regra, jurisdição universal ("A Teia"), promoção WARN→FAIL, bloqueio de reassinatura automatizado
- Correção automatizada com rollback via negative registry, Knowledge Graph, auto-commit em correções bem-sucedidas
- Análise de tendências: detecção via regressão linear, auto-suppress, detecção de flakiness, promoção de canary
- Memória e aprendizado: persistência de histórico, aprendizado contínuo (`--learn`), padrões de bug com auto-fix commands, sugestões proativas
- Ecossistema de documentação: 185 arquivos, DocBot
- FMEA vivo, Audio WAL, Neural Flow, circuit breaker adaptativo

**Relatoria & Sistematização de Dados** (paralelo à StênioBOT):
- Consultor independente em relatoria, sistematização de dados e planejamento estratégico
- Relatoria do **3º Encontro Nacional da Juventude das Populações Extrativistas e Tradicionais** — Semana da Sociobiodiversidade 2025 (IEB/CNS/MCM/CONFREM). Realizada com **Stênio v1** — primeira versão operacional da plataforma em produção
- Relatoria do **Módulo II — "Formar Protagonistas"** (IEB/APAFE/Rainforest Trust): imersão de 39 lideranças da FLONA de Tefé em Brasília
- **Encontro de Planejamento Estratégico do IPEA** (jun/2026) — relatoria dos Movimentos 5 (Integração, comunidade e colaboração) e 7 (Gestão da Informação) com transcrição em tempo real via StênioREC e observação etnográfica. Evento de 3 dias no ParlaMundi da LBV e sede do IPEA, contratado via **Imagine Gestão Social**, resultando na agenda estratégica 2026–2027 do instituto
- **CNPCT (Conselho Nacional dos Povos e Comunidades Tradicionais):** Acompanhamento e relatoria das reuniões desde 2025, incluindo a 22ª Reunião Ordinária (mar/2026) com devolutiva do Decreto de Regularização Fundiária no Palácio do Planalto e fala de abertura da Ministra Marina Silva — transcrição em tempo real via StênioREC

### 🗺️ ISPN — Instituto Sociedade, População e Natureza
*2017 — 2021 · Brasília-DF*

**Assessor Técnico Júnior** (2019–2021) · **Estagiário** (2017–2019)

- **Tô no Mapa**: Dados oficiais do governo representavam apenas 28% das comunidades tradicionais no Cerrado — uma lacuna crítica que as tornava "invisíveis". Participei da pesquisa etnográfica em campo e da fase de discovery do produto, ajudando a definir o problema central e as necessidades dos usuários. O resultado foi a **Plataforma Tô no Mapa** — um aplicativo de automapeamento que hoje está integrada ao **Ministério Público Federal**, empoderando milhares de comunidades tradicionais a gerar seus próprios dados e se colocar no mapa
- Criei a primeira estratégia de comunicação pública do Instituto em anos
- Produzi mapas (QGIS), relatórios e cobertura fotográfica em expedições de campo
- Apoio técnico a eventos socioambientais de grande porte: Acampamento Terra Livre, Encontro e Feira dos Povos do Cerrado, Congresso Latino-Americano de Agroecologia

### 🦎 Rede de Monitoria Participativa da Fauna
*2020 — 2022 · Cavalcante-GO*

**Especialista em Comunicação**

Trabalhei diretamente com **André Rodrigues de Aquino** (Lead Environmental Specialist do World Bank, então gerente sênior de recursos naturais) e **Daniel Ferreira** (diplomata do Itamaraty), proprietários da **Reserva Natural Veredas dos Buritis** — que fica **dentro** da Fazenda Canadá, área do meu TCC. Apoiei a facilitação da reunião inaugural da Rede de Monitoria, que buscava criar um corredor ecológico entre o Parque Nacional da Chapada dos Veadeiros e o Sítio Histórico Kalunga, reunindo ICMBio, UnB, ONGs e proprietários rurais. Produzi relatório executivo completo (concepção, redação, fotografia, diagramação).

### 🌳 IPAM — Instituto de Pesquisa Ambiental da Amazônia
*2022 — 2025 · Brasília-DF*

**Analista de Comunicação** (2024–2025) · **Assistente de Comunicação** (2023–2024) · **Estagiário** (2022–2023)

**Case: Scaling Digital Engagement — +143% de crescimento em comunicação científica climática**

Tratei os canais sociais do IPAM como produtos digitais: segmentei audiências (Instagram: público jovem; Facebook: audiência consolidada), testei formatos como features (infográficos, storytelling visual, posts interativos) e integrei campanhas orgânicas e pagas.

**📈 Resultados:**
- **+143,3%** de seguidores no Facebook, **+100%** no Instagram
- **2+ milhões** de alcance consolidado (1,6M nos canais principais)
- **66,7K** interações no Instagram — canal validado como principal para engajamento de alto valor

Outras entregas:
- Implementei Agile/Scrum como Scrum Master, estruturando sprints e métricas de entrega
- Gerenciei Google Ad Grants (US$ 10K/mês) e Meta Ads com segmentação e otimização contínua
- Codiretor do documentário **"Manaus Extrema"** — publicado pelo IPAM. Estreia no INPA / PROTEJA Talks 2024
- Apoio à organização e comunicação institucional do **evento do SOMUC na UFAC** (2024), sobre monitoramento de Unidades de Conservação na Amazônia, com participação de servidores do ICMBio e pesquisadores
- **Prêmio Mercosul de Jornalismo e Divulgação Científica — 1º lugar, categoria Redes Sociais** (2024)
- Presidi a CIPA por dois mandatos

---

## 🎓 Formação

**Universidade de Brasília (UnB)** — Bacharelado em Ciências Sociais / Antropologia (2016–2023)

- **Monografia:** *"Uma Assemblage de Projetos de Vida: mudanças organizacionais na Fazenda Canadá, Cavalcante-GO"* (2023). Orientação: Prof. Henyo Trindade Barretto Filho. Etnografia sobre o fracionamento de terras, memória e projetos de vida na Chapada dos Veadeiros. A pesquisa de campo foi realizada na mesma região onde ficam a Reserva Veredas dos Buritis e a Rede de Monitoria — tudo interligado.

**Mestrado em Antropologia** — Universidade de Brasília (2024–2025)
Dois semestres concluídos. Escolhi sair do mestrado para me dedicar integralmente a dados, design de produto e arquitetura de sistemas. Esta decisão definiu minha transição de carreira.

---

## 📡 Infraestrutura — Sumænimá & Mnemocine

O **Homelab Mnemocine** é a infraestrutura da **Sumænimá**. São indistinguíveis — um cluster multi-nó orquestrado via Docker Swarm que provê serviços de IA, banco, cache, DNS, monitoramento e borda web.

| Nó | Hardware | Papel |
|----|----------|-------|
| **psicopompo** 🧠 | Dell Frankenstein · Xeon E-2246G 6C/12T · RTX 5050 · 46GB RAM · CachyOS (Arch) | Core — IA, banco, Swarm manager. **Dados sensíveis ficam aqui.** |
| **ybyra** 🌐 | Oracle Cloud · 1GB RAM | Edge primário — nginx, SPA frontend, Umami analytics |
| **ybytu** ☁️ | Oracle Cloud · 1GB RAM | DNS (AdGuard), dashboard Homepage, sincronização Syncthing |
| **kuaray** ♻️ | Dell notebook reaproveitado · i5-4200U · 6GB RAM · Linux Mint | Edge standby — failover warm + multimídia |

> 🔒 **Soberania de dados**: os nós Oracle (ybyra/ybytu) rodam **apenas** serviços de borda não-sensíveis (nginx, DNS, analytics). Processamento de dados, inferência de IA e armazenamento são 100% locais em psicopompo e kuaray. Dados de comunidades nunca saem do seu controle.

- Rede mesh **Tailscale** como backbone (bypass de CGNAT, funnels públicos)
- **30+ containers** em produção (PostgreSQL, Valkey, nginx, AdGuard, Home Assistant, *arr stack)
- Monitoramento com **Grafana + Loki + Promtail**, backups Borg + pg_dump
- Desktop principal: Arch Linux (CachyOS) — daily driver

---

## 📚 Publicações

- **Coautor** — Moser, P. et al. *"Institutional Invisibility Threatens the Lands and Livelihoods of Traditional Communities in the Northern Brazilian Cerrado"* — Submetido a **Land Use Policy** (Elsevier, 2026). A pesquisa de campo que fundamenta o artigo foi realizada durante minha graduação em Antropologia na UnB.
- **Artigo** — Rodrigues, C.E. *"Doenças são sintomas de uma crise cultural e ambiental"* — JOTA, Em Clima de Justiça (2026). [Ler](https://www.jota.info/opiniao-e-analise/colunas/em-clima-de-justica/doencas-sao-sintomas-de-uma-crise-cultural-e-ambiental)
- **Documentário** — *RUA PARA QUE(M)?* (85min, 2020) — Direção, fotografia, edição. Etnografia visual do movimento neo-fanfarrista de Brasília. Publicado pela Sumænimá.
- **Documentário** — *Manaus Extrema* (2024) — Codireção. Mudanças climáticas na Amazônia urbana. Publicado pelo IPAM. Estreia no INPA / PROTEJA Talks 2024.

---

## 🛠️ Habilidades

| Categoria | Tecnologias |
|-----------|-------------|
| **Backend** | FastAPI, Python, SQLAlchemy, asyncpg, REST APIs, WebSockets |
| **Frontend** | React, TypeScript, Vite, Tailwind, Material Web Components |
| **Banco de Dados** | PostgreSQL, Alembic, SQL, modelagem de dados |
| **Infraestrutura** | Docker Swarm, Nginx, Tailscale, Linux (Arch), GPU passthrough |
| **AI/ML** | Whisper (transcrição), LLMs (Gemma), GroundingDINO, SAM 2, embeddings |
| **QA & Governança** | StênioKernel (21K linhas, 132 drivers, 22 módulos kernel), FMEA, ADRs, docs-first CI/CD |
| **Governança de Agentes** | StênioKernel arquitetura anti-bypass (10 camadas), design de workflow para agentes, aplicação criptográfica de regras, correção automatizada com rollback |
| **Observabilidade** | Grafana, Loki, Promtail, health endpoints |
| **Métodos** | Agile/Scrum (Scrum Master), pesquisa etnográfica, UX Research, OKRs |
| **Ferramentas** | Git, Adobe Creative Suite, QGIS, Google Earth Engine |

---

## 🌐 Idiomas

- **Português** — Nativo
- **Inglês** — Fluente (leitura, escrita, conversação técnica e acadêmica)
