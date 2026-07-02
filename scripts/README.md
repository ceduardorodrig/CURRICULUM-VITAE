# Scripts de Validação

Este diretório substitui o antigo `cvcheck/`. A validação agora é feita
pelo **StênioKernel** unificado, localizado em:

```
/mnt/NVME_PCI/sumaenimahub/SUMAENIMA-HUB/scripts/steniocheck
```

## Uso

```bash
# Rodar todas as verificações do perfil resume
./scripts/stenio_check

# Auto-teste do kernel
./scripts/stenio_check --self-test

# Listar drivers disponíveis
./scripts/stenio_check 2>&1 | grep resume_
```

O perfil `resume` inclui 10 drivers que validam:
- Datas PT-BR
- Ortografia (PT e EN)
- Paridade bilíngue
- Siglas com definição
- Imagens com alt text
- Conteúdo solto
- Sumário (TOC)
- Tom consistente
