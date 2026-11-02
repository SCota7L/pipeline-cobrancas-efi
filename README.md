# Pipeline de Cobranças Efí + Indicadores BACEN

Pipeline de dados que extrai cobranças (Pix e boleto) da **API da Efí** em ambiente sandbox, cruza com indicadores econômicos do **Banco Central (Selic, CDI, IPCA)**, modela os dados em *star schema* e gera um painel de acompanhamento de cobranças.

> 🚧 Projeto em construção. Acompanhe o progresso pelos commits e pelas issues.

## Problema

Times de tesouraria precisam acompanhar a conversão de cobranças, o prazo médio de recebimento e o custo de oportunidade do dinheiro parado (comparado ao CDI). Este projeto automatiza essa análise de ponta a ponta.

## Arquitetura

```
API Efí (sandbox) ─┐
                   ├─> Python (extração) ─> Postgres [raw] ─> dbt [staging → marts] ─> Power BI
API BACEN (SGS) ───┘            ▲
                                └── orquestrado por Airflow (Docker)
```

## Tecnologias

| Camada | Ferramenta |
|---|---|
| Extração | Python (requests, SDK `efipay`) |
| Armazenamento | PostgreSQL (Docker) · AWS S3 |
| Transformação | dbt |
| Orquestração | Apache Airflow |
| Visualização | Power BI |
| CI/CD | GitHub Actions |

## Modelo de dados (star schema)

- `fato_cobranca`: valor, status, data de criação, data de pagamento
- `dim_cliente`
- `dim_data`
- `dim_meio_pagamento` (Pix, boleto)
- `fato_indicadores`: Selic, CDI, IPCA por data

## Como rodar

```bash
# 1. Copie as variáveis de ambiente e preencha
cp .env.example .env

# 2. Suba o banco
docker compose up -d

# 3. Instale as dependências e extraia os indicadores do BACEN
pip install -r requirements.txt
python src/extrair_bcb.py
```

## Roadmap

- [x] Estrutura inicial
- [ ] Extração BACEN (SGS)
- [ ] Extração Efí (sandbox)
- [ ] Carga no Postgres (camada raw)
- [ ] Modelagem com dbt
- [ ] Orquestração com Airflow
- [ ] Painel Power BI
- [ ] Dados brutos no S3
- [ ] Resumo mensal com IA
- [ ] CI com GitHub Actions

## Autor

**Samuel Gomes Cota**: Engenheiro (UFMG) e Tecnólogo em ADS, atuando em Tesouraria e Finanças.
[LinkedIn](https://www.linkedin.com/in/SEU-PERFIL)
