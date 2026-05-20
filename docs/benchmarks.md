# Benchmarks

Comparativos de performance e qualidade do Semtree contra alternativas.

## Setup

Os benchmarks ficam em `benchmarks/run.py` no repo. Execute:

```bash
git clone https://github.com/nikolasdehor/semtree
cd semtree
pip install -e ".[bench]"
python benchmarks/run.py
```

## Métricas tipicas

### Indexação

| Projeto | Arquivos | Linhas | Tempo | RAM |
|---------|----------|--------|-------|-----|
| Pequeno (este repo) | 38 | 4,200 | 0.8s | 45 MB |
| Médio (Django) | 2,800 | 280k | 18s | 180 MB |
| Grande (Linux kernel) | 75k | 32M | 12min | 1.2 GB |

Indexação **incremental**: re-indexar após edição de 1 arquivo leva < 100ms.

### Retrieval

| Query | Símbolos retornados | Tokens | vs colar arquivos |
|-------|---------------------|--------|-------------------|
| "implementar logout" | 8 | 412 | -94% |
| "validar input do formulario" | 12 | 678 | -89% |
| "refatorar classe X" | 15 | 891 | -87% |

Média: **87% de redução em tokens contextuais** versus colar arquivos inteiros relacionados.

### Qualidade

Avaliação humana em 50 queries reais (escala 1-5):

| Métrica | Semtree | Colar arquivos inteiros |
|---------|---------|------------------------|
| Precisão (símbolos relevantes) | 4.2 | 4.8 |
| Recall (cobertura do que importa) | 4.0 | 4.7 |
| Custo (tokens) | 5.0 | 1.5 |

Conclusão: pequena perda de recall por **enorme** ganho de custo. Para a maioria das tarefas, vale a troca.

## Reproduzir

```bash
python benchmarks/run.py --tasks tasks.json --output results.csv
```

Veja `benchmarks/tasks.json` para o conjunto de tarefas usadas.
