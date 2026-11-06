
# Desigualdade de Gênero no Mercado de Trabalho em São Paulo

Projeto acadêmico desenvolvido para a disciplina de **Introdução à Ciência de Dados**, do curso de Tecnologia em Sistemas para Internet do Centro Universitário Senac.

## Integrantes

- Felipe Freitas
- Wanessa Gonçalves

**Curso:** Tecnologia em Sistemas para Internet — 5º semestre  
**Instituição:** Centro Universitário Senac  
**Ano:** 2026
**Deploy:** https://icd-desigualdade-genero.streamlit.app/


---

## 1. Sobre o projeto

O projeto tem como objetivo analisar diferenças de gênero no mercado de trabalho do estado de São Paulo, utilizando dados reais da Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua), realizada pelo IBGE.

A análise investiga diferenças entre mulheres e homens em relação à participação entre as pessoas ocupadas, aos rendimentos mensais habituais e à distribuição por setores econômicos.

Também são realizadas comparações por faixa etária e escolaridade.

O trabalho está dividido em três partes:

- **Parte 1:** coleta, pré-processamento, indicadores e análise exploratória.
- **Parte 2:** desenvolvimento de uma dashboard interativa utilizando Streamlit.
- **Parte 3:** modelagem preditiva e integração dos resultados à aplicação.

## 2. Problema de pesquisa

Quais diferenças existem entre mulheres e homens no mercado de trabalho do estado de São Paulo em relação à participação entre as pessoas ocupadas, aos rendimentos e à distribuição pelos setores de atividade econômica?

## 3. Fonte dos dados

Os dados utilizados são provenientes da PNAD Contínua, disponibilizada pelo Instituto Brasileiro de Geografia e Estatística (IBGE).

- **Fonte:** IBGE — PNAD Contínua
- **Período:** 4º trimestre de 2025
- **Recorte geográfico:** Estado de São Paulo
- **Código da UF:** 35
- **Base original:** PNADC_042025.zip
- **Registros da amostra paulista:** 38.483

Link oficial:

https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/2025/

O arquivo original contém os microdados da pesquisa. Para facilitar sua utilização na dashboard, foi criada uma base tratada em CSV.

As estimativas consideram os pesos amostrais disponibilizados pelo IBGE.

## 4. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Processamento e análise dos dados |
| Pandas | Manipulação e filtragem dos dados |
| NumPy | Cálculos estatísticos |
| Streamlit | Desenvolvimento da dashboard |
| Plotly | Gráficos interativos |
| Jupyter Notebook | Análise exploratória da Parte 1 |
| Git e GitHub | Versionamento e hospedagem do código |
| Visual Studio Code | Ambiente de desenvolvimento |

## 5. Estrutura do projeto

```text
ICD-Desigualdade-Genero/
│
├── dados/
│   └── dados_tratados.csv
│
├── parte 1/
│   ├── Parte1_Desigualdade_Genero.ipynb
│   └── Relatorio_ICD_Desigualdade_Genero.docx
│
├── parte 2/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 6. Parte 1 — Análise exploratória

Na primeira etapa, foi realizado o carregamento e o pré-processamento dos microdados da PNAD Contínua.

Foram selecionadas variáveis relacionadas a sexo, idade, escolaridade, condição de ocupação, setor econômico, rendimento e peso amostral.

O tratamento incluiu:

1. Seleção dos registros do estado de São Paulo.
2. Identificação e organização das variáveis.
3. Conversão das variáveis numéricas.
4. Tratamento de registros ausentes e inválidos.
5. Classificação das variáveis categóricas.
6. Cálculo de indicadores ponderados.
7. Construção de tabelas e gráficos comparativos.

### Indicadores principais

**Participação feminina entre as pessoas ocupadas**

Percentual estimado de mulheres em relação ao total de pessoas ocupadas.

**Diferença de rendimento entre homens e mulheres**

Comparação dos rendimentos médios mensais habituais do trabalho principal.

**Composição por setor econômico**

Participação percentual de mulheres e homens dentro dos diferentes setores econômicos.

### Resultados da Parte 1

| Indicador | Resultado |
|---|---:|
| Participação feminina | 44,78% |
| Participação masculina | 55,22% |
| Rendimento médio masculino | R$ 4.723,03 |
| Rendimento médio feminino | R$ 3.599,50 |
| Diferença percentual de rendimento | 23,79% |

Os resultados referem-se ao quarto trimestre de 2025 e foram calculados utilizando os pesos amostrais.

**Importante:** os percentuais de participação representam a composição entre as pessoas ocupadas, não a taxa de ocupação da população. Os rendimentos são mensais, não ajustados pela jornada de trabalho.

As diferenças observadas não comprovam, isoladamente, discriminação causada pelo gênero.

## 7. Parte 2 — Dashboard interativa

A Parte 2 transforma os resultados da análise exploratória em uma aplicação interativa desenvolvida com Streamlit.

A dashboard permite visualizar indicadores e explorar diferenças de gênero no mercado de trabalho paulista.

### Funcionalidades implementadas

- Carregamento dos dados tratados em CSV.
- Cálculo de indicadores com pesos amostrais.
- Exibição de três indicadores principais.
- Filtros interativos por faixa etária, escolaridade e setor econômico.
- Atualização automática dos indicadores e gráficos conforme os filtros.
- Gráficos interativos desenvolvidos com Plotly.
- Consulta e exportação de registros filtrados em CSV.
- Navegação entre diferentes seções da análise.

### Seções da aplicação

**Visão geral**

Apresenta os indicadores principais, um gráfico de rosca com a composição por gênero e um gráfico de barras comparando rendimentos médios.

**Rendimento**

Apresenta comparações dos rendimentos médios por escolaridade e gênero.

**Setores econômicos**

Mostra a participação percentual de mulheres e homens dentro dos setores de atividade econômica.

**Perfil dos trabalhadores**

Apresenta a evolução dos rendimentos médios entre diferentes faixas etárias, separadamente por gênero.

**Análise preditiva**

Seção reservada para apresentar os resultados da modelagem desenvolvida na Parte 3.

## 8. Justificativa dos componentes Streamlit

Os componentes foram escolhidos de acordo com sua utilidade para a análise de dados.

| Componente | Justificativa |
|---|---|
| `st.metric` | Destaca os três indicadores principais da pesquisa. |
| `st.sidebar` | Organiza a navegação e os filtros em uma área específica. |
| `st.radio` | Permite navegar entre as seções da dashboard. |
| `st.multiselect` | Permite selecionar faixas etárias, níveis de escolaridade e setores econômicos. |
| `st.columns` | Organiza indicadores e gráficos lado a lado. |
| `st.plotly_chart` | Exibe gráficos interativos para comparação dos resultados. |
| `st.dataframe` | Apresenta tabelas detalhadas dos dados analisados. |
| `st.download_button` | Permite exportar os registros filtrados em CSV. |
| `st.cache_data` | Evita o carregamento desnecessário da base a cada interação. |
| `st.info` e `st.caption` | Apresentam orientações, fontes e limitações da análise. |

Os filtros permitem modificar o conjunto de dados utilizado nos cálculos, facilitando comparações entre diferentes perfis de trabalhadores.

A escolha dos componentes prioriza clareza, interatividade e facilidade de utilização.

## 9. Gráficos interativos

A aplicação apresenta gráficos de diferentes tipos:

**Gráfico de rosca**

Composição percentual de mulheres e homens entre as pessoas ocupadas.

**Gráfico de barras**

Comparação dos rendimentos médios mensais por gênero e escolaridade.

**Gráfico de barras horizontais empilhadas**

Composição percentual de mulheres e homens nos setores econômicos.

**Gráfico de linhas**

Comparação dos rendimentos médios por faixa etária e gênero.

Os gráficos foram desenvolvidos com Plotly, permitindo interações como a consulta de valores ao posicionar o cursor sobre os elementos.

## 10. Como executar o projeto localmente

### Pré-requisitos

- Python instalado.
- Git instalado, caso deseje clonar o repositório.
- Visual Studio Code ou outro editor de código.
- Conexão com a internet para instalar as dependências.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/FelipeSF13/ICD-Desigualdade-Genero.git
```

### Passo 2 — Acessar a pasta

```bash
cd ICD-Desigualdade-Genero
```

### Passo 3 — Criar o ambiente virtual

No terminal do Windows:

```powershell
python -m venv .venv
```

### Passo 4 — Instalar as dependências

No PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Passo 5 — Executar a dashboard

```powershell
.\.venv\Scripts\python.exe -m streamlit run "parte 2/app.py"
```

### Passo 6 — Acessar a aplicação

Abra o navegador no endereço:

http://localhost:8501

O arquivo `dados/dados_tratados.csv` deve estar presente para que a aplicação carregue os dados.

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

## 11. Limitações da análise

A PNAD Contínua é uma pesquisa amostral. Portanto, os indicadores representam estimativas e não contagens censitárias.

O projeto utiliza pesos amostrais nos cálculos, mas não estima intervalos de confiança ou erros-padrão considerando integralmente o desenho amostral complexo.

Os indicadores de rendimento utilizam valores mensais habituais positivos e informados.

Além disso, os resultados apresentados correspondem a um único trimestre, não sendo possível identificar tendências históricas a partir desse período isoladamente.

A dashboard permite explorar associações e diferenças entre grupos, mas não estabelece relações de causalidade.

## 12. Parte 3 — Modelagem preditiva

A próxima etapa do projeto será dedicada à construção e avaliação de modelos preditivos.

Os resultados serão incorporados à seção "Análise preditiva" da dashboard.

Serão documentados, conforme o modelo desenvolvido:

- Objetivo da previsão.
- Variáveis utilizadas.
- Método de modelagem.
- Métricas de avaliação.
- Resultados e limitações.

**Status:** aguardando desenvolvimento da Parte 3.

## 13. Publicação

O código-fonte do projeto está hospedado no GitHub:

https://github.com/FelipeSF13/ICD-Desigualdade-Genero

O deploy público da aplicação poderá ser realizado posteriormente utilizando o Streamlit Community Cloud.

## 14. Referências

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Pesquisa Nacional por Amostra de Domicílios Contínua: microdados trimestrais. Disponível em:

https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pnad-continua.html

STREAMLIT. Documentação oficial. Disponível em:

https://docs.streamlit.io/

PLOTLY. Documentação oficial do Plotly para Python. Disponível em:

https://plotly.com/python/


---

**Centro Universitário Senac — 2026**  
**Introdução à Ciência de Dados**  
**Felipe Freitas e Wanessa Gonçalves**
