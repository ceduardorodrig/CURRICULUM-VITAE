# 🚀 Sumaenima — StênioBOT

**Plataforma de Etnografia com IA Local, Privada e Open-Source**

[sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net) | [github.com/ceduardorodrig](https://github.com/ceduardorodrig)

---

## 🎯 Visão Geral

**Fundador & Product Owner:** Carlos Eduardo Rodrigues

Sumaenima é meu projeto de vida. Existe há quase 10 anos como entidade criativa independente, atravessando toda minha carreira em paralelo aos empregos formais. Nasceu de uma convicção: pesquisa qualitativa — especialmente com comunidades tradicionais, indígenas e grupos vulneráveis — não deveria depender de infraestrutura de big tech para processar dados sensíveis. Mas por falta de recursos, seguiu como projeto paralelo durante anos — até que em 2024 comecei a construir a **StênioBOT**.

O sonho é captar recursos para ter equipe e construir um **Bureau de Dados** com alma antropológica: uma estrutura que produza projetos como o Tô no Mapa, visualizações de dados e pesquisa etnográfica em escala — unindo ciência, território e tecnologia de forma soberana.

Mas a camada mais profunda e valiosa da Sumaenima é invisível: o **StênioKernel** — um Kernel proprietário de Governança para Agentes de IA (21.435 linhas, 22 módulos de kernel, 132 drivers automatizados, 10 camadas anti-bypass) que governa todos os agentes de IA trabalhando no projeto. Ele aplica criptograficamente 13 leis absolutas, autocorrige violações, detecta tentativas de bypass e garante que nenhum agente escape da governança. É o sistema operacional que torna a IA confiável, auditável e responsável.

**StênioBOT** é uma plataforma de etnografia assistida por IA que roda 100% offline, em hardware local, sem enviar dados para nuvem. Quatro módulos integrados que cobrem o ciclo completo da pesquisa qualitativa: da coleta em campo à análise e visualização.

---

## ❓ O Problema

Pesquisadores, ONGs e instituições que trabalham com dados sensíveis enfrentam um dilema:
- Serviços cloud (Google, OpenAI, AWS) são caros e exigem envio de dados para servidores externos
- Alternativas locais são fragmentadas, mal documentadas e exigem conhecimento técnico profundo
- LGPD, GDPR e comitês de ética restringem cada vez mais o uso de soluções cloud para dados de pesquisa

Não existe uma plataforma integrada, local, privada e acessível para pesquisa qualitativa assistida por IA.

---

## 💡 A Solução — StênioBOT

### Módulos

- **StênioREC** — Transcrição em tempo real via Whisper large-v3-turbo com VAD, purificação via Gemma 3 (Neural Flow paralelo), exportação Google Docs em modo colaborativo
- **StênioPANEL** — Scanner de workshops físicos com GroundingDINO + SAM 2 + PaddleOCR, gerando esquemas `.canvas` compatíveis com Obsidian
- **StênioDIVE** — Mineração semântica cruzada de wikilinks, tags e notas em grafo interativo; embeddings e busca semântica local
- **DataVis** — Visualizações climáticas em tempo real (PM2.5, matriz energética, enchentes) com física de partículas

### Funcionalidades Transversais

- SaaS com assinaturas via Mercado Pago, Google OAuth com tokens criptografados
- CMS com editor TipTap WYSIWYG e biblioteca de imagens
- ERP: organizações, membros, leads, contratos, faturas, projetos
- Observabilidade: Grafana + Loki + Promtail

---

## ⚙️ Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | FastAPI (async) · Python 3.12+ · SQLAlchemy 2.0 (asyncpg) |
| **Frontend** | React 19 · Vite 8 · TypeScript 6 · Material Web Components (MD3) · Tailwind |
| **Banco** | PostgreSQL 16 · Alembic (migrations) |
| **Cache/Queue** | Valkey 8 (Redis-compatível) · Streams, Pub/Sub, arq job queues |
| **AI Áudio** | Whisper large-v3-turbo (transformers/PyTorch) · Gemma 3 (1B) |
| **AI Visão** | GroundingDINO · SAM 2 · PaddleOCR · Gemma 4B |
| **Infra** | Docker Swarm multi-nó · Docker Compose · NVIDIA GPU (RTX 5050) |
| **Rede** | Tailscale Funnel · Nginx reverse proxy |
| **Pagamentos** | Mercado Pago SDK |
| **Analytics** | Umami (self-hosted, privacy-first) |
| **Governança** | StênioKernel (21.435 linhas, 132 drivers, 22 módulos kernel) |
| **Monitoramento** | Grafana · Loki · Promtail |

---

## 🏗️ StênioKernel — Kernel de Governança para Agentes de IA

Este é o ativo mais profundo e valioso da Sumaenima. O StênioKernel não é um framework de QA — é um **Kernel proprietário de Governança para Agentes de IA** (construído do zero, sem fork de nenhum projeto open-source) projetado para governar agentes de IA em todo o ciclo de vida do software: código, documentação, infraestrutura e o próprio comportamento dos agentes.

- **22 módulos de kernel** (scheduler, guardian, healer, docbot, learner, registry, self-test, history, flakiness, classifier, impact, entre outros)
- **132 drivers de verificação** em 12 domínios (governança, segurança, frontend, infraestrutura, documentação, qualidade de código, deprecação, backend, dados, GPU, API, CMS)
- **21.435 linhas** de Python, zero dependência de frameworks de QA externos
- **Arquitetura plugin**: auto-descoberta via `CHECK_METADATA` em cada driver, scheduler com ThreadPoolExecutor + asyncio

### 🛡️ Arquitetura Anti-Bypass (10 Camadas)

| Camada | Mecanismo | O Que Impede |
|--------|-----------|--------------|
| 1. **Pre-Commit Hooks** | `pre-commit-config.yaml` — gate P0+sec+doc | Commit sem checagens estáticas |
| 2. **Bypass Guard** | `sec_ai_bypass_guard` — driver P0 | `--no-verify`, `\|\| true`, `2>/dev/null`, CI `continue-on-error` |
| 3. **No-Bypass Ops** | `sec_no_bypass` — driver P0 | `rsync+ssh` manual, `docker compose`, `npm run build`, `pg_dump` |
| 4. **Scope Guard** | `sec_scope_guard` — driver P0 | Runs parciais que escondem falhas (`--only`, `--tag`, `--scope`) |
| 5. **Imutabilidade do Kernel** | Hashes SHA256 de arquivos críticos | Agentes modificando o próprio kernel |
| 6. **Integridade das Leis** | Hash SHA256 das 13 Leis do AGENTS.md | Agentes alterando ou removendo regras |
| 7. **Protocolo de Conhecimento** | ADR-032 — herança de handoff obrigatória | Agentes ignorando contexto de sessões anteriores |
| 8. **Repetição → Regra** | ADR-034 — promove instruções repetidas | Instruções recorrentes ficando ad-hoc |
| 9. **A Teia** | `pm_omniscience` — jurisdição universal | Qualquer arquivo escapando da governança |
| 10. **Promoção de Warnings** | `__main__.py` promove P0/sec WARN→FAIL | Agentes ignorando warnings críticos |
| + **Bloqueio de Reassinatura** | Detecção de TTY + chaves de API | Agentes reassinando baselines de segurança |

### 🔧 Auto-Healing

O Healer não apenas reporta violações — ele as corrige autonomamente:
1. Extrai `arquivo:linha` das strings de violação
2. Consulta o **Knowledge Graph** (docs/external + registry + git log) por correções candidatas
3. Verifica o **Negative Registry** (`.steniocheck-negative-registry.json`) para pular tentativas já falhas
4. Aplica a correção com precisão de linha
5. Re-executa o check no contexto real para verificar
6. Se passar: `git add + git commit` automático, adiciona ao registry permanente
7. Se falhar: reverte, registra falha no negative registry, tenta próximo candidato

### 📊 Governança Preditiva

O kernel não apenas reporta falhas atuais — ele prevê as futuras:
- **Detecção de tendências**: regressão linear sobre contagens de violações nas últimas 10 execuções
- **Auto-suppress**: suprime warnings persistentes por N execuções consecutivas (limiar adaptativo)
- **Comparação com baseline**: `.steniocheck-baseline.json` para redução de ruído
- **Detecção de flakiness**: identifica checks que oscilam entre pass/fail
- **Promoção de canary**: promove automaticamente drivers com >80% de aprovação em 5+ execuções

### 🧠 Memória e Aprendizado

- **Persistência de histórico** (`.steniocheck-history.json`): armazena resultados em cache, rastreia hashes de arquivos, registra durações
- **Aprendizado contínuo**: `--learn`, `--learn --interactive`, `--learn-auto` (detecta correções do `git diff`)
- **Registry**: 40+ padrões de bug curados com `id`, `title`, `pattern`, `fix`, `auto_fix_commands`
- **Sugestões proativas**: `--suggest <fingerprint>` consulta o registry por soluções conhecidas
- **Knowledge Graph**: indexa `docs/external/` (MD3, Tailwind, MWC, FastAPI), padrões do registry e histórico git para correção por similaridade

### 📚 Documentação como Produto

- **185 arquivos** de documentação, **~74.000 linhas**
- **28 Architecture Decision Records (ADRs)** documentando cada decisão arquitetural
- **17 imperativos de engenharia** (I1-I17) com enforcement automatizado em CI
- **29 invariantes de negócio** formalmente especificados
- **DocBot**: baixa automaticamente READMEs do GitHub/GitLab, arquiva docs não utilizadas, reindexa o Knowledge Graph

### 🔄 Resiliência

- **FMEA vivo**: 54 nós de falha documentados (A-BB) com logging em tempo real (`fmea_events.jsonl`) e auditoria via LLM (`gemma_audit.jsonl`)
- **Audio WAL**: Write-Ahead Log com criptografia AES-GCM 256 + IndexedDB, detecção de falha em 3 camadas, resiliência silenciosa a quedas de rede
- **Circuit breaker adaptativo** via Valkey para Google Docs, Mercado Pago, OAuth e Umami
- **Neural Flow**: pipeline dual-stage Whisper (draft sub-500ms) + Gemma (refinamento) com política de tolerância zero a alucinações
- **Cross-worker handoff**: sessão persistida em Valkey com TTL de 8h, qualquer worker pode retomar contexto

### 🔍 Autodiagnóstico

O kernel audita a si mesmo:
- `--blame`: rastreia cada violação até o commit, autor e data específicos via `git blame`
- `--self-test`: 19 auto-testes validando GC1-GC12, imports dos drivers, formato do registry, Knowledge Graph, tipos de blame, healer, ciclo de histórico
- `--guardian`: auto-auditoria que detecta desvio de hash, gaps no registry, quedas suspeitas de violações, candidatos canary, degradação de performance, anomalias de timeout
- `.steniocheck-driver-hashes.json`: sela criptograficamente cada arquivo de driver contra modificação não autorizada

---

## 🖥️ Infraestrutura — Homelab Mnemocine

O **Homelab Mnemocine** é a infraestrutura da **Sumaenima**. São indistinguíveis — prova de conceito rodando em hardware real, sem dependência de cloud comercial para dados sensíveis.

| Nó | Hardware | Função |
|----|----------|--------|
| **psicopompo** 🧠 | Dell Frankenstein · Xeon E-2246G 6C/12T · RTX 5050 · 46GB RAM · CachyOS (Arch) | Core — Workers IA, PostgreSQL, Valkey, API. **Dados sensíveis.** |
| **ybyra** 🌐 | Oracle Cloud · 1GB RAM | Edge primário — nginx, SPA frontend, Umami |
| **ybytu** ☁️ | Oracle Cloud · 1GB RAM | DNS (AdGuard), dashboard (Homepage), Syncthing |
| **kuaray** ♻️ | Dell notebook reaproveitado · i5-4200U · 6GB RAM · Linux Mint | Edge standby — failover warm + multimídia |

> 🔒 **Soberania de dados**: nós Oracle (ybyra/ybytu) rodam **apenas** serviços de borda não-sensíveis. Inferência de IA, armazenamento e dados de comunidades são 100% locais em psicopompo e kuaray.

- Rede mesh **Tailscale** como backbone · CGNAT bypass · Funnels públicos
- **30+ containers** em produção · PostgreSQL 16 · Valkey 8 · Nginx
- Monitoramento: **Grafana + Loki + Promtail**
- Backup automatizado: Borg + pg_dump
- Latência Core↔Edge: **19–70ms** via Tailscale
- GPU Management: VRAM mutex, circuit breaker, auto-exit após 180s idle

---

## 👤 Fundador

**Carlos Eduardo Rodrigues** · Antropólogo (UnB), founder, PO e arquiteto do StênioKernel.

Há quase 10 anos combinando pesquisa etnográfica, tecnologia e dados — com a Sumaenima como fio condutor. Construiu a **Plataforma Tô no Mapa** (integrada ao MPF) enquanto estava no ISPN. Projetou o **StênioKernel** — um Kernel proprietário de Governança para Agentes de IA que governa todos os agentes de IA do projeto através de 10 camadas de segurança, auto-healing, integridade criptográfica e governança preditiva. Viveu na pele o potencial transformador da tecnologia no socioambiental — e também o burnout de usar comunicação a serviço de terceiros.

Sua pesquisa de campo na **Fazenda Canadá** (Cavalcante-GO) o conectou com **André Aquino** (Lead Environmental Specialist, World Bank) e **Daniel** (diplomata, Itamaraty), proprietários da **Reserva Natural Veredas dos Buritis** — dentro da área do seu TCC. Trabalhou com eles na **Rede de Monitoria Participativa da Fauna**. Essa experiência definiu seu olhar híbrido.

**Monografia:** *"Uma Assemblage de Projetos de Vida"* (UnB, 2023). **Coautor** em Land Use Policy (Elsevier, 2026). **Prêmio Mercosul** de Jornalismo Científico. Documentarista ("RUA PARA QUE(M)?"). Arquiteto do **Homelab Mnemocine** e do **StênioKernel**.

**Mestrado em Antropologia (interrompido):** largou para se dedicar a dados, design de produto e arquitetura de sistemas.

Híbrido por natureza — capaz de traduzir necessidades de pesquisa qualitativa em requisitos de sistema, e arquitetura técnica em impacto socioambiental. Alguém que constrói os sistemas de governança que tornam agentes de IA confiáveis, auditáveis e responsáveis.

---

## 📋 Próximos Passos

1. Finalizar beta da StênioBOT para testes com instituições parceiras
2. Programa de aceleração para escala
3. Expansão do módulo DataVis com datasets climáticos do Cerrado e Amazônia
4. Versão mobile para coleta em campo offline-first
5. Marketplace de modelos de IA especializados para pesquisa qualitativa

---

**Contato:** [ceduardorodrig@gmail.com](mailto:ceduardorodrig@gmail.com) · +55 (61) 9-9803-3546
**Sumaenima:** [sumaenima.chimaera-heptatonic.ts.net](https://sumaenima.chimaera-heptatonic.ts.net)
