# Análise Estatística da Nova Economia Espacial

**Global Solution — Modelagem Linear para Aprendizagem de Máquina**
Ciência da Computação | Turma 1CC

> Transformação de uma base **real** de 4.630 missões espaciais (1957–2022) em
> informação útil para apoio à tomada de decisão na nova economia espacial,
> utilizando Python, estatística descritiva e visualização de dados.

---

## Integrantes

| Nome completo | Matrícula |
|---------------|-----------|
| _Matheus Caviglia Ferreira_ | _[569638]_ |
| _Gustavo Henrique Pereira Correia_ | _[569921]_ |

---

## Descrição da solução

Este projeto realiza uma **análise exploratória e descritiva** de dados reais de
lançamentos espaciais para responder a duas perguntas estratégicas do setor:

1. **Quanto custa**, tipicamente, colocar uma missão no espaço?
2. **Como evoluiu** o volume de lançamentos ao longo das décadas?

A partir dessas perguntas, o trabalho cobre integralmente os itens do briefing:
seleção e justificativa da base, tabelas de distribuição de frequências (variável
discreta e contínua), gráficos estatísticos, análises univariadas completas
(tendência central, dispersão e separatrizes) e um relatório técnico consolidado,
estruturado como material para um cliente/tomador de decisão.

### Principais resultados
-  **Mercado em expansão:** recorde histórico de **157 lançamentos em 2021**.
-  **Custo mediano de US$ 63,2 mi** por foguete; **70%** das missões custam < US$ 100 mi.
-  **Distribuição de custos fortemente assimétrica** (CV de 200%) — média (US$ 128,3 mi) puxada por outliers de até US$ 5 bi.
-  **Taxa de sucesso de 89,9%**, indicando maturidade tecnológica do setor.

---

---

## Fonte e descrição da base de dados

- **Base:** *Space Missions (1957–2022)*
- **Origem:** dados extraídos do portal [Next Spaceflight](https://nextspaceflight.com/), disponibilizados via Maven Analytics / Kaggle.
- **Dimensão:** 4.630 registros × 9 campos originais.

| Campo | Descrição |
|-------|-----------|
| Company | Organização responsável pela missão |
| Location | Local de lançamento |
| Date / Time | Data e hora do lançamento |
| Rocket | Nome do foguete |
| Mission | Nome da missão |
| RocketStatus | Status do foguete (Active / Retired) |
| **Price → Custo** | Custo do foguete (US$ milhões) |
| MissionStatus | Resultado (Success / Failure / Partial / Prelaunch Failure) |

Variáveis derivadas: **Ano** (a partir de `Date`) e **País** (a partir de `Location`).

---

## Como executar

Requisitos: Python 3.9+.

```bash
# 1. Instalar dependências
pip install pandas numpy matplotlib reportlab

# 2. Rodar a análise (gera gráficos, tabelas e resultados.json em /graficos)
cd codigo
python analise_economia_espacial.py

# 3. Gerar o relatório técnico em PDF (em /relatorio)
python gerar_relatorio.py
```

Alternativamente, abra `codigo/analise_economia_espacial.ipynb` no Jupyter e
execute as células em ordem.

---

##  Tecnologias

Python · pandas · NumPy · Matplotlib · ReportLab · Jupyter

---


