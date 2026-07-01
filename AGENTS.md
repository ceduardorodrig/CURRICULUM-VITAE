# AGENTS.md — Regras de Governança para Agentes de IA

Este repositório contém **3 versões de currículo em PT e EN** (tech, socioambiental, sumænimá), uma **sub-versão específica** (socioambiental-icmbio), um **README narrativo**, e um sistema de validação (cvcheck) que é uma miniatura funcional do StênioKernel.

Ao modificar qualquer arquivo deste repositório, siga estas regras obrigatoriamente:

## 🔄 Consistência entre Arquivos

1. **Revise o README.md** — toda experiência nova, evento ou conquista adicionada em qualquer CV deve estar refletida na seção "Narrativa" do README (PT e EN). Se não estiver, o README está desatualizado.

2. **Revise TODAS as versões pertinentes** — uma mudança no `02-socioambiental` pode ser relevante para `01-tech` e `03-sumaenima`. Exemplo: adicionar uma relatoria do CNPCT no 02-socioambiental significa que o 01-tech e 03-sumaenima também devem mencionar se for relevante ao perfil.

3. **Mantenha PT e EN sincronizados** — se adicionou conteúdo em português, crie a versão em inglês no arquivo correspondente em `en-us/`. Revise a tradução: termos técnicos e nomes de instituições brasileiras podem ser mantidos em português com explicação em inglês na primeira ocorrência.

4. **Sub-versões específicas** — o arquivo `02-socioambiental-icmbio.md` é uma versão especializada para o ICMBio. Mudanças no `02-socioambiental-tech.md` que sejam relevantes para este público (relatorias governamentais, articulação com órgãos públicos, experiências com comunidades tradicionais) devem ser replicadas na sub-versão.

5. **Narrativa do README** — a seção "O Fio da Meada" / "The Thread" conta a trajetória do autor em formato de história. Novas experiências não precisam de um parágrafo inteiro, mas devem ser mencionadas se representarem um marco na carreira.

## ✅ Verificação Obrigatória

6. **Rode `python -m cvcheck` antes de todo commit** — a verificação cobre ortografia (PT e EN), estrutura, links, datas, consistência bilíngue, imutabilidade do kernel e auto-auditoria. Nunca commite sem rodar.

7. **Nunca edite arquivos em `cvcheck/` sem atualizar hashes** — se precisar modificar drivers do cvcheck, execute `python -m cvcheck --fix` depois para reconstruir o baseline de hashes.

8. **README como fonte da verdade narrativa** — a seção "Narrativa" é o único lugar onde a história é contada de forma contínua. Os CVs são versões recortadas para públicos específicos. Se uma informação nova for adicionada a um CV, verifique se ela merece um lugar na narrativa do README.
