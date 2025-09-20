import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu  # para trabalhar com menu
from query import conexao  # A sua conexão com o banco de dados

# ------ PRIMEIRA CONSULTA E ATUALIZAÇÃO ------
query = "SELECT * FROM tb_carro"  # CONSULTA SQL
df = conexao(query)  # carregar os dados para a variável df

# Botão para atualização dos dados
if st.button("Atualizar Dados"):  # Atualização - botão
    df = conexao(query)

# --------- Estrutura de Filtro Lateral ---------
marca = st.sidebar.multiselect("Marca Selecionada", 
                               options=df["marca"].unique(),
                               default=df["marca"].unique())

modelo = st.sidebar.multiselect("Modelo Selecionado", 
                                options=df["modelo"].unique(),
                                default=df["modelo"].unique())

ano = st.sidebar.multiselect("Ano Selecionado", 
                             options=df["ano"].unique(),
                             default=df["ano"].unique())

cor = st.sidebar.multiselect("Cor Selecionada", 
                             options=df["cor"].unique(),
                             default=df["cor"].unique())

min_vendas = int(df['numero_vendas'].min())
max_vendas = int(df['numero_vendas'].max())

vendas = st.sidebar.slider(
    "Intervalo de número de vendas selecionado",
    min_value=min_vendas,
    max_value=max_vendas,
    value=(min_vendas, max_vendas)  # valor inicial
)

# ******* Verificação da aplicação dos filtros
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"] >= vendas[0]) &
    (df["numero_vendas"] <= vendas[1])
]

# Exibir os dados filtrados para depuração (opcional)
# st.write(df_selecionado)  # Remova esse código após garantir que tudo funciona

# ******* DASHBOARD *********
# CARDS DE VALORES
def PaginaInicial():
    # Expande para selecionar as opções
    with st.expander("Tabela de Carros"):
        exibicao = st.multiselect("Filtro",
                                  df_selecionado.columns,
                                  default=[],
                                  key="Filtro_Exibição"
                                  )
    if exibicao:
        st.write(df_selecionado[exibicao])

    if not df_selecionado.empty:
        total_Vendas = df_selecionado["numero_vendas"].sum()
        media_valor = df_selecionado['valor'].mean()
        media_vendas = df_selecionado["numero_vendas"].mean()

        card1, card2, card3 = st.columns(3, gap="large")
        with card1:
            st.info("Valor Total de Vendas", icon="📌")
            st.metric(label="Total (R$)", value=f"{total_Vendas:,.2f}")
        with card2:
            st.info("Valor Médio dos Carros", icon="📌")
            st.metric(label="Total (R$)", value=f"{media_valor:,.2f}")
        with card3:
            st.info("Valor Médio de Vendas", icon="📌")
            st.metric(label="Total (R$)", value=f"{media_vendas:,.2f}")

    else:
        st.warning("Nenhum dado disponível com os filtros selecionados")
        st.markdown("----")

def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para gerar gráficos")
        return
    
    graf1, graf2, graf3, graf4 = st.tabs(["Gráfico de Barras", "Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dispersão"])

    with graf1:
        st.write("Gráfico de Barras")
        valor = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)

        fig1 = px.bar(
            valor,
            x=valor.index,
            y="valor",
            orientation="h",
            title="Valores dos Carros",
            color_discrete_sequence=["#0084b8"]
        )

        st.plotly_chart(fig1, use_container_width=True)

    with graf2:
        st.write("Gráfico de Linhas")
        valor_linhas = df_selecionado.groupby("modelo").count()[["valor"]]

        fig2 = px.line(
            valor_linhas,
            x=valor_linhas.index,
            y="valor",
            title="Valor por modelo",
            color_discrete_sequence=["#e41c68"]
        )

        st.plotly_chart(fig2, use_container_width=True)

PaginaInicial()
graficos(df_selecionado)
