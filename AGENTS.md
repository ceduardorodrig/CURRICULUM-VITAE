# AGENTS.md — Regras de Governança para Agentes de IA

Este repositório contém **3 versões de currículo em PT e EN** (tech, socioambiental, sumænimá), **duas sub-versões** (`02-socioambiental-nichado-pt.md` para contexto institucional [PT], `02-socioenvironmental-niche-en.md` para o mesmo contexto em EN, e `01-tech-dados-negocios-pt.md` para consultoria em dados de negócios), um **README narrativo**, e um sistema de validação (cvcheck) que é uma miniatura funcional do StênioKernel.

Ao modificar qualquer arquivo deste repositório, siga estas regras obrigatoriamente:

## 🔄 Consistência entre Arquivos

1. **Revise o README.md** — toda experiência nova, evento ou conquista adicionada em qualquer CV deve estar refletida na seção "Narrativa" do README (PT e EN). Se não estiver, o README está desatualizado.

2. **Revise TODAS as versões pertinentes** — uma mudança no `02-socioambiental` pode ser relevante para `01-tech` e `03-sumaenima`. Exemplo: adicionar uma relatoria do CNPCT no 02-socioambiental significa que o 01-tech e 03-sumaenima também devem mencionar se for relevante ao perfil.

3. **Mantenha PT e EN sincronizados** — se adicionou conteúdo em português, crie a versão em inglês no arquivo correspondente em `en-us/`. Revise a tradução: termos técnicos e nomes de instituições brasileiras podem ser mantidos em português com explicação em inglês na primeira ocorrência.

4. **Sub-versões específicas** — o arquivo `02-socioambiental-nichado-pt.md` (PT) e `02-socioenvironmental-niche-en.md` (EN) são sub-versões para contextos institucionais. Mudanças nos arquivos `02-socioambiental-tech-pt.md` / `02-socioenvironmental-tech-en.md` que sejam relevantes para este perfil (relatorias governamentais, articulação com órgãos públicos, experiências com comunidades tradicionais) devem ser replicadas na sub-versão correspondente.

5. **Narrativa do README** — a seção "O Fio da Meada" / "The Thread" conta a trajetória do autor em formato de história. Novas experiências não precisam de um parágrafo inteiro, mas devem ser mencionadas se representarem um marco na carreira.

## ✅ Verificação Obrigatória

6. **Rode `./scripts/stenio_check` antes de todo commit** — a verificação cobre ortografia (PT e EN), estrutura, links, datas, consistência bilíngue, paridade PT↔EN. A validação é feita pelo StênioKernel unificado (`python -m steniocheck --tag resume`). Nunca commite sem rodar.

7. **O cvcheck foi substituído** — o diretório `cvcheck/` foi removido. O kernel unificado está em `/mnt/NVME_PCI/sumaenimahub/SUMAENIMA-HUB/scripts/steniocheck/`. Use `./scripts/stenio_check` que chama o kernel com o perfil `resume`. Não edite drivers do steniocheck sem seguir o onboarding (Lei 16 do AGENTS.md do kernel).

8. **README como fonte da verdade narrativa** — a seção "Narrativa" é o único lugar onde a história é contada de forma contínua. Os CVs são versões recortadas para públicos específicos. Se uma informação nova for adicionada a um CV, verifique se ela merece um lugar na narrativa do README.

## 🤖 CI e Deploy Key

9. **O CI roda o mesmo kernel unificado** — o workflow `.github/workflows/ci.yml` faz checkout do SUMAENIMA-HUB (repositório privado do StênioKernel) via SSH deploy key e executa `steniocheck --tag resume --scope static --format github`. Agentes **nunca** devem modificar, remover ou contornar as verificações do CI.

10. **O segredo `STENIOCHECK_SSH_KEY` é intocável** — a chave SSH privada está armazenada como secret do GitHub Actions e é usada exclusivamente pelo `actions/checkout` para acessar o SUMAENIMA-HUB. Agentes **não** devem ler, alterar, remover ou expor este segredo de nenhuma forma. A chave pública correspondente está registrada como deploy key read-only no SUMAENIMA-HUB.
