
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================

st.set_page_config(
    page_title="Desigualdade de Gênero | São Paulo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent.parent

ARQUIVO_DADOS = BASE / "dados" / "dados_tratados.csv"
ARQUIVO_MODELO = BASE / "modelos" / "modelo_rendimento.joblib"
ARQUIVO_METRICAS = BASE / "modelos" / "metricas_modelo.json"

CORES = {
    "Homens": "#475569",
    "Mulheres": "#9575CD",
}

ORDEM_IDADE = [
    "14 a 24",
    "25 a 34",
    "35 a 44",
    "45 a 54",
    "55 a 64",
    "65 ou mais",
]

ORDEM_ESCOLARIDADE = [
    "Sem instrução/menos de 1 ano",
    "Fundamental incompleto",
    "Fundamental completo",
    "Médio incompleto",
    "Médio completo",
    "Superior incompleto",
    "Superior completo",
]

COLUNAS_OBRIGATORIAS = [
    "Genero",
    "Ocupado",
    "Rendimento",
    "Peso",
    "Escolaridade",
    "Faixa_Etaria",
    "Setor",
]


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    [data-testid="stMetric"] {
        background-color: rgba(148, 163, 184, 0.06);
        padding: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def moeda(valor):
    if pd.isna(valor):
        return "Não disponível"

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def numero(valor):
    return f"{valor:,.0f}".replace(",", ".")


def percentual(valor):
    if pd.isna(valor):
        return "Não disponível"

    return f"{valor:.2f}%".replace(".", ",")


def media_ponderada(df, coluna):
    if df.empty:
        return np.nan

    base = df.dropna(subset=[coluna, "Peso"]).copy()
    base = base[base["Peso"] > 0]

    if base.empty:
        return np.nan

    return float(
        np.average(
            base[coluna],
            weights=base["Peso"],
        )
    )


def total_ponderado(df):
    if df.empty:
        return 0.0

    return float(df["Peso"].sum())


def participacao_feminina(df):
    total = total_ponderado(df)

    if total <= 0:
        return np.nan

    mulheres = total_ponderado(
        df[df["Genero"] == "Mulheres"]
    )

    return 100 * mulheres / total


def rendimento_por_genero(df):
    resultados = []

    validos = df[
        (df["Rendimento"] > 0)
        & (df["Peso"] > 0)
    ]

    for genero in ["Homens", "Mulheres"]:
        grupo = validos[validos["Genero"] == genero]

        resultados.append(
            {
                "Genero": genero,
                "Rendimento médio": media_ponderada(
                    grupo,
                    "Rendimento",
                ),
            }
        )

    return pd.DataFrame(resultados)


def calcular_diferenca_rendimento(df):
    rendimentos = rendimento_por_genero(df)

    homens = rendimentos.loc[
        rendimentos["Genero"] == "Homens",
        "Rendimento médio",
    ].iloc[0]

    mulheres = rendimentos.loc[
        rendimentos["Genero"] == "Mulheres",
        "Rendimento médio",
    ].iloc[0]

    if pd.isna(homens) or pd.isna(mulheres) or homens <= 0:
        return np.nan

    return 100 * (homens - mulheres) / homens


def grafico(figura):
    figura.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=55, b=10),
        font=dict(size=13),
    )

    st.plotly_chart(
        figura,
        use_container_width=True,
    )


def ordenar_faixas(valores, ordem):
    return [
        item
        for item in ordem
        if item in valores
    ]


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data(show_spinner="Carregando dados da PNAD Contínua...")
def carregar_dados():
    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    df = pd.read_csv(ARQUIVO_DADOS)

    faltantes = [
        coluna
        for coluna in COLUNAS_OBRIGATORIAS
        if coluna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Colunas ausentes na base: "
            + ", ".join(faltantes)
        )

    for coluna in ["Ocupado", "Rendimento", "Peso"]:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce",
        )

    if "Idade" in df.columns:
        df["Idade"] = pd.to_numeric(
            df["Idade"],
            errors="coerce",
        )

    df = df[
        (df["Ocupado"] == 1)
        & (df["Peso"] > 0)
        & df["Genero"].isin(["Homens", "Mulheres"])
    ].copy()

    return df


@st.cache_resource(show_spinner="Carregando modelo preditivo...")
def carregar_modelo():
    return joblib.load(ARQUIVO_MODELO)


@st.cache_data
def carregar_metricas():
    with ARQUIVO_METRICAS.open(
        "r",
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


try:
    dados = carregar_dados()

except (FileNotFoundError, ValueError) as erro:
    st.error(str(erro))
    st.stop()

if dados.empty:
    st.error("A base não possui registros ocupados válidos.")
    st.stop()


# ============================================================
# CABEÇALHO
# ============================================================

st.title(
    "Desigualdade de Gênero no Mercado de Trabalho "
    "em São Paulo"
)

st.write(
    "Análise dos dados da Pesquisa Nacional por Amostra "
    "de Domicílios Contínua (PNAD Contínua), do IBGE, "
    "referentes ao 4º trimestre de 2025."
)

st.caption(
    "Projeto acadêmico de Introdução à Ciência de Dados "
    "— Tecnologia em Sistemas para Internet | "
    "Centro Universitário Senac"
)

st.divider()


# ============================================================
# NAVEGAÇÃO E FILTROS LATERAIS
# ============================================================

with st.sidebar:
    st.title("Painel de análise")

    pagina = st.radio(
        "Navegação",
        [
            "Visão geral",
            "Rendimento",
            "Setores econômicos",
            "Perfil dos trabalhadores",
            "Análise preditiva",
        ],
    )

    st.divider()
    st.subheader("Filtros")

    idades_disponiveis = ordenar_faixas(
        dados["Faixa_Etaria"].dropna().unique(),
        ORDEM_IDADE,
    )

    idades = st.multiselect(
        "Faixa etária",
        options=idades_disponiveis,
        default=idades_disponiveis,
    )

    escolaridades_disponiveis = ordenar_faixas(
        dados["Escolaridade"].dropna().unique(),
        ORDEM_ESCOLARIDADE,
    )

    escolaridades = st.multiselect(
        "Escolaridade",
        options=escolaridades_disponiveis,
        default=escolaridades_disponiveis,
    )

    setores_disponiveis = sorted(
        dados["Setor"].dropna().unique().tolist()
    )

    setores = st.multiselect(
        "Setores econômicos",
        options=setores_disponiveis,
        default=setores_disponiveis,
    )

    st.divider()

    st.caption(
        "Os filtros são aplicados às análises descritivas. "
        "O modelo preditivo foi treinado com a amostra "
        "completa de registros elegíveis."
    )


# ============================================================
# APLICAÇÃO DOS FILTROS
# ============================================================

filtrados = dados[
    dados["Faixa_Etaria"].isin(idades)
    & dados["Escolaridade"].isin(escolaridades)
    & dados["Setor"].isin(setores)
].copy()

if filtrados.empty and pagina != "Análise preditiva":
    st.warning(
        "Nenhum registro foi encontrado com os filtros "
        "selecionados. Ajuste os filtros na lateral."
    )
    st.stop()

ocupados = filtrados.copy()

rendimentos = rendimento_por_genero(ocupados)

participacao = participacao_feminina(ocupados)
diferenca = calcular_diferenca_rendimento(ocupados)


# ============================================================
# VISÃO GERAL
# ============================================================

if pagina == "Visão geral":
    st.header("Visão geral do mercado de trabalho")

    st.write(
        "Esta seção apresenta a participação de mulheres "
        "e homens entre as pessoas ocupadas e compara "
        "seus rendimentos mensais habituais."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Participação feminina",
            percentual(participacao),
        )

    with col2:
        rendimento_mulheres = rendimentos.loc[
            rendimentos["Genero"] == "Mulheres",
            "Rendimento médio",
        ].iloc[0]

        st.metric(
            "Rendimento médio das mulheres",
            moeda(rendimento_mulheres),
        )

    with col3:
        st.metric(
            "Diferença de rendimento",
            percentual(diferenca),
        )

    st.caption(
        "A diferença é calculada em relação ao rendimento "
        "médio dos homens. As estimativas utilizam os "
        "pesos amostrais da pesquisa."
    )

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        participacoes = (
            ocupados.groupby("Genero", as_index=False)["Peso"]
            .sum()
        )

        fig = px.pie(
            participacoes,
            names="Genero",
            values="Peso",
            hole=0.55,
            color="Genero",
            color_discrete_map=CORES,
            title="Participação entre pessoas ocupadas",
        )

        fig.update_traces(
            textinfo="label+percent",
        )

        grafico(fig)

    with col_b:
        fig = px.bar(
            rendimentos.dropna(),
            x="Genero",
            y="Rendimento médio",
            color="Genero",
            color_discrete_map=CORES,
            text="Rendimento médio",
            title="Rendimento médio habitual por gênero",
            labels={
                "Genero": "Gênero",
                "Rendimento médio": "Rendimento médio (R$)",
            },
        )

        fig.update_traces(
            texttemplate="R$ %{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            showlegend=False,
        )

        grafico(fig)

    st.info(
        "Os resultados mostram diferenças de participação "
        "e rendimento entre homens e mulheres. "
        "Essas diferenças são descritivas e não permitem "
        "concluir, isoladamente, quais fatores as causaram."
    )


# ============================================================
# RENDIMENTO
# ============================================================

elif pagina == "Rendimento":
    st.header("Análise dos rendimentos")

    st.write(
        "Comparação do rendimento mensal habitual de "
        "trabalhadores ocupados por gênero."
    )

    validos = ocupados[
        (ocupados["Rendimento"] > 0)
        & (ocupados["Peso"] > 0)
    ].copy()

    if validos.empty:
        st.warning(
            "Não há rendimentos positivos para "
            "os filtros selecionados."
        )

    else:
        col1, col2, col3 = st.columns(3)

        homens = rendimentos.loc[
            rendimentos["Genero"] == "Homens",
            "Rendimento médio",
        ].iloc[0]

        mulheres = rendimentos.loc[
            rendimentos["Genero"] == "Mulheres",
            "Rendimento médio",
        ].iloc[0]

        with col1:
            st.metric(
                "Média — Homens",
                moeda(homens),
            )

        with col2:
            st.metric(
                "Média — Mulheres",
                moeda(mulheres),
            )

        with col3:
            st.metric(
                "Diferença relativa",
                percentual(diferenca),
            )

        fig = px.bar(
            rendimentos.dropna(),
            x="Genero",
            y="Rendimento médio",
            color="Genero",
            color_discrete_map=CORES,
            text="Rendimento médio",
            title="Rendimento mensal habitual por gênero",
        )

        fig.update_traces(
            texttemplate="R$ %{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            showlegend=False,
        )

        grafico(fig)

        st.subheader("Rendimento por escolaridade")

        resultados = []

        for (nivel, genero), grupo in validos.groupby(
            ["Escolaridade", "Genero"]
        ):
            resultados.append(
                {
                    "Escolaridade": nivel,
                    "Genero": genero,
                    "Rendimento médio": media_ponderada(
                        grupo,
                        "Rendimento",
                    ),
                }
            )

        tabela = pd.DataFrame(resultados)

        if not tabela.empty:
            fig = px.bar(
                tabela,
                x="Escolaridade",
                y="Rendimento médio",
                color="Genero",
                barmode="group",
                color_discrete_map=CORES,
                category_orders={
                    "Escolaridade": ORDEM_ESCOLARIDADE,
                },
                title="Rendimento médio por escolaridade e gênero",
            )

            fig.update_layout(
                xaxis_tickangle=-30,
            )

            grafico(fig)

            st.dataframe(
                tabela,
                use_container_width=True,
                hide_index=True,
            )

        st.caption(
            "A renda média é ponderada pelos pesos amostrais. "
            "O gráfico por escolaridade permite observar "
            "diferenças entre os grupos, mas não estabelece "
            "relações de causalidade."
        )


# ============================================================
# SETORES ECONÔMICOS
# ============================================================

elif pagina == "Setores econômicos":
    st.header("Participação por setor econômico")

    st.write(
        "Distribuição de homens e mulheres entre os "
        "diferentes setores de atividade econômica."
    )

    setores_genero = (
        ocupados.groupby(
            ["Setor", "Genero"],
            as_index=False,
        )["Peso"]
        .sum()
    )

    setores_genero["Participação (%)"] = (
        setores_genero["Peso"]
        / setores_genero.groupby("Setor")["Peso"].transform("sum")
        * 100
    )

    ordem_setores = (
        ocupados.groupby("Setor")["Peso"]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig = px.bar(
        setores_genero,
        x="Setor",
        y="Participação (%)",
        color="Genero",
        barmode="stack",
        color_discrete_map=CORES,
        category_orders={
            "Setor": ordem_setores,
        },
        title="Composição por gênero em cada setor",
        labels={
            "Participação (%)": "Participação (%)",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-35,
        yaxis_range=[0, 100],
    )

    grafico(fig)

    st.write(
        "Cada coluna representa 100% das pessoas ocupadas "
        "no respectivo setor, dentro do recorte selecionado."
    )

    participacao_setor = []

    for setor, grupo in ocupados.groupby("Setor"):
        participacao_setor.append(
            {
                "Setor": setor,
                "Participação feminina (%)": (
                    participacao_feminina(grupo)
                ),
            }
        )

    tabela_setores = pd.DataFrame(participacao_setor)

    if not tabela_setores.empty:
        tabela_setores = tabela_setores.sort_values(
            "Participação feminina (%)",
            ascending=False,
        )

        st.subheader("Participação feminina por setor")

        fig = px.bar(
            tabela_setores,
            x="Participação feminina (%)",
            y="Setor",
            orientation="h",
            title="Percentual de mulheres em cada setor",
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending",
            },
        )

        grafico(fig)

        st.dataframe(
            tabela_setores,
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Os percentuais consideram os pesos amostrais "
        "e são calculados dentro de cada setor econômico."
    )


# ============================================================
# PERFIL DOS TRABALHADORES
# ============================================================

elif pagina == "Perfil dos trabalhadores":
    st.header("Perfil das pessoas ocupadas")

    st.write(
        "Análise da composição do mercado de trabalho "
        "por faixa etária e escolaridade."
    )

    st.subheader("Distribuição por faixa etária")

    idade_genero = (
        ocupados.groupby(
            ["Faixa_Etaria", "Genero"],
            as_index=False,
        )["Peso"]
        .sum()
    )

    idade_genero["Participação (%)"] = (
        idade_genero["Peso"]
        / idade_genero.groupby(
            "Faixa_Etaria"
        )["Peso"].transform("sum")
        * 100
    )

    fig = px.bar(
        idade_genero,
        x="Faixa_Etaria",
        y="Participação (%)",
        color="Genero",
        barmode="group",
        color_discrete_map=CORES,
        category_orders={
            "Faixa_Etaria": ORDEM_IDADE,
        },
        title="Composição por gênero e faixa etária",
        labels={
            "Faixa_Etaria": "Faixa etária",
        },
    )

    grafico(fig)

    st.subheader("Distribuição por escolaridade")

    escolaridade_genero = (
        ocupados.groupby(
            ["Escolaridade", "Genero"],
            as_index=False,
        )["Peso"]
        .sum()
    )

    escolaridade_genero["Participação (%)"] = (
        escolaridade_genero["Peso"]
        / escolaridade_genero.groupby(
            "Escolaridade"
        )["Peso"].transform("sum")
        * 100
    )

    fig = px.bar(
        escolaridade_genero,
        x="Escolaridade",
        y="Participação (%)",
        color="Genero",
        barmode="stack",
        color_discrete_map=CORES,
        category_orders={
            "Escolaridade": ORDEM_ESCOLARIDADE,
        },
        title="Composição por gênero e escolaridade",
    )

    fig.update_layout(
        xaxis_tickangle=-30,
        yaxis_range=[0, 100],
    )

    grafico(fig)

    st.caption(
        "Os gráficos mostram a composição de gênero "
        "dentro de cada grupo etário ou nível de escolaridade."
    )


# ============================================================
# ANÁLISE PREDITIVA
# ============================================================

elif pagina == "Análise preditiva":
    st.header("Análise preditiva")

    st.write(
        "Nesta seção, utilizamos aprendizado de máquina "
        "para estimar o rendimento mensal habitual de "
        "trabalhadores de São Paulo, com base na "
        "PNAD Contínua do 4º trimestre de 2025."
    )

    if not ARQUIVO_MODELO.exists() or not ARQUIVO_METRICAS.exists():
        st.warning(
            "Os arquivos do modelo ainda não foram encontrados. "
            "Execute 'parte 2/treinar_modelo.py' para gerá-los."
        )

    else:
        try:
            modelo = carregar_modelo()
            metricas = carregar_metricas()

        except Exception as erro:
            st.error(
                "Não foi possível carregar o modelo preditivo."
            )
            st.exception(erro)
            st.stop()

        # ----------------------------------------------------
        # METODOLOGIA
        # ----------------------------------------------------

        st.subheader("1. Metodologia")

        st.write(
            "Foi utilizado o algoritmo Random Forest Regressor, "
            "um método de regressão supervisionada baseado "
            "em múltiplas árvores de decisão."
        )

        st.write(
            "As variáveis explicativas do modelo são gênero, "
            "idade, escolaridade e setor econômico. "
            "A variável-alvo é o rendimento mensal habitual."
        )

        st.write(
            "A base foi dividida em 75% para treinamento "
            "e 25% para teste, com random_state=42. "
            "Os pesos amostrais foram utilizados no "
            "treinamento e no cálculo das métricas."
        )

        st.write(
            "O modelo foi treinado utilizando log1p do "
            "rendimento. As estimativas são convertidas "
            "para reais com a transformação inversa expm1."
        )

        # ----------------------------------------------------
        # MÉTRICAS
        # ----------------------------------------------------

        st.subheader("2. Avaliação do modelo")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Registros utilizados",
                numero(metricas["n_total"]),
            )

        with col2:
            st.metric(
                "Erro médio absoluto (MAE)",
                moeda(metricas["mae_reais"]),
            )

        with col3:
            st.metric(
                "Coeficiente R²",
                str(metricas["r2"]).replace(".", ","),
            )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric(
                "Amostra de treinamento",
                numero(metricas["n_treino"]),
            )

        with col_b:
            st.metric(
                "Amostra de teste",
                numero(metricas["n_teste"]),
            )

        with col_c:
            st.metric(
                "MAE da referência",
                moeda(metricas["mae_baseline_reais"]),
            )

        st.info(
            "O MAE indica o erro absoluto médio das "
            "estimativas em reais. O R² mede o desempenho "
            "do modelo na explicação das variações de "
            "rendimento no conjunto de teste. "
            "O resultado obtido demonstra capacidade "
            "preditiva limitada."
        )

        # ----------------------------------------------------
        # GRÁFICO DE ERROS
        # ----------------------------------------------------

        st.subheader("3. Erro das previsões por gênero")

        tabela_erros = pd.DataFrame(
            metricas["resultados_por_genero"]
        )

        if not tabela_erros.empty:
            fig = px.bar(
                tabela_erros,
                x="genero",
                y="mae_reais",
                color="genero",
                color_discrete_map=CORES,
                text="mae_reais",
                title="Erro médio absoluto por gênero",
                labels={
                    "genero": "Gênero",
                    "mae_reais": "MAE (R$)",
                },
            )

            fig.update_traces(
                texttemplate="R$ %{text:,.2f}",
                textposition="outside",
            )

            fig.update_layout(
                showlegend=False,
            )

            grafico(fig)

            tabela_formatada = tabela_erros.rename(
                columns={
                    "genero": "Gênero",
                    "n": "Registros de teste",
                    "mae_reais": "MAE (R$)",
                }
            )

            st.dataframe(
                tabela_formatada,
                use_container_width=True,
                hide_index=True,
            )

        st.caption(
            "Diferenças de erro entre gêneros não comprovam "
            "discriminação algorítmica, isoladamente. "
            "Esses resultados representam o desempenho "
            "observado na amostra de teste."
        )

        # ----------------------------------------------------
        # SIMULADOR
        # ----------------------------------------------------

        st.subheader("4. Simulador de rendimento")

        st.write(
            "Selecione as características de um perfil "
            "hipotético para calcular o rendimento mensal "
            "estimado pelo modelo."
        )

        generos_opcoes = sorted(
            dados["Genero"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        escolaridade_opcoes = ordenar_faixas(
            dados["Escolaridade"].dropna().unique(),
            ORDEM_ESCOLARIDADE,
        )

        setores_opcoes = sorted(
            dados["Setor"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        with st.form("formulario_previsao"):
            col1, col2 = st.columns(2)

            with col1:
                genero_prev = st.selectbox(
                    "Gênero",
                    generos_opcoes,
                )

                idade_prev = st.number_input(
                    "Idade",
                    min_value=14,
                    max_value=110,
                    value=30,
                    step=1,
                )

            with col2:
                escolaridade_prev = st.selectbox(
                    "Escolaridade",
                    escolaridade_opcoes,
                )

                setor_prev = st.selectbox(
                    "Setor econômico",
                    setores_opcoes,
                )

            calcular = st.form_submit_button(
                "Calcular rendimento estimado",
            )

        if calcular:
            entrada = pd.DataFrame(
                [
                    {
                        "Genero": genero_prev,
                        "Idade": int(idade_prev),
                        "Escolaridade": escolaridade_prev,
                        "Setor": setor_prev,
                    }
                ]
            )

            try:
                previsao_log = modelo.predict(entrada)[0]

                previsao = max(
                    0,
                    float(np.expm1(previsao_log)),
                )

                st.metric(
                    "Rendimento mensal estimado",
                    moeda(previsao),
                )

                st.caption(
                    "Este valor é uma estimativa estatística "
                    "para um perfil hipotético. "
                    "Não representa uma garantia salarial "
                    "nem uma previsão individual precisa."
                )

            except Exception as erro:
                st.error(
                    "Não foi possível calcular a previsão."
                )
                st.exception(erro)

        # ----------------------------------------------------
        # LIMITAÇÕES
        # ----------------------------------------------------

        st.subheader("5. Limitações da análise")

        st.write(
            "O modelo utiliza apenas quatro características "
            "dos trabalhadores. Outros fatores relevantes, "
            "como experiência profissional, jornada de "
            "trabalho, ocupação detalhada e tipo de vínculo, "
            "não foram incluídos."
        )

        st.write(
            "As informações são observacionais. "
            "Assim, as diferenças encontradas não permitem "
            "estabelecer causalidade ou identificar "
            "isoladamente discriminação salarial."
        )

        st.write(
            "O modelo foi treinado com a base completa de "
            "registros elegíveis. Os filtros laterais "
            "não alteram o treinamento nem as métricas "
            "apresentadas nesta página."
        )

        st.caption(
            "Fonte: IBGE — PNAD Contínua, "
            "4º trimestre de 2025, São Paulo."
        )


# ============================================================
# DOWNLOAD E INFORMAÇÕES
# ============================================================

st.divider()

with st.expander("Consultar e exportar os dados filtrados"):
    st.write(
        "A tabela apresenta os registros amostrais "
        "selecionados pelos filtros da barra lateral."
    )

    st.dataframe(
        filtrados,
        use_container_width=True,
        hide_index=True,
    )

    csv = filtrados.to_csv(
        index=False,
    ).encode("utf-8-sig")

    st.download_button(
        "Baixar dados filtrados (CSV)",
        data=csv,
        file_name="dados_filtrados_pnad_sp.csv",
        mime="text/csv",
    )


with st.expander("Sobre o projeto e a fonte de dados"):
    st.markdown(
        """
        **Projeto:** Desigualdade de Gênero no Mercado
        de Trabalho em São Paulo

        **Integrantes:**
        - Felipe Freitas
        - Wanessa Gonçalves

        **Disciplina:** Introdução à Ciência de Dados

        **Curso:** Tecnologia em Sistemas para Internet

        **Instituição:** Centro Universitário Senac

        **Fonte:** Instituto Brasileiro de Geografia
        e Estatística (IBGE), PNAD Contínua.

        **Período:** 4º trimestre de 2025.

        **Recorte geográfico:** Estado de São Paulo.

        **Observação metodológica:** Os indicadores
        utilizam os pesos amostrais dos registros.
        As análises são descritivas e não estabelecem
        relações causais.
        """
    )

st.caption(
    "Projeto acadêmico — Centro Universitário Senac | 2026"
)
