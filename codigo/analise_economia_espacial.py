# -*- coding: utf-8 -*-
"""
============================================================================
GLOBAL SOLUTION - Modelagem Linear para Aprendizagem de Máquina
ANÁLISE ESTATÍSTICA DA NOVA ECONOMIA ESPACIAL
============================================================================
Base de dados: Space Missions (1957-2022) - nextspaceflight.com / Maven Analytics
Objetivo: Transformar dados reais de lançamentos espaciais em informação útil
          para apoio à tomada de decisão na nova economia espacial.

Conteúdo deste script:
  01) Carga e tratamento da base real
  02) Tabelas de Distribuição de Frequências (discreta e contínua)
  03) Gráficos estatísticos
  04) Análises univariadas (tendência central, dispersão, separatrizes)

Autor(es): [PREENCHER NOME(S) E MATRÍCULA(S) DO GRUPO]
============================================================================
"""

import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend não interativo (gera arquivos de imagem)
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------------------------
# Configurações visuais globais dos gráficos
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Paleta de cores (tema "espacial")
AZUL_PROFUNDO = "#0B3D91"   # azul NASA
LARANJA       = "#FC3D21"   # vermelho/laranja foguete
AZUL_CLARO    = "#4C9BE8"
CINZA         = "#5A6472"
VERDE         = "#2BB673"

PASTA_GRAFICOS = "../graficos"   # ajuste o caminho se executar de outro diretório
CAMINHO_BASE   = "../dados/space_missions.csv"

resultados = {}  # dicionário para exportar os números do relatório


# ===========================================================================
# 01) CARGA E TRATAMENTO DA BASE
# ===========================================================================
def carregar_dados(caminho=CAMINHO_BASE):
    """Lê a base real e cria as variáveis de análise."""
    df = pd.read_csv(caminho, encoding="utf-8")

    # Conversão de data e extração do ano (variável quantitativa DISCRETA)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Ano"] = df["Date"].dt.year

    # Conversão do custo do foguete (variável quantitativa CONTÍNUA)
    # Remove separador de milhar e converte para número (em milhões de USD)
    df["Custo"] = pd.to_numeric(
        df["Price"].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

    # País de lançamento (categórica auxiliar, extraída do final do endereço)
    df["Pais"] = df["Location"].str.split(", ").str[-1].str.strip()

    return df


# ===========================================================================
# 02) TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS
# ===========================================================================
def tabela_freq_discreta(serie):
    """
    Tabela de distribuição de frequências para variável quantitativa DISCRETA.
    Variável: Ano de lançamento.
    Colunas: fi (freq. absoluta), fr (relativa), fr% , Fi (acumulada), Fr% (acum.)
    """
    serie = serie.dropna().astype(int)
    contagem = serie.value_counts().sort_index()
    n = contagem.sum()

    tab = pd.DataFrame({"Ano": contagem.index, "fi": contagem.values})
    tab["fr"] = tab["fi"] / n
    tab["fr_%"] = (tab["fr"] * 100).round(2)
    tab["Fi"] = tab["fi"].cumsum()
    tab["Fr_%"] = (tab["Fi"] / n * 100).round(2)
    return tab, n


def tabela_freq_continua(serie, limites=None):
    """
    Tabela de distribuição de frequências para variável quantitativa CONTÍNUA.
    Variável: Custo do foguete (milhões de USD).

    O número de classes foi orientado pela Regra de Sturges
    (k = 1 + 3.322*log10(n)). Como a variável é fortemente assimétrica à
    direita (presença de outliers de até US$ 5 bilhões), adotam-se classes
    de amplitude crescente, economicamente interpretáveis — prática usual
    quando há grande dispersão — preservando a leitura estatística.
    """
    serie = serie.dropna()
    n = len(serie)
    k_sturges = int(round(1 + 3.322 * np.log10(n)))  # referência de nº de classes

    if limites is None:
        # Faixas de custo significativas para o setor (US$ milhões)
        limites = [0, 25, 50, 100, 200, 500, 1000, serie.max()]

    rotulos, fis, pontos_medios = [], [], []
    for i in range(len(limites) - 1):
        li, ls = limites[i], limites[i + 1]
        if i < len(limites) - 2:
            mask = (serie >= li) & (serie < ls)
            rot = f"[{li:.0f} ; {ls:.0f})"
        else:  # última classe fechada à direita
            mask = (serie >= li) & (serie <= ls)
            rot = f"[{li:.0f} ; {ls:.0f}]"
        rotulos.append(rot)
        fis.append(int(mask.sum()))
        pontos_medios.append(round((li + ls) / 2, 1))

    tab = pd.DataFrame({"Classe (US$ mi)": rotulos,
                        "Ponto médio": pontos_medios,
                        "fi": fis})
    tab["fr_%"] = (tab["fi"] / n * 100).round(2)
    tab["Fi"] = tab["fi"].cumsum()
    tab["Fr_%"] = (tab["Fi"] / n * 100).round(2)
    return tab, n, k_sturges, len(rotulos)


# ===========================================================================
# 04) ANÁLISE UNIVARIADA (medidas descritivas)
# ===========================================================================
def analise_univariada(serie, nome, unidade=""):
    """Calcula todas as medidas exigidas para uma variável quantitativa."""
    s = serie.dropna().astype(float)

    medidas = {
        "variavel": nome,
        "unidade": unidade,
        "n": int(s.count()),
        # Tendência central
        "media": float(s.mean()),
        "mediana": float(s.median()),
        "moda": [float(m) for m in s.mode().tolist()],
        # Dispersão
        "maximo": float(s.max()),
        "minimo": float(s.min()),
        "amplitude": float(s.max() - s.min()),
        "variancia": float(s.var(ddof=1)),       # variância amostral
        "desvio_padrao": float(s.std(ddof=1)),   # desvio padrão amostral
        "coef_variacao_%": float(s.std(ddof=1) / s.mean() * 100),
        # Separatrizes
        "Q1": float(s.quantile(0.25)),
        "Q2": float(s.quantile(0.50)),
        "Q3": float(s.quantile(0.75)),
        "IQR": float(s.quantile(0.75) - s.quantile(0.25)),
    }
    return medidas


def imprime_univariada(m):
    print(f"\n{'='*60}\nANÁLISE UNIVARIADA: {m['variavel']} ({m['unidade']})\n{'='*60}")
    print(f"n (observações)......: {m['n']}")
    print("-- Tendência Central --")
    print(f"Média................: {m['media']:.2f}")
    print(f"Mediana..............: {m['mediana']:.2f}")
    print(f"Moda.................: {', '.join(f'{x:.2f}' for x in m['moda'])}")
    print("-- Dispersão --")
    print(f"Valor máximo.........: {m['maximo']:.2f}")
    print(f"Valor mínimo.........: {m['minimo']:.2f}")
    print(f"Amplitude............: {m['amplitude']:.2f}")
    print(f"Variância............: {m['variancia']:.2f}")
    print(f"Desvio padrão........: {m['desvio_padrao']:.2f}")
    print(f"Coef. de variação....: {m['coef_variacao_%']:.2f}%")
    print("-- Separatrizes --")
    print(f"Q1 (25%).............: {m['Q1']:.2f}")
    print(f"Q2 (50% = mediana)...: {m['Q2']:.2f}")
    print(f"Q3 (75%).............: {m['Q3']:.2f}")
    print(f"IQR (Q3-Q1)..........: {m['IQR']:.2f}")


# ===========================================================================
# 03) GRÁFICOS ESTATÍSTICOS
# ===========================================================================
def grafico_histograma_custo(df):
    """Gráfico 1 - Histograma da variável CONTÍNUA (custo do foguete).
    Dois painéis: visão completa (mostra outliers) e zoom na faixa principal
    (até US$ 500 mi), onde se concentra ~99% dos lançamentos."""
    custo = df["Custo"].dropna()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

    # Painel A: visão completa
    ax1.hist(custo, bins=25, color=AZUL_PROFUNDO, edgecolor="white", alpha=0.9)
    ax1.set_title("(a) Visão completa")
    ax1.set_xlabel("Custo do foguete (milhões de US$)")
    ax1.set_ylabel("Frequência (nº de lançamentos)")

    # Painel B: zoom na faixa principal (<= 500 mi)
    foco = custo[custo <= 500]
    ax2.hist(foco, bins=20, color=AZUL_CLARO, edgecolor="white", alpha=0.95)
    ax2.axvline(custo.mean(), color=LARANJA, linestyle="--", linewidth=2,
                label=f"Média = US$ {custo.mean():.1f} mi")
    ax2.axvline(custo.median(), color=VERDE, linestyle="-.", linewidth=2,
                label=f"Mediana = US$ {custo.median():.1f} mi")
    ax2.set_title("(b) Zoom: custos até US$ 500 mi (~99% dos dados)")
    ax2.set_xlabel("Custo do foguete (milhões de US$)")
    ax2.set_ylabel("Frequência (nº de lançamentos)")
    ax2.legend()

    fig.suptitle("Distribuição do Custo dos Foguetes (1957–2022)",
                 fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(f"{PASTA_GRAFICOS}/g1_histograma_custo.png", bbox_inches="tight")
    plt.close(fig)


def grafico_lancamentos_por_ano(df):
    """Gráfico 2 - Série temporal: nº de lançamentos por ano (variável diferente)."""
    lpa = df.groupby("Ano").size()
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(lpa.index, lpa.values, color=AZUL_PROFUNDO, linewidth=2.2,
            marker="o", markersize=3, label="Lançamentos/ano")
    ax.fill_between(lpa.index, lpa.values, color=AZUL_CLARO, alpha=0.25)
    ax.axhline(lpa.mean(), color=LARANJA, linestyle="--", linewidth=1.8,
               label=f"Média = {lpa.mean():.0f}/ano")
    ax.annotate(f"Pico: {lpa.max()} ({lpa.idxmax()})",
                xy=(lpa.idxmax(), lpa.max()),
                xytext=(lpa.idxmax()-22, lpa.max()-12),
                arrowprops=dict(arrowstyle="->", color=CINZA))
    ax.set_title("Evolução do Número de Lançamentos Espaciais por Ano")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Número de lançamentos")
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{PASTA_GRAFICOS}/g2_lancamentos_por_ano.png", bbox_inches="tight")
    plt.close(fig)


def grafico_top_organizacoes(df):
    """Gráfico extra - Top 10 organizações por nº de lançamentos (categórica)."""
    top = df["Company"].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5.2))
    cores = [LARANJA if c == "SpaceX" else AZUL_PROFUNDO for c in top.index]
    ax.barh(top.index, top.values, color=cores, edgecolor="white")
    for i, (nome, val) in enumerate(top.items()):
        ax.text(val + 8, i, str(val), va="center", fontsize=9, color=CINZA)
    ax.set_title("Top 10 Organizações por Número de Lançamentos (1957–2022)")
    ax.set_xlabel("Número de lançamentos")
    ax.set_ylabel("Organização")
    fig.tight_layout()
    fig.savefig(f"{PASTA_GRAFICOS}/g3_top_organizacoes.png", bbox_inches="tight")
    plt.close(fig)


def grafico_status_missoes(df):
    """Gráfico extra - Status das missões (categórica)."""
    status = df["MissionStatus"].value_counts()
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    cores = [VERDE, LARANJA, "#F2A900", CINZA]
    wedges, _, autotexts = ax.pie(
        status.values, labels=None,
        autopct=lambda p: f"{p:.1f}%" if p > 4 else "",
        colors=cores[:len(status)], startangle=90, pctdistance=0.78,
        wedgeprops=dict(width=0.42, edgecolor="white"))
    for t in autotexts:
        t.set_color("white"); t.set_fontweight("bold"); t.set_fontsize(9)
    ax.legend(wedges, [f"{k} ({v})" for k, v in status.items()],
              title="Status da missão", loc="center left",
              bbox_to_anchor=(1, 0.5))
    ax.set_title("Status das Missões Espaciais (1957–2022)")
    fig.tight_layout()
    fig.savefig(f"{PASTA_GRAFICOS}/g4_status_missoes.png", bbox_inches="tight")
    plt.close(fig)


# ===========================================================================
# EXECUÇÃO PRINCIPAL
# ===========================================================================
def main():
    print("Carregando base real de missões espaciais...")
    df = carregar_dados()
    print(f"Base carregada: {df.shape[0]} registros, {df.shape[1]} colunas.")
    print(f"Período: {int(df['Ano'].min())} a {int(df['Ano'].max())}")
    resultados["n_registros"] = int(df.shape[0])
    resultados["periodo"] = [int(df["Ano"].min()), int(df["Ano"].max())]
    resultados["n_com_custo"] = int(df["Custo"].notna().sum())

    # ---- 02) Tabelas de frequência ----
    print("\n" + "#"*70 + "\n# 02) TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS\n" + "#"*70)

    tab_disc, n_disc = tabela_freq_discreta(df["Ano"])
    print("\n>> DISCRETA - Lançamentos por ano (amostra das 8 primeiras linhas):")
    print(tab_disc.head(8).to_string(index=False))
    tab_disc.to_csv(f"{PASTA_GRAFICOS}/tabela_freq_discreta.csv", index=False)

    tab_cont, n_cont, k_sturges, k_usado = tabela_freq_continua(df["Custo"])
    print(f"\n>> CONTÍNUA - Custo do foguete  (n={n_cont}, "
          f"Sturges sugere k={k_sturges}; classes interpretáveis usadas={k_usado}):")
    print(tab_cont.to_string(index=False))
    tab_cont.to_csv(f"{PASTA_GRAFICOS}/tabela_freq_continua.csv", index=False)

    resultados["fdt_continua"] = tab_cont.to_dict(orient="records")
    resultados["fdt_continua_meta"] = {"n": int(n_cont), "k_sturges": int(k_sturges),
                                       "k_usado": int(k_usado)}
    resultados["fdt_discreta_amostra"] = tab_disc.head(10).to_dict(orient="records")

    # ---- 03) Gráficos ----
    print("\n" + "#"*70 + "\n# 03) GERANDO GRÁFICOS\n" + "#"*70)
    grafico_histograma_custo(df)
    grafico_lancamentos_por_ano(df)
    grafico_top_organizacoes(df)
    grafico_status_missoes(df)
    print("Gráficos salvos na pasta 'graficos/'.")

    # ---- 04) Análises univariadas ----
    print("\n" + "#"*70 + "\n# 04) ANÁLISES UNIVARIADAS\n" + "#"*70)

    m_custo = analise_univariada(df["Custo"], "Custo do foguete", "milhões de US$")
    imprime_univariada(m_custo)

    lpa = df.groupby("Ano").size()
    m_lpa = analise_univariada(lpa, "Lançamentos por ano", "lançamentos/ano")
    imprime_univariada(m_lpa)

    resultados["univ_custo"] = m_custo
    resultados["univ_lpa"] = m_lpa

    # Exporta números para o relatório
    with open(f"{PASTA_GRAFICOS}/resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print("\nResultados numéricos exportados para 'graficos/resultados.json'.")
    print("\nProcessamento concluído com sucesso.")


if __name__ == "__main__":
    main()
