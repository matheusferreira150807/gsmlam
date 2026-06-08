# -*- coding: utf-8 -*-
"""
Gera o RELATÓRIO TÉCNICO em PDF consolidando tabelas, gráficos e análises.
Lê os números calculados em ../graficos/resultados.json e as imagens dos gráficos.
"""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable)

# -------- Paleta --------
AZUL = colors.HexColor("#0B3D91")
AZUL_CLARO = colors.HexColor("#4C9BE8")
LARANJA = colors.HexColor("#FC3D21")
CINZA = colors.HexColor("#5A6472")
CINZA_CLARO = colors.HexColor("#EEF2F7")
VERDE = colors.HexColor("#2BB673")

G = "../graficos"
with open(f"{G}/resultados.json", encoding="utf-8") as f:
    R = json.load(f)


# -------- Estilos --------
styles = getSampleStyleSheet()
def add(name, **kw):
    styles.add(ParagraphStyle(name, **kw))

add("Capa", fontName="Helvetica-Bold", fontSize=30, leading=36,
    textColor=AZUL, alignment=TA_CENTER)
add("CapaSub", fontName="Helvetica", fontSize=15, leading=20,
    textColor=CINZA, alignment=TA_CENTER)
add("H1", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=AZUL,
    spaceBefore=14, spaceAfter=8)
add("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
    textColor=LARANJA, spaceBefore=10, spaceAfter=5)
add("Corpo", fontName="Helvetica", fontSize=10.5, leading=15.5,
    alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#1A1A1A"))
add("Leg", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
    textColor=CINZA, alignment=TA_CENTER, spaceAfter=10)
add("Cell", fontName="Helvetica", fontSize=8.8, leading=11)
add("CellB", fontName="Helvetica-Bold", fontSize=8.8, leading=11,
    textColor=colors.white)
add("KPInum", fontName="Helvetica-Bold", fontSize=18, leading=20,
    textColor=AZUL, alignment=TA_CENTER)
add("KPItxt", fontName="Helvetica", fontSize=8, leading=10,
    textColor=CINZA, alignment=TA_CENTER)

story = []
def P(t, s="Corpo"): story.append(Paragraph(t, styles[s]))
def SP(h=8): story.append(Spacer(1, h))
def hr(): story.append(HRFlowable(width="100%", thickness=1.2, color=AZUL_CLARO,
                                  spaceBefore=4, spaceAfter=10))


# =================== CAPA ===================
SP(70)
P("RELATÓRIO ESTATÍSTICO", "Capa")
P("A Nova Economia Espacial em Números", "Capa")
SP(16)
P("Análise exploratória de 4.630 missões espaciais (1957–2022)", "CapaSub")
P("aplicada ao apoio à tomada de decisão", "CapaSub")
SP(40)
story.append(HRFlowable(width="55%", thickness=2, color=LARANJA))
SP(28)
P("Global Solution &mdash; Modelagem Linear para Aprendizagem de Máquina", "CapaSub")
P("Ciência da Computação | Turma 1CC", "CapaSub")
SP(50)
P("Documento técnico preparado para o cliente / tomador de decisão", "Leg")
P("Fonte dos dados: Next Spaceflight / Maven Analytics", "Leg")
story.append(PageBreak())


# =================== SUMÁRIO EXECUTIVO ===================
P("Sumário Executivo", "H1"); hr()
P("Este relatório transforma uma base real de lançamentos espaciais em "
  "informação acionável para o contexto da <b>nova economia espacial</b>. "
  "Foram analisadas <b>4.630 missões</b> realizadas entre <b>1957 e 2022</b>, "
  "com foco em duas dimensões críticas para qualquer plano de negócios no setor: "
  "o <b>custo dos foguetes</b> e o <b>volume de lançamentos ao longo do tempo</b>.")
P("As principais descobertas indicam um mercado em forte reaquecimento: após o "
  "auge da Corrida Espacial e o arrefecimento nas décadas de 1980–2010, o número "
  "de lançamentos atingiu o <b>recorde histórico de 157 em 2021</b>. No campo de "
  "custos, a distribuição é fortemente assimétrica &mdash; a maioria das missões "
  "custa menos de US$ 100 milhões (mediana de US$ 63,2 mi), enquanto poucos "
  "programas de altíssimo orçamento elevam a média para US$ 128,3 mi.")

# KPIs
kpi = [[Paragraph("4.630", styles["KPInum"]),
        Paragraph("70/ano", styles["KPInum"]),
        Paragraph("US$ 63,2 mi", styles["KPInum"]),
        Paragraph("89,9%", styles["KPInum"])],
       [Paragraph("missões analisadas", styles["KPItxt"]),
        Paragraph("média de lançamentos", styles["KPItxt"]),
        Paragraph("custo mediano por foguete", styles["KPItxt"]),
        Paragraph("taxa de sucesso das missões", styles["KPItxt"])]]
t = Table(kpi, colWidths=[4.1*cm]*4)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), CINZA_CLARO),
    ("BOX", (0,0), (-1,-1), 0.5, colors.white),
    ("INNERGRID", (0,0), (-1,-1), 4, colors.white),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,0), 10),
    ("BOTTOMPADDING", (0,-1), (-1,-1), 10),
]))
SP(4); story.append(t)
story.append(PageBreak())


# =================== 1) BASE DE DADOS ===================
P("1. Seleção e Justificativa da Base de Dados", "H1"); hr()
P("<b>Base escolhida:</b> <i>Space Missions (1957–2022)</i>, compilada a partir "
  "do portal Next Spaceflight e disponibilizada publicamente (Maven Analytics / "
  "Kaggle). Trata-se de dados <b>reais</b> &mdash; não simulados &mdash; cobrindo "
  "praticamente todo o histórico da atividade espacial mundial.")
P("<b>Justificativa técnica:</b>", "H2")
just = [
    ("Relevância e aderência ao tema", "Registra diretamente a atividade da "
     "economia espacial (organizações, foguetes, custos e resultados), núcleo do "
     "desafio proposto no Global Solution."),
    ("Volume e período", "4.630 registros cobrindo 66 anos (1957–2022), "
     "permitindo análise temporal robusta e identificação de tendências."),
    ("Qualidade e estrutura", "Dados tabulares organizados em 9 campos originais, "
     "com tipos bem definidos (datas, valores monetários e categorias) e "
     "rastreabilidade da fonte."),
    ("Potencial analítico", "Contém variáveis quantitativas discretas (ano), "
     "contínuas (custo) e categóricas (organização, país, status), viabilizando "
     "todas as análises exigidas."),
]
data = [[Paragraph(f"<b>{a}</b>", styles["Cell"]), Paragraph(b, styles["Cell"])]
        for a, b in just]
t = Table(data, colWidths=[5*cm, 11.4*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), CINZA_CLARO),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D6DEE8")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(t)
SP(8)
P("<b>Dicionário (campos utilizados):</b> Company (organização responsável), "
  "Location (local de lançamento), Date (data), Rocket (foguete), "
  "Price &rarr; <b>Custo</b> (US$ milhões), RocketStatus (ativo/aposentado) e "
  "MissionStatus (sucesso/falha). Foram derivadas as variáveis <b>Ano</b> (a "
  "partir da data) e <b>País</b> (a partir do local).")
P("<b>Tratamento dos dados:</b> conversão de datas e extração do ano; conversão "
  "do custo para valor numérico (remoção de separadores de milhar); o custo está "
  "disponível para 1.265 missões &mdash; subconjunto usado nas análises monetárias. "
  "Todo o tratamento é reprodutível pelo código-fonte Python que acompanha o projeto.")
story.append(PageBreak())


# =================== 2) TABELAS DE FREQUÊNCIA ===================
P("2. Tabelas de Distribuição de Frequências", "H1"); hr()

# ---- 2.1 discreta ----
P("2.1 Variável quantitativa discreta &mdash; Lançamentos por ano", "H2")
P("A tabela abaixo (extrato; tabela completa de 66 anos no repositório) distribui "
  "as frequências de lançamentos por ano. <i>fi</i> = frequência absoluta; "
  "<i>fr%</i> = relativa; <i>Fi</i> e <i>Fr%</i> = acumuladas.")

disc = R["fdt_discreta_amostra"]
header = ["Ano", "fi", "fr %", "Fi", "Fr %"]
rows = [[Paragraph(h, styles["CellB"]) for h in header]]
for d in disc:
    rows.append([str(d["Ano"]), str(d["fi"]), f'{d["fr_%"]:.2f}',
                 str(d["Fi"]), f'{d["Fr_%"]:.2f}'])
rows.append(["...", "...", "...", "...", "..."])
rows.append(["Total (66 anos)", "4.630", "100,00", "—", "100,00"])
t = Table(rows, colWidths=[3.3*cm]+[2.6*cm]*4)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AZUL),
    ("ROWBACKGROUNDS", (0,1), (-1,-3), [colors.white, CINZA_CLARO]),
    ("BACKGROUND", (0,-1), (-1,-1), AZUL_CLARO),
    ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D6DEE8")),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("FONTSIZE", (0,0), (-1,-1), 8.8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(t)
P("Tabela 1. Distribuição de frequências do nº de lançamentos por ano (extrato).", "Leg")

# ---- 2.2 contínua ----
P("2.2 Variável quantitativa contínua &mdash; Custo do foguete (US$ milhões)", "H2")
P("Para a variável contínua, a Regra de Sturges indicou k &asymp; 11 classes; dada "
  "a forte assimetria (custos de US$ 2,5 mi a US$ 5 bi), adotaram-se classes de "
  "amplitude crescente economicamente interpretáveis, preservando a leitura "
  "estatística (n = 1.265 missões com custo informado).")

cont = R["fdt_continua"]
header = ["Classe (US$ mi)", "Ponto médio", "fi", "fr %", "Fi", "Fr %"]
rows = [[Paragraph(h, styles["CellB"]) for h in header]]
for c in cont:
    rows.append([c["Classe (US$ mi)"], f'{c["Ponto médio"]:.1f}', str(c["fi"]),
                 f'{c["fr_%"]:.2f}', str(c["Fi"]), f'{c["Fr_%"]:.2f}'])
rows.append(["Total", "—", "1.265", "100,00", "—", "100,00"])
t = Table(rows, colWidths=[3.5*cm, 2.6*cm, 2*cm, 2.2*cm, 2*cm, 2.2*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AZUL),
    ("ROWBACKGROUNDS", (0,1), (-1,-2), [colors.white, CINZA_CLARO]),
    ("BACKGROUND", (0,-1), (-1,-1), AZUL_CLARO),
    ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D6DEE8")),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("FONTSIZE", (0,0), (-1,-1), 8.8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(t)
P("Tabela 2. Distribuição de frequências do custo dos foguetes (US$ milhões).", "Leg")
P("<b>Leitura:</b> cerca de <b>70%</b> das missões com custo informado situam-se "
  "abaixo de US$ 100 milhões (Fr% acumulada na 3ª classe), e <b>98,8%</b> abaixo "
  "de US$ 500 milhões. Apenas 15 missões (1,2%) ultrapassam US$ 1 bilhão, "
  "confirmando a presença de poucos programas de orçamento excepcional.")
story.append(PageBreak())


# =================== 3) GRÁFICOS ===================
P("3. Gráficos Estatísticos", "H1"); hr()

P("3.1 Distribuição do custo dos foguetes (variável contínua)", "H2")
story.append(Image(f"{G}/g1_histograma_custo.png", width=16.5*cm, height=7.15*cm))
P("Figura 1. Histograma do custo dos foguetes. O painel (b) evidencia a "
  "concentração da maioria dos lançamentos abaixo de US$ 100 mi e a assimetria à "
  "direita (média > mediana).", "Leg")

P("3.2 Evolução dos lançamentos por ano (variável temporal)", "H2")
story.append(Image(f"{G}/g2_lancamentos_por_ano.png", width=15.5*cm, height=8.5*cm))
P("Figura 2. Série histórica do número de lançamentos por ano (1957–2022), com "
  "média de referência e destaque para o pico recorde de 2021.", "Leg")
story.append(PageBreak())

P("3.3 Principais organizações (variável categórica)", "H2")
story.append(Image(f"{G}/g3_top_organizacoes.png", width=15.5*cm, height=8.7*cm))
P("Figura 3. Top 10 organizações por número de lançamentos. SpaceX (destaque) "
  "consolidou-se entre as maiores apesar de fundada apenas em 2002.", "Leg")

P("3.4 Resultado das missões (variável categórica)", "H2")
story.append(Image(f"{G}/g4_status_missoes.png", width=11.5*cm, height=8.1*cm))
P("Figura 4. Distribuição do status das missões: a taxa de sucesso de 89,9% "
  "indica maturidade tecnológica do setor.", "Leg")
story.append(PageBreak())


# =================== 4) ANÁLISES UNIVARIADAS ===================
P("4. Análises Univariadas (Estatística Descritiva)", "H1"); hr()

def tabela_medidas(m):
    linhas = [
        ("Tendência central", "Média", f'{m["media"]:.2f}'),
        ("", "Mediana", f'{m["mediana"]:.2f}'),
        ("", "Moda", ", ".join(f'{x:.2f}' for x in m["moda"])),
        ("Dispersão", "Valor máximo", f'{m["maximo"]:.2f}'),
        ("", "Valor mínimo", f'{m["minimo"]:.2f}'),
        ("", "Amplitude", f'{m["amplitude"]:.2f}'),
        ("", "Variância", f'{m["variancia"]:.2f}'),
        ("", "Desvio padrão", f'{m["desvio_padrao"]:.2f}'),
        ("", "Coef. de variação", f'{m["coef_variacao_%"]:.2f}%'),
        ("Separatrizes", "Q1 (25%)", f'{m["Q1"]:.2f}'),
        ("", "Q2 (50% = mediana)", f'{m["Q2"]:.2f}'),
        ("", "Q3 (75%)", f'{m["Q3"]:.2f}'),
        ("", "IQR (Q3 - Q1)", f'{m["IQR"]:.2f}'),
    ]
    rows = [[Paragraph(h, styles["CellB"]) for h in ["Grupo", "Medida", "Valor"]]]
    for g, med, val in linhas:
        rows.append([g, med, val])
    t = Table(rows, colWidths=[4.2*cm, 6.2*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D6DEE8")),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (2,0), (2,-1), "CENTER"),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), LARANJA),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, CINZA_CLARO]),
        ("SPAN", (0,1), (0,3)), ("SPAN", (0,4), (0,9)), ("SPAN", (0,10), (0,13)),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return t

# 4.1 Custo
mc = R["univ_custo"]
P("4.1 Análise univariada — Custo do foguete (US$ milhões, n = 1.265)", "H2")
story.append(tabela_medidas(mc))
P("Tabela 3. Medidas descritivas do custo do foguete.", "Leg")
P("<b>Interpretação:</b> a média (US$ 128,3 mi) é mais que o dobro da mediana "
  "(US$ 63,2 mi), o que confirma uma distribuição <b>assimétrica à direita</b>: "
  "poucos programas de altíssimo custo (até US$ 5 bi) puxam a média para cima. "
  "Por isso, a <b>mediana</b> é o indicador mais representativo do custo típico de "
  "um lançamento. O <b>coeficiente de variação de 200%</b> revela dispersão "
  "altíssima &mdash; o setor abriga desde pequenos lançadores até megaprogramas. "
  "Metade central das missões (entre Q1 = US$ 30 mi e Q3 = US$ 115 mi) está "
  "contida numa faixa de US$ 85 mi (IQR), reforçando que o mercado economicamente "
  "acessível concentra-se abaixo da casa dos US$ 100 milhões.")
story.append(PageBreak())

# 4.2 Lançamentos por ano
ml = R["univ_lpa"]
P("4.2 Análise univariada — Lançamentos por ano (n = 66 anos)", "H2")
story.append(tabela_medidas(ml))
P("Tabela 4. Medidas descritivas do número de lançamentos por ano.", "Leg")
P("<b>Interpretação:</b> em média, o mundo realizou <b>70 lançamentos por ano</b> "
  "no período, com mediana de 61,5 &mdash; média e mediana próximas indicam "
  "distribuição razoavelmente simétrica. A amplitude é enorme (de apenas 3 "
  "lançamentos em 1957 a 157 em 2021), e o desvio padrão de 29,2 (CV de 41,6%) "
  "mostra variação relevante entre os anos, reflexo dos ciclos geopolíticos e "
  "tecnológicos do setor. Os quartis revelam que em 25% dos anos houve até 50 "
  "lançamentos (Q1) e em 25% houve 96 ou mais (Q3); a aproximação do volume atual "
  "ao limite superior histórico evidencia o atual ciclo de expansão.")
story.append(PageBreak())


# =================== 5) CONCLUSÕES ===================
P("5. Conclusões, Insights e Recomendações", "H1"); hr()
P("A análise estatística de mais de seis décadas de atividade espacial revela um "
  "setor em transformação acelerada, com implicações diretas para decisões de "
  "investimento e posicionamento de mercado:")

insights = [
    ("Mercado em forte expansão", "Após décadas de estabilidade em torno de 60–70 "
     "lançamentos anuais, o volume disparou recentemente, atingindo o recorde de "
     "157 em 2021. A nova economia espacial está claramente em ciclo ascendente."),
    ("Custo típico acessível", "A mediana de US$ 63,2 mi (e 70% das missões abaixo "
     "de US$ 100 mi) mostra que o lançamento deixou de ser exclusividade de "
     "megaprogramas, abrindo espaço para novos entrantes comerciais."),
    ("Alta dispersão de custos", "Com coeficiente de variação de 200%, o setor "
     "comporta modelos de negócio muito distintos; análises de custo devem usar a "
     "mediana, não a média, para evitar distorção pelos outliers bilionários."),
    ("Maturidade e confiabilidade", "A taxa de sucesso de 89,9% (e ~95% somando "
     "sucessos parciais) sinaliza tecnologia madura, reduzindo o risco percebido "
     "para investidores e seguradoras."),
    ("Reconfiguração de protagonistas", "O domínio histórico de agências estatais "
     "(RVSN USSR à frente) convive com a ascensão de players comerciais como a "
     "SpaceX, que em ~20 anos entrou no top 10 mundial de lançamentos."),
]
for titulo, texto in insights:
    P(f"<b>&#9679; {titulo}.</b> {texto}")

SP(6)
P("Recomendações ao cliente", "H2")
P("1) Priorizar oportunidades na faixa de custo até US$ 100 mi, onde se concentra "
  "a maior parte do mercado e o crescimento de demanda. "
  "2) Adotar a mediana e os quartis como referência de custo em estudos de "
  "viabilidade, dada a forte assimetria. "
  "3) Monitorar a tendência de crescimento pós-2015 como janela estratégica de "
  "entrada. "
  "4) Considerar a elevada taxa de sucesso como fator favorável na modelagem de "
  "risco de novos empreendimentos.")
SP(10); hr()
P("<b>Limitações:</b> a variável custo está disponível para 1.265 das 4.630 "
  "missões; valores ausentes podem introduzir viés de seleção (programas mais "
  "recentes/comerciais tendem a divulgar custos). Recomenda-se, em etapas futuras, "
  "complementar a base e aplicar modelos preditivos (regressão) para estimar custos "
  "e projetar a demanda de lançamentos.", "Leg")
P("Metodologia e reprodutibilidade: todos os cálculos e gráficos deste relatório "
  "foram gerados em Python (pandas, numpy, matplotlib); o código-fonte e a base "
  "acompanham o projeto no repositório.", "Leg")


# =================== RODAPÉ COM PAGINAÇÃO ===================
def rodape(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(AZUL_CLARO)
    canvas.setLineWidth(0.8)
    canvas.line(2*cm, 1.4*cm, A4[0]-2*cm, 1.4*cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(CINZA)
    canvas.drawString(2*cm, 1.0*cm,
                      "Global Solution · Modelagem Linear para Aprendizagem de Máquina · 1CC")
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, f"Página {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate("../relatorio/Relatorio_Estatistico_Economia_Espacial.pdf",
                        pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2*cm, rightMargin=2*cm,
                        title="Relatório Estatístico - Nova Economia Espacial",
                        author="Grupo GS - 1CC")
doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=rodape)
print("PDF gerado com sucesso.")
