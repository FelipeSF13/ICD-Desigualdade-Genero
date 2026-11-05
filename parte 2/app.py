
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ======================================================
# CONFIGURAÇÃO
# ======================================================

st.set_page_config(
    page_title="Desigualdade de Gênero | São Paulo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent.parent
ARQUIVO = BASE / "dados" / "dados_tratados.csv"

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


# ======================================================
# ESTILO
# ======================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.07);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

@st.cache_data
def carregar_dados():
    if not ARQUIVO.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO}"
        )

    df = pd.read_csv(ARQUIVO)

    obrigatorias = [
        "Genero",
        "Ocupado",
        "Rendimento",
        "Peso",
        "Escolaridade",
        "Faixa_Etaria",
        "Setor",
    ]

    faltando = [
        coluna for coluna in obrigatorias
        if coluna not in df.columns
    ]

    if faltando:
        raise ValueError(
            "Colunas ausentes: " + ", ".join(faltando)
        )

    for coluna in ["Ocupado", "Rendimento", "Peso"]:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce",
        )

    df = df[
        df["Peso"].notna() &
        (df["Peso"] > 0)
    ].copy()

    return df


def media_ponderada(df):
    validos = df[
        df["Rendimento"].notna() &
        (df["Rendimento"] > 0) &
        (df["Peso"] > 0)
    ]

    if validos.empty:
        return np.nan

    return np.average(
        validos["Rendimento"],
        weights=validos["Peso"],
    )


def formato_moeda(valor):
    if pd.isna(valor):
        return "Sem dados"

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def dados_ocupados(df):
    return df[
        (df["Ocupado"] == 1) &
        df["Genero"].isin(["Homens", "Mulheres"])
    ].copy()


def calcular_indicadores(df):
    ocupados = dados_ocupados(df)

    total = ocupados["Peso"].sum()

    if total <= 0:
        return np.nan, np.nan, np.nan, np.nan

    peso_mulheres = ocupados.loc[
        ocupados["Genero"] == "Mulheres", "Peso"
    ].sum()

    participacao = peso_mulheres / total * 100

    mulheres = ocupados[
        ocupados["Genero"] == "Mulheres"
    ]

    homens = ocupados[
        ocupados["Genero"] == "Homens"
    ]

    renda_mulheres = media_ponderada(mulheres)
    renda_homens = media_ponderada(homens)

    diferenca = np.nan

    if (
        pd.notna(renda_homens)
        and renda_homens > 0
        and pd.notna(renda_mulheres)
    ):
        diferenca = (
            (renda_homens - renda_mulheres)
            / renda_homens * 100
        )

    return (
        participacao,
        renda_mulheres,
        renda_homens,
        diferenca,
    )


def tabela_rendimentos(df, coluna):
    ocupados = dados_ocupados(df)

    linhas = []

    for (categoria, genero), grupo in ocupados.groupby(
        [coluna, "Genero"],
        dropna=True,
        observed=True,
    ):
        media = media_ponderada(grupo)

        if pd.notna(media):
            linhas.append({
                coluna: categoria,
                "Genero": genero,
                "Rendimento médio": media,
            })

    return pd.DataFrame(linhas)


def configurar_grafico(fig, altura=430):
    fig.update_layout(
        height=altura,
        margin=dict(l=15, r=15, t=45, b=15),
        legend_title_text="Gênero",
        hovermode="closest",
    )

    return fig


# ======================================================
# CARREGAR BASE
# ======================================================

try:
    dados = carregar_dados()
except (FileNotFoundError, ValueError) as erro:
    st.error(str(erro))
    st.info(
        "Confira se dados_tratados.csv está "
        "na pasta dados, na raiz do projeto."
    )
    st.stop()


# ======================================================
# MENU E FILTROS
# ======================================================

with st.sidebar:
    st.title("📊 Análise de Dados")
    st.caption("Introdução à Ciência de Dados")
    st.divider()

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

    idades_disponiveis = [
        faixa for faixa in ORDEM_IDADE
        if faixa in dados["Faixa_Etaria"].dropna().unique()
    ]

    idades = st.multiselect(
        "Faixa etária",
        options=idades_disponiveis,
        default=idades_disponiveis,
    )

    escolaridades_disponiveis = [
        nivel for nivel in ORDEM_ESCOLARIDADE
        if nivel in dados["Escolaridade"].dropna().unique()
    ]

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

    st.caption(
        "Os filtros modificam os indicadores "
        "e as visualizações."
    )

    st.divider()
    st.write("**Fonte:** IBGE — PNAD Contínua")
    st.caption("São Paulo | 4º trimestre de 2025")
    st.caption("SENAC — 2026")


# ======================================================
# APLICAR FILTROS
# ======================================================

# Os filtros são aplicados à população ocupada.
# Registros sem categoria no recorte ficam fora
# das comparações filtradas.

filtrados = dados_ocupados(dados)

filtrados = filtrados[
    filtrados["Faixa_Etaria"].isin(idades) &
    filtrados["Escolaridade"].isin(escolaridades) &
    filtrados["Setor"].isin(setores)
].copy()

st.title("Desigualdade de gênero no mercado de trabalho")

st.write(
    "Análise da participação, dos rendimentos e "
    "dos setores econômicos de mulheres e homens "
    "no estado de São Paulo."
)

st.caption(
    "Felipe Freitas e Wanessa Gonçalves | "
    "Centro Universitário Senac"
)

st.divider()

if filtrados.empty:
    st.warning(
        "Nenhum registro corresponde aos filtros. "
        "Selecione mais opções na barra lateral."
    )
    st.stop()


# ======================================================
# INDICADORES
# ======================================================

participacao, renda_mulheres, renda_homens, diferenca = (
    calcular_indicadores(filtrados)
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Participação feminina",
        (
            f"{participacao:.2f}%"
            if pd.notna(participacao)
            else "Sem dados"
        ),
    )

with col2:
    st.metric(
        "Rendimento médio feminino",
        formato_moeda(renda_mulheres),
    )

with col3:
    st.metric(
        "Diferença de rendimento",
        (
            f"{diferenca:.2f}%"
            if pd.notna(diferenca)
            else "Sem dados"
        ),
    )

st.caption(
    "Indicadores ponderados pelo peso amostral. "
    "Participação calculada entre pessoas ocupadas "
    "do recorte selecionado. Rendimento mensal habitual "
    "do trabalho principal, considerando valores "
    "positivos e informados."
)

st.divider()


# ======================================================
# VISÃO GERAL
# ======================================================

if pagina == "Visão geral":
    st.header("Visão geral")

    st.write(
        "Os gráficos apresentam a composição das pessoas "
        "ocupadas e as diferenças de rendimento no "
        "recorte selecionado."
    )

    col_esq, col_dir = st.columns(2)

    with col_esq:
        participacao_genero = (
            filtrados.groupby("Genero")["Peso"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            participacao_genero,
            names="Genero",
            values="Peso",
            hole=0.5,
            title="Participação entre pessoas ocupadas",
            color="Genero",
            color_discrete_map=CORES,
        )

        fig.update_traces(
            textinfo="label+percent"
        )

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )

    with col_dir:
        tabela = pd.DataFrame({
            "Genero": ["Homens", "Mulheres"],
            "Rendimento": [
                renda_homens,
                renda_mulheres,
            ],
        }).dropna()

        fig = px.bar(
            tabela,
            x="Genero",
            y="Rendimento",
            color="Genero",
            title="Rendimento médio mensal",
            color_discrete_map=CORES,
            text_auto=".2f",
        )

        fig.update_layout(
            yaxis_title="Rendimento (R$)",
            xaxis_title="",
            showlegend=False,
        )

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )

    st.info(
        "Os resultados são estimativas descritivas da "
        "PNAD Contínua e não demonstram, isoladamente, "
        "causalidade ou discriminação."
    )


# ======================================================
# RENDIMENTO
# ======================================================

elif pagina == "Rendimento":
    st.header("Análise de rendimentos")

    tabela = tabela_rendimentos(
        filtrados,
        "Escolaridade",
    )

    if not tabela.empty:
        fig = px.bar(
            tabela,
            x="Escolaridade",
            y="Rendimento médio",
            color="Genero",
            barmode="group",
            title="Rendimento médio por escolaridade",
            color_discrete_map=CORES,
            category_orders={
                "Escolaridade": ORDEM_ESCOLARIDADE
            },
        )

        fig.update_layout(
            xaxis_title="Escolaridade",
            yaxis_title="Rendimento mensal (R$)",
        )

        st.plotly_chart(
            configurar_grafico(fig, 520),
            use_container_width=True,
        )

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True,
        )


# ======================================================
# SETORES ECONÔMICOS
# ======================================================

elif pagina == "Setores econômicos":
    st.header("Participação por setor econômico")

    tabela = (
        filtrados.groupby(["Setor", "Genero"])["Peso"]
        .sum()
        .unstack(fill_value=0)
    )

    tabela = tabela.reindex(
        columns=["Mulheres", "Homens"],
        fill_value=0,
    )

    percentuais = (
        tabela.div(tabela.sum(axis=1), axis=0) * 100
    ).fillna(0)

    percentuais = (
        percentuais.reset_index().melt(
            id_vars="Setor",
            var_name="Genero",
            value_name="Participação (%)",
        )
    )

    fig = px.bar(
        percentuais,
        x="Participação (%)",
        y="Setor",
        color="Genero",
        orientation="h",
        barmode="stack",
        title="Composição por gênero em cada setor",
        color_discrete_map=CORES,
    )

    fig.update_layout(
        xaxis_range=[0, 100],
        xaxis_title="Participação no setor (%)",
        yaxis_title="",
    )

    st.plotly_chart(
        configurar_grafico(fig, 590),
        use_container_width=True,
    )

    st.caption(
        "Cada barra representa a composição interna "
        "de um setor econômico."
    )


# ======================================================
# PERFIL DOS TRABALHADORES
# ======================================================

elif pagina == "Perfil dos trabalhadores":
    st.header("Perfil dos trabalhadores")

    tabela = tabela_rendimentos(
        filtrados,
        "Faixa_Etaria",
    )

    if not tabela.empty:
        fig = px.line(
            tabela,
            x="Faixa_Etaria",
            y="Rendimento médio",
            color="Genero",
            markers=True,
            title="Rendimento por faixa etária e gênero",
            color_discrete_map=CORES,
            category_orders={
                "Faixa_Etaria": ORDEM_IDADE
            },
        )

        fig.update_layout(
            xaxis_title="Faixa etária",
            yaxis_title="Rendimento mensal (R$)",
        )

        st.plotly_chart(
            configurar_grafico(fig, 480),
            use_container_width=True,
        )

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True,
        )


# ======================================================
# ANÁLISE PREDITIVA
# ======================================================

elif pagina == "Análise preditiva":
    st.header("Análise preditiva — Parte 3")

    st.info(
        "Os resultados da modelagem preditiva "
        "serão integrados nesta seção após a "
        "realização da Parte 3 do projeto."
    )

    st.write(
        "Esta seção apresentará o modelo utilizado, "
        "as métricas de avaliação, as previsões "
        "e as limitações da análise."
    )


# ======================================================
# DOWNLOAD E INFORMAÇÕES
# ======================================================

st.divider()

with st.expander("Consultar e exportar os dados filtrados"):
    st.write(
        "A tabela apresenta os registros amostrais "
        "selecionados pelos filtros."
    )

    st.dataframe(
        filtrados,
        use_container_width=True,
        hide_index=True,
    )

    csv = filtrados.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "Baixar dados filtrados (CSV)",
        data=csv,
        file_name="pnad_sp_filtrado.csv",
        mime="text/csv",
    )

st.caption(
    f"Registros amostrais no recorte: "
    f"{len(filtrados):,}".replace(",", ".")
)

st.caption(
    "Fonte: IBGE — PNAD Contínua, 4º trimestre de 2025. "
    "Elaboração própria. Estimativas descritivas, "
    "sem cálculo de intervalos de confiança."
)
