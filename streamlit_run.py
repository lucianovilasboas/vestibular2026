import streamlit as st 
import pandas as pd 
import plotly.express as px
from funcoes import load_data
from funcoes import get_last_modified_file

st.set_page_config(page_title="Vestibular IFMG 2026",  page_icon="📊", layout="wide")

df_all = load_data()  
 
_, image_col, _ = st.columns([2,5,2])

with image_col:
    st.image("ifmg-ps-2026.png")

# st.header(f'✔️ Vestibular IFMG 2026')
html_code = f"<div id=\"update\">Ultima atualização: {get_last_modified_file('dados/processed/all_data.csv')}</div>"
st.markdown(html_code, unsafe_allow_html=True)
# st.warning('Importante! Para esse levantamento estamos considerando apenas a primeira opção de curso do candidato.', icon="⚠️")


col1 = st.sidebar.container()
col2 = st.sidebar.container()
col3 = st.sidebar.container()

with col1:
    unidades = df_all['Unidade'].unique()
    unidade = st.selectbox('Selecione o campus:', unidades, key='unidade_select', index=len(unidades)-1)

df_unidade = df_all[df_all['Unidade'] == unidade]

with col2:
    modalidades = ["TODAS"] + list(df_unidade['Modalidade'].unique())
    modalidade = st.selectbox('Selecione a modalidade:', modalidades, key='modalidade_select')

ultima_data = list(df_all['Data'].unique())[-1]


if modalidade == "TODAS":
    df_filter = df_unidade[df_unidade['Data'] == ultima_data]
    df_filter_mapa = df_unidade
else:
    df_filter = df_unidade[(df_unidade['Modalidade'] == modalidade) & (df_unidade['Data'] == ultima_data)]
    df_filter_mapa = df_unidade[df_unidade['Modalidade'] == modalidade]


with col3:
    cursos = ["Todos"] + list(df_filter['Curso'].unique())
    curso = st.selectbox('Selecione o curso:', cursos, key='curso_select')


if curso != "Todos":
    df_filter = df_filter[df_filter['Curso'] == curso]
    df_filter_mapa = df_filter_mapa[df_filter_mapa['Curso'] == curso]




st.subheader('📈 Evolução das Inscrições')
st.write(f"**Unidade:** {unidade} | **Modalidade:** {modalidade} | **Curso:** {curso} | **Vagas:** {df_filter['Vagas'].sum()} | **Total de inscrições (1ª Op.):** {df_filter['1ª Op.'].sum()}")
# st.warning(f"ATENÇÃO: A coluna Insc. é a soma das colunas 1ª Op., 2ª Op. e 3ª Op.")
container = st.container()
with container:
    # Colunas que queremos acompanhar
    colunas = ["1ª Op.","2ª Op.","3ª Op.","AC","LB_PPI","LB_Q","LB_PCD","LB_EP","LI_PPI","LI_Q","LI_PCD","LI_EP"]
    # Agrupar por data e somar
    df_grouped = df_filter_mapa.groupby("Data")[colunas].sum().reset_index()
    # Calcular acumulado
    df_cumsum = df_grouped.copy()
    # df_cumsum[colunas] = df_cumsum[colunas].cumsum()
    # Transformar em formato longo (para Plotly)
    df_melt = df_cumsum.melt(id_vars="Data", value_vars=colunas, var_name="Categorias", value_name="Inscrições")
    # Criar gráfico com Plotly Express
    fig = px.line(df_melt, 
        x="Data", 
        y="Inscrições", 
        color="Categorias", 
        markers=True,
        category_orders={'Categorias': colunas},  # Define a ordem da legend   a
        title="Evolução das Inscrições ao Longo do Tempo",
        height=600)

    # Atualizar layout para mostrar todos os valores no hover
    fig.update_traces(mode="lines+markers", hovertemplate="%{y}")
    fig.update_layout(
        hovermode="x unified"  # mostra todas as séries no mesmo tooltip
    )

    # Deixar visíveis apenas as séries desejadas
    colunas_visiveis = ["1ª Op.","2ª Op.","3ª Op.","AC"]
    for trace in fig.data:
        if trace.name not in colunas_visiveis:
            trace.visible = "legendonly"

    # Mostrar no Streamlit
    st.plotly_chart(fig, use_container_width=True)

# insira um emiji apropriado para o resumo dos dados
st.subheader('📊 Resumo dos dados')

colunas = ["Unidade","Curso","Modalidade","Vagas",
           "1ª Op.","2ª Op.","3ª Op.","Todas Op.",
           "1ª Op. / Vagas","1ª Op. Homolog.","1ª Op. Homolog. / Vagas",
           "AC", "LB_PPI","LB_Q","LB_PCD", "LB_EP",
           "LI_PPI","LI_Q","LI_PCD","LI_EP", "Data"]

st.dataframe(df_filter[colunas].sort_values(by="Todas Op.", ascending=False).reset_index(drop=True), use_container_width=True)


st.markdown("""___""")


# Gere grafico de barras para cada unidade
st.subheader('📊 Comparativo de Inscrições por Unidade')

# Criar gráfico de barras comparando todas as unidades
col1_chart = st.container()

with col1_chart:
    df_all_filtered = df_all[df_all['Data'] == ultima_data]
    # remover as linhas com Curso = 'Todos'
    df_all_filtered = df_all_filtered[df_all_filtered['Curso'] != 'Todos']
    
    
    # Agrupar dados por unidade e modalidade, somando as inscrições da primeira opção
    df_unidades_modalidades = df_all_filtered.groupby(['Unidade', 'Modalidade'])['1ª Op.'].sum().reset_index()
    # ordenar por 1ª Op.
    df_unidades_modalidades = df_unidades_modalidades.sort_values(by='1ª Op.', ascending=False)

    
    # Criar gráfico de barras com Plotly
    fig_barras = px.bar(
        df_unidades_modalidades, 
        x='Unidade', 
        y='1ª Op.', 
        color='Modalidade',
        title='Total de Inscrições (1ª Opção) por Unidade e Modalidade',
        barmode='group'
    )
    
    # Atualizar layout
    fig_barras.update_layout(
        xaxis_title="Unidade",
        yaxis_title="Total de Inscrições (1ª Opção)",
        height=600,
        showlegend=True
    )
    
    # Rotacionar labels do eixo X para melhor visualização
    fig_barras.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_barras, use_container_width=True)




# Gráfico adicional: Evolução temporal por unidade
st.subheader('📈 Evolução das Inscrições por Unidade')

col1_chart_line = st.container()

with col1_chart_line:
    # Agrupar dados por data e unidade
    df_evolucao_unidades = df_all.groupby(['Data', 'Unidade'])['1ª Op.'].sum().reset_index()
    # remover as linhas com Curso = 'Todos'
    df_evolucao_unidades = df_evolucao_unidades[df_evolucao_unidades['Unidade'] != 'Todos']
    
    # Calcular o total de inscrições por unidade para ordenar a legenda
    df_totais_unidades = df_evolucao_unidades.groupby('Unidade')['1ª Op.'].sum().sort_values(ascending=False)
    ordem_legenda = df_totais_unidades.index.tolist()

    # Criar gráfico de linha para cada unidade
    fig_evolucao = px.line(
        df_evolucao_unidades,
        x='Data',
        y='1ª Op.',
        color='Unidade',
        title='Evolução das Inscrições (1ª Opção) por Unidade',
        markers=True,
        category_orders={'Unidade': ordem_legenda}  # Define a ordem da legenda
    )
    fig_evolucao.update_traces(mode="lines+markers", hovertemplate="%{y}")
    fig_evolucao.update_layout(
        height=600,
        hovermode="x unified"  # mostra todas as séries no mesmo tooltip
    )


    st.plotly_chart(fig_evolucao, use_container_width=True) 










st.markdown("""___""")
st.caption("Desenvolvido com ❤️ por [Luciano Espiridiao](luciano.espiridiao@ifmg.edu.br). 2025 - Todos os direitos reservados.")
