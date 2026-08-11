# Construction Price Scraper

> **Etapa 1 — Raw Data / Ingestion**

Este repositório representa **exclusivamente a etapa bruta (Raw) de ingestão** do projeto Construction Price Analytics.

O objetivo é realizar a **coleta dos dados de preços de materiais de construção diretamente das fontes**, preservando os dados coletados em seu formato bruto e armazenando-os em **Parquet** no Supabase Storage.

**Este projeto não realiza tratamento analítico, modelagem dimensional, EDA ou criação de dashboards.** Essas etapas serão desenvolvidas em repositórios separados.

---

## 📌 Papel deste repositório na arquitetura

O projeto completo está dividido em diferentes etapas, cada uma com uma responsabilidade específica:

```text
┌──────────────────────────────────────────────┐
│  1. CONSTRUCTION PRICE SCRAPER               │
│                                              │
│  Coleta → Padronização mínima → Raw Storage │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              construction-price-raw
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  2. CONSTRUCTION PRICE EDA                   │
│                                              │
│  Exploração → Qualidade → Distribuições     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  3. CONSTRUCTION PRICE ANALYSIS              │
│                                              │
│  Análises → Métricas → Insights             │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  4. CONSTRUCTION PRICE DASHBOARD             │
│                                              │
│  Visualização → Indicadores → Dashboard     │
└──────────────────────────────────────────────┘
```

### Escopo deste repositório

Este repositório é responsável somente por:

* acessar as fontes de dados;
* realizar as buscas dos produtos;
* extrair os dados;
* aplicar a **padronização mínima necessária para estruturar os registros**;
* remover duplicidades básicas;
* adicionar a data/hora da coleta;
* gerar arquivos Parquet;
* armazenar os dados na camada Raw;
* registrar logs da execução.

### Fora do escopo

Não fazem parte desta etapa:

* tratamento analítico dos dados;
* imputação de valores ausentes;
* análise estatística;
* identificação de outliers;
* criação de métricas;
* modelagem dimensional;
* criação de tabelas analíticas;
* geração de insights;
* dashboards.

Essas responsabilidades pertencem às etapas seguintes do projeto.

---

## 🗂️ Camada Raw

Os dados coletados são armazenados no Supabase Storage como **dados brutos de ingestão**, organizados por fonte:

```text
construction-price
│
├── construction-price-raw/
│   │
│   ├── leroy/
│   │   └── *.parquet
│   │
│   ├── sodimac/
│   │   └── *.parquet
│   │
│   ├── obramax/
│   │   └── *.parquet
│   │
│   └── joli/
│       └── *.parquet
│
└── logs/
    └── *.log
```

A camada Raw tem como objetivo manter uma **cópia confiável dos dados coletados na origem**, permitindo que as etapas posteriores sejam reproduzidas sem a necessidade de realizar novamente o scraping.

### Por que preservar os dados brutos?

A separação entre ingestão e transformação permite:

* reproduzir análises futuras;
* rastrear a origem dos dados;
* identificar problemas na coleta;
* reprocessar os dados sem realizar novo scraping;
* separar responsabilidades entre ingestão e transformação;
* manter histórico das coletas.

---

## 🔄 Fluxo desta etapa

```text
Fonte
  │
  ▼
Scraper
  │
  ▼
Extração
  │
  ▼
Padronização mínima
  │
  ▼
DataFrame
  │
  ▼
Parquet
  │
  ▼
Supabase Storage
  │
  ▼
construction-price-raw/
```

A transformação realizada nesta etapa é **mínima e operacional**. O objetivo não é produzir um dataset analítico, mas garantir que os dados coletados sejam armazenados de forma consistente e utilizável pelas próximas etapas.

---

## 🚫 O que NÃO acontece aqui

É importante destacar que um produto coletado como:

```text
price = 35.90
```

não significa que este repositório irá determinar:

* se o preço é um outlier;
* se o preço está abaixo da média;
* qual loja possui o menor preço;
* qual é a variação percentual;
* qual produto possui melhor custo-benefício;
* qual região possui preços maiores;
* qual tendência de preço existe.

Essas perguntas serão respondidas **nas etapas de EDA e Analysis**.

Este repositório apenas responde:

> **"Quais dados estavam disponíveis na fonte no momento da coleta?"**

---

## 📚 Repositórios relacionados

A arquitetura planejada para o projeto é:

| Etapa | Repositório                    | Responsabilidade       |
| ----- | ------------------------------ | ---------------------- |
| 1     | `construction-price-scraper`   | **Ingestão / Raw**     |
| 2     | `construction-price-eda`       | Exploração e qualidade |
| 3     | `construction-price-analysis`  | Análises e insights    |
| 4     | `construction-price-dashboard` | Visualização           |

Dessa forma, cada repositório possui uma responsabilidade clara dentro do pipeline de dados.
