
import streamlit as st

# ==================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==================================================

st.set_page_config(
    page_title="Desigualdade de Gênero | São Paulo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# ESTILO
# ==================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.07);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# MENU LATERAL
# ==================================================

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
            "Análise preditiva"
        ]
    )

    st.divider()

    st.subheader("Fonte dos dados")

    st.write("IBGE — PNAD Contínua")
    st.caption("Estado de São Paulo")
    st.caption("4º trimestre de 2025")

    st.divider()
    st.caption("Centro Universitário Senac — 2026")

# ==================================================
# CABEÇALHO
# ==================================================

st.title("Desigualdade de gênero no mercado de trabalho")

st.write(
    "Uma análise da participação, dos rendimentos "
    "e das atividades econômicas de mulheres e homens "
    "no estado de São Paulo."
)

st.caption(
    "Projeto acadêmico | Felipe Freitas e Wanessa Gonçalves"
)

st.divider()

# ==================================================
# VISÃO GERAL
# ==================================================

if pagina == "Visão geral":

    st.header("Visão geral do mercado de trabalho")

    st.write(
        "Esta seção apresentará os principais indicadores "
        "calculados a partir dos microdados da PNAD Contínua."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Participação feminina",
            value="—"
        )

    with col2:
        st.metric(
            label="Rendimento médio feminino",
            value="—"
        )

    with col3:
        st.metric(
            label="Diferença de rendimento",
            value="—"
        )

    st.info(
        "Os indicadores serão calculados após "
        "a integração dos dados da Parte 1."
    )

    st.subheader("Objetivo da análise")

    st.write(
        "Investigar diferenças entre mulheres e homens "
        "na participação entre pessoas ocupadas, "
        "na remuneração e na distribuição por "
        "setores de atividade econômica."
    )

# ==================================================
# RENDIMENTO
# ==================================================

elif pagina == "Rendimento":

    st.header("Análise de rendimentos")

    st.write(
        "Comparação dos rendimentos mensais habituais "
        "do trabalho principal entre mulheres e homens."
    )

    st.info(
        "Nesta seção serão incluídos gráficos "
        "interativos de rendimento por gênero."
    )

# ==================================================
# SETORES ECONÔMICOS
# ==================================================

elif pagina == "Setores econômicos":

    st.header("Distribuição por setor econômico")

    st.write(
        "Análise da participação de mulheres e homens "
        "nos diferentes setores de atividade econômica."
    )

    st.info(
        "Nesta seção será apresentado um gráfico "
        "interativo de participação por setor."
    )

# ==================================================
# PERFIL DOS TRABALHADORES
# ==================================================

elif pagina == "Perfil dos trabalhadores":

    st.header("Perfil dos trabalhadores")

    st.write(
        "Análise das diferenças de rendimento "
        "por escolaridade e faixa etária."
    )

    st.info(
        "Os filtros de escolaridade e faixa etária "
        "serão adicionados nesta seção."
    )

# ==================================================
# ANÁLISE PREDITIVA
# ==================================================

elif pagina == "Análise preditiva":

    st.header("Análise preditiva")

    st.write(
        "Esta seção receberá os resultados "
        "da modelagem preditiva desenvolvida "
        "na Parte 3 do projeto."
    )

    st.warning(
        "A modelagem preditiva ainda não foi realizada."
    )

# ==================================================
# RODAPÉ
# ==================================================

st.divider()

st.caption(
    "Fonte: IBGE — PNAD Contínua. "
    "Projeto desenvolvido para a disciplina "
    "Introdução à Ciência de Dados | SENAC — 2026."
)
