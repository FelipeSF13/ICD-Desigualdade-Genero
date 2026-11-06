
# Desigualdade de Gênero no Mercado de Trabalho em São Paulo

Projeto acadêmico de Introdução à Ciência de Dados, desenvolvido com dados reais da Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua), do Instituto Brasileiro de Geografia e Estatística (IBGE).

O objetivo é analisar diferenças entre mulheres e homens no mercado de trabalho paulista, considerando participação entre pessoas ocupadas, rendimentos, escolaridade, idade e setores econômicos.

## Informações do projeto

**Integrantes:** Felipe Freitas e Wanessa Gonçalves  
**Curso:** Tecnologia em Sistemas para Internet  
**Instituição:** Centro Universitário Senac  
**Disciplina:** Introdução à Ciência de Dados  
**Ano:** 2026

### Dashboard online

[Acessar a aplicação Streamlit](https://icd-desigualdade-genero.streamlit.app/)

## 1. Objetivo

Investigar diferenças de gênero no mercado de trabalho do estado de São Paulo, utilizando dados da PNAD Contínua do quarto trimestre de 2025.

O projeto procura responder às seguintes questões:

- Qual é a participação de mulheres e homens entre as pessoas ocupadas?
- Como os rendimentos médios mensais diferem entre os gêneros?
- Como a composição por gênero varia entre setores econômicos?
- Qual é a distribuição dos trabalhadores por idade e escolaridade?
- É possível estimar o rendimento mensal habitual com um modelo de aprendizado de máquina?

As análises possuem caráter exploratório, descritivo e preditivo, sem pretensão de identificar relações causais.

## 2. Fonte dos dados

Os dados utilizados são provenientes dos microdados trimestrais da PNAD Contínua, disponibilizados pelo IBGE.

**Pesquisa:** PNAD Contínua  
**Período:** 4º trimestre de 2025  
**Recorte geográfico:** Estado de São Paulo  
**Código da UF:** 35

A PNAD Contínua é uma pesquisa amostral. Por isso, os indicadores de participação e rendimento utilizam os pesos amostrais fornecidos pelo IBGE.

O arquivo original dos microdados não foi incluído no repositório devido ao seu tamanho.

A aplicação utiliza o arquivo tratado:

`dados/dados_tratados.csv`

## 3. Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Jupyter Notebook
- Streamlit
- Plotly
- Scikit-learn
- Joblib
- Git e GitHub

Pandas e NumPy são utilizados no tratamento e nos cálculos estatísticos.

O Jupyter Notebook organiza a análise exploratória da Parte 1.

Streamlit e Plotly são utilizados na construção da aplicação interativa.

Scikit-learn é utilizado para treinamento e avaliação do modelo preditivo, enquanto Joblib permite salvar e carregar o modelo.

## 4. Organização do repositório

```text
ICD-Desigualdade-Genero/
├── dados/
│   └── dados_tratados.csv
├── modelos/
│   ├── modelo_rendimento.joblib
│   └── metricas_modelo.json
├── parte 1/
│   ├── Parte1_Desigualdade_Genero.ipynb
│   └── Relatorio_ICD_Desigualdade_Genero.docx
├── parte 2/
│   ├── app.py
│   ├── modelo.py
│   └── treinar_modelo.py
├── requirements.txt
├── README.md
└── .gitignore
```

A pasta `parte 1` contém os materiais da análise exploratória.

A pasta `parte 2` contém a aplicação Streamlit e o código responsável pela modelagem preditiva.

A pasta `modelos` armazena o modelo treinado e as métricas de avaliação.

## 5. Preparação e tratamento dos dados

A preparação foi realizada a partir dos microdados da PNAD Contínua.

As principais variáveis utilizadas incluem:

| Variável | Descrição |
|---|---|
| UF | Unidade da Federação |
| V2007 | Sexo |
| V2009 | Idade |
| V1028 | Peso amostral |
| VD4002 | Condição de ocupação |
| VD4016 | Rendimento mensal habitual do trabalho principal |
| VD4010 | Grupamento de atividade econômica |
| VD3004 | Nível de instrução |

Foram selecionados registros referentes ao estado de São Paulo.

Para as análises de rendimento, são considerados valores positivos e válidos.

Os dados foram organizados em variáveis interpretáveis, como gênero, escolaridade, faixa etária, setor econômico e rendimento.

O tratamento resultou no arquivo `dados_tratados.csv`, utilizado pela dashboard e pela modelagem.

## 6. Parte 1 — Análise exploratória

A Parte 1 apresenta uma análise descritiva das diferenças entre mulheres e homens no mercado de trabalho paulista.

O estudo utiliza estatísticas ponderadas pelos pesos amostrais e visualizações para explorar a composição das pessoas ocupadas.

### Indicadores principais

| Indicador | Resultado |
|---|---:|
| Participação feminina | 44,78% |
| Participação masculina | 55,22% |
| Rendimento médio masculino | R$ 4.723,03 |
| Rendimento médio feminino | R$ 3.599,50 |
| Diferença percentual de rendimento | 23,79% |

Os resultados referem-se ao quarto trimestre de 2025.

A diferença percentual de rendimento é calculada em relação ao rendimento médio masculino.

**Importante:** os percentuais de participação representam a composição entre as pessoas ocupadas, e não a taxa de ocupação da população.

Os rendimentos são mensais e não foram ajustados pela jornada de trabalho.

As diferenças observadas não comprovam, isoladamente, discriminação causada pelo gênero.

## 7. Parte 2 — Dashboard interativa

A Parte 2 transforma os resultados da análise exploratória e da modelagem preditiva em uma aplicação interativa desenvolvida com Streamlit.

A dashboard permite visualizar indicadores, explorar diferenças entre grupos e consultar estimativas de rendimento calculadas por um modelo de aprendizado de máquina.

### Funcionalidades implementadas

- Carregamento dos dados tratados em CSV.
- Cálculo de indicadores utilizando pesos amostrais.
- Exibição dos três indicadores principais da pesquisa.
- Filtros por faixa etária, escolaridade e setor econômico.
- Atualização dos indicadores e gráficos conforme os filtros.
- Gráficos interativos desenvolvidos com Plotly.
- Consulta e exportação dos registros filtrados em CSV.
- Navegação entre cinco seções.
- Exibição dos resultados da modelagem preditiva.
- Apresentação das métricas MAE e R².
- Gráfico comparativo do erro das previsões por gênero.
- Simulador interativo de rendimento mensal.

### Seções da aplicação

**Visão geral**

Apresenta os indicadores principais, um gráfico de rosca com a composição das pessoas ocupadas por gênero e um gráfico de barras comparando rendimentos médios.

**Rendimento**

Apresenta comparações dos rendimentos médios por gênero e escolaridade.

**Setores econômicos**

Mostra a participação percentual de mulheres e homens dentro dos setores de atividade econômica.

**Perfil dos trabalhadores**

Apresenta a composição por gênero entre faixas etárias e níveis de escolaridade.

**Análise preditiva**

Apresenta a metodologia de modelagem, os resultados de avaliação, um gráfico de erros por gênero e um simulador de rendimento mensal para perfis hipotéticos.

## 8. Modelagem preditiva

A modelagem preditiva tem como objetivo estimar o rendimento mensal habitual de trabalhadores a partir de características disponíveis na base.

### Algoritmo

Foi utilizado o **Random Forest Regressor**, algoritmo de aprendizado de máquina supervisionado baseado na combinação de múltiplas árvores de decisão.

### Variável-alvo

- Rendimento mensal habitual.

### Variáveis explicativas

- Gênero.
- Idade.
- Escolaridade.
- Setor econômico.

### Preparação para o treinamento

Foram selecionados registros de pessoas ocupadas com rendimento positivo, peso amostral válido e informações completas das variáveis utilizadas.

O rendimento foi transformado utilizando `log1p` para o treinamento. As estimativas são convertidas novamente para reais por meio de `expm1`.

As variáveis categóricas são transformadas com `OneHotEncoder`.

### Divisão dos dados

O conjunto foi separado em:

- 75% para treinamento.
- 25% para teste.

Foi utilizado `random_state=42` para permitir a reprodução da divisão dos dados.

Os pesos amostrais foram considerados no treinamento e no cálculo das métricas de avaliação.

### Resultados obtidos

| Métrica | Resultado |
|---|---:|
| Registros válidos | 19.543 |
| Registros de treinamento | 14.657 |
| Registros de teste | 4.886 |
| Erro médio absoluto (MAE) | R$ 2.082,10 |
| Coeficiente R² | 0,1705 |
| MAE do modelo de referência | R$ 2.919,25 |

O modelo apresentou um erro médio absoluto menor do que o modelo de referência baseado na média ponderada do rendimento.

Entretanto, o valor de R² demonstra capacidade preditiva limitada.

### Avaliação por gênero

| Gênero | Registros de teste | MAE |
|---|---:|---:|
| Homens | 2.690 | R$ 2.416,26 |
| Mulheres | 2.196 | R$ 1.668,86 |

Esses resultados mostram diferenças no erro de previsão entre os grupos.

Entretanto, não permitem concluir, isoladamente, que o modelo apresenta discriminação algorítmica.

### Simulador de rendimento

A aplicação disponibiliza um formulário interativo no qual o usuário informa:

- Gênero.
- Idade.
- Escolaridade.
- Setor econômico.

Ao clicar em **Calcular rendimento estimado**, a aplicação utiliza o modelo treinado para gerar uma estimativa de rendimento mensal.

O valor apresentado é uma estimativa estatística para um perfil hipotético.

Não representa uma garantia salarial nem uma previsão individual precisa.

### Limitações da modelagem

A capacidade preditiva é limitada porque o modelo utiliza apenas quatro características explicativas.

Outras informações relevantes, como experiência profissional, ocupação detalhada, jornada de trabalho e tipo de vínculo, não foram incluídas.

O modelo utiliza dados de um único trimestre e não permite identificar tendências históricas.

A análise não estabelece relações causais entre gênero e rendimento.

Os filtros laterais da dashboard não realizam novo treinamento. As métricas preditivas correspondem ao conjunto de teste definido durante a modelagem.

## 9. Justificativa dos componentes Streamlit

Os componentes foram selecionados conforme sua utilidade para a exploração dos dados e a apresentação dos resultados.

| Componente | Justificativa |
|---|---|
| `st.metric` | Apresenta indicadores principais e métricas de avaliação do modelo. |
| `st.sidebar` | Organiza a navegação e os filtros. |
| `st.radio` | Permite alternar entre as seções da aplicação. |
| `st.multiselect` | Permite filtrar idade, escolaridade e setor econômico. |
| `st.columns` | Organiza indicadores e visualizações. |
| `st.plotly_chart` | Apresenta gráficos interativos. |
| `st.dataframe` | Exibe tabelas de dados e resultados. |
| `st.download_button` | Permite exportar os registros filtrados. |
| `st.cache_data` | Evita recarregar desnecessariamente os dados e as métricas. |
| `st.cache_resource` | Mantém o modelo preditivo carregado para reutilização. |
| `st.form` | Agrupa os campos do simulador de rendimento. |
| `st.selectbox` | Permite selecionar características categóricas do perfil. |
| `st.number_input` | Permite informar a idade para a simulação. |
| `st.form_submit_button` | Executa a previsão após o preenchimento do formulário. |
| `st.info` | Apresenta explicações metodológicas. |
| `st.caption` | Informa fontes, ressalvas e limitações. |
| `st.expander` | Organiza informações complementares e exportação dos dados. |

A escolha dos componentes prioriza clareza, interatividade e facilidade de utilização.

## 10. Visualizações interativas

A aplicação utiliza gráficos construídos com Plotly.

Entre as visualizações estão:

**Gráfico de rosca**

Apresenta a composição percentual de mulheres e homens entre as pessoas ocupadas.

**Gráfico de barras**

Compara os rendimentos médios mensais por gênero.

**Gráfico de barras agrupadas**

Permite comparar rendimentos por escolaridade e a composição por faixa etária.

**Gráfico de barras empilhadas**

Mostra a composição percentual por gênero em setores econômicos e níveis de escolaridade.

**Gráfico de barras horizontais**

Apresenta a participação feminina por setor econômico.

**Gráfico de avaliação preditiva**

Compara os erros médios absolutos obtidos pelo modelo para mulheres e homens.

As visualizações permitem consultar informações adicionais ao posicionar o cursor sobre os elementos.

## 11. Como executar o projeto localmente

### Pré-requisitos

- Python instalado.
- Git instalado, caso deseje clonar o repositório.
- Visual Studio Code ou outro editor de código.
- Conexão com a internet para instalar dependências.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/FelipeSF13/ICD-Desigualdade-Genero.git
```

### Passo 2 — Acessar a pasta

```bash
cd ICD-Desigualdade-Genero
```

### Passo 3 — Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

### Passo 4 — Instalar as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Passo 5 — Executar a dashboard

```powershell
.\.venv\Scripts\python.exe -m streamlit run "parte 2/app.py"
```

### Passo 6 — Acessar a aplicação

Abra o navegador em:

http://localhost:8501

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

### Treinar novamente o modelo

Caso seja necessário gerar novamente o modelo e as métricas, execute:

```powershell
.\.venv\Scripts\python.exe "parte 2/treinar_modelo.py"
```

O treinamento gera os arquivos:

```text
modelos/modelo_rendimento.joblib
modelos/metricas_modelo.json
```

O arquivo `dados/dados_tratados.csv` deve estar disponível para executar o treinamento e a aplicação.

Não é necessário ativar o ambiente virtual no PowerShell quando os comandos utilizam diretamente o executável Python da pasta `.venv`.

## 12. Limitações gerais

A PNAD Contínua é uma pesquisa amostral. Os indicadores apresentados são estimativas populacionais, e não contagens censitárias.

Os indicadores utilizam pesos amostrais, mas não foram calculados intervalos de confiança ou erros-padrão que considerem integralmente o desenho amostral complexo.

A análise de rendimentos considera valores mensais habituais positivos e informados.

O estudo corresponde exclusivamente ao quarto trimestre de 2025.

Por esse motivo, não é possível estabelecer tendências temporais a partir desse recorte isolado.

A dashboard permite explorar associações e diferenças entre grupos, mas não determina relações causais.

As previsões geradas pelo modelo devem ser interpretadas considerando suas limitações e o desempenho observado no conjunto de teste.

## 13. Publicação

O código-fonte está disponível no GitHub:

https://github.com/FelipeSF13/ICD-Desigualdade-Genero

A dashboard foi publicada utilizando o Streamlit Community Cloud:

https://icd-desigualdade-genero.streamlit.app/

A publicação permite acessar a aplicação pelo navegador, sem instalar Python localmente.

As atualizações enviadas à branch principal do repositório podem ser incorporadas ao aplicativo hospedado.

## 14. Referências

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Pesquisa Nacional por Amostra de Domicílios Contínua: microdados trimestrais. Disponível em:

https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pnad-continua.html

STREAMLIT. Documentação oficial. Disponível em:

https://docs.streamlit.io/

PLOTLY. Documentação oficial para Python. Disponível em:

https://plotly.com/python/

SCIKIT-LEARN. Documentação oficial. Disponível em:

https://scikit-learn.org/stable/

---

**Centro Universitário Senac — 2026**  
**Introdução à Ciência de Dados**  
**Felipe Freitas e Wanessa Gonçalves**
