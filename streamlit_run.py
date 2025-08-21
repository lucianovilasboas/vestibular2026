import streamlit as st 
import pandas as pd 
import plotly.express as px
from funcoes import load_data
from funcoes import get_last_modified_file

st.set_page_config(page_title="Vestibular IFMG 2026",  page_icon="📊", layout="wide")

df_all = load_data()  
 

st.header(f'✔️ Vestibular IFMG 2026')
html_code = f"<div id=\"update\">Ultima atualização: {get_last_modified_file('dados/processed/all_data.csv')}</div>"
st.markdown(html_code, unsafe_allow_html=True)
# st.warning('Importante! Para esse levantamento estamos considerando apenas a primeira opção de curso do candidato.', icon="⚠️")



col1 = st.sidebar.container()
col2 = st.sidebar.container()
col3 = st.sidebar.container()

with col1:
    unidades = df_all['Unidade'].unique()
    unidade = st.selectbox('Selecione o campus:', unidades, key='unidade_select')

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
st.write(f"**Unidade:** {unidade} | **Modalidade:** {modalidade} | **Curso:** {curso} | **Total de inscrições:** {df_filter['Insc.'].sum()}")
st.warning(f"ATENÇÃO: A coluna Insc. é a soma das colunas 1ª Op., 2ª Op. e 3ª Op.")
container = st.container()
with container:
    # Colunas que queremos acompanhar
    colunas = ["Insc.","1ª Op.","2ª Op.","3ª Op.","LB_PPI","LB_Q","LB_PCD","LB_EP","LI_PPI","LI_Q","LI_PCD","LI_EP","AC"]
    # Agrupar por data e somar
    df_grouped = df_filter_mapa.groupby("Data")[colunas].sum().reset_index()
    # Calcular acumulado
    df_cumsum = df_grouped.copy()
    # df_cumsum[colunas] = df_cumsum[colunas].cumsum()
    # Transformar em formato longo (para Plotly)
    df_melt = df_cumsum.melt(id_vars="Data", value_vars=colunas, var_name="Categorias", value_name="Inscrições")
    # Criar gráfico com Plotly Express
    fig = px.line(df_melt, x="Data", y="Inscrições", color="Categorias", markers=True)

    # Deixar visíveis apenas as séries desejadas
    colunas_visiveis = ["1ª Op.","2ª Op.","3ª Op."]
    for trace in fig.data:
        if trace.name not in colunas_visiveis:
            trace.visible = "legendonly"

    # Mostrar no Streamlit
    st.plotly_chart(fig, use_container_width=True)




st.subheader('📊 Resumo dos dados')

colunas = ["Unidade","Curso","Modalidade","Vagas","Insc.","LB_PPI","LB_Q","LB_PCD","LB_EP","LI_PPI","LI_Q","LI_PCD","LI_EP","AC","1ª Op.","2ª Op.","3ª Op.","Insc. / Vagas","Insc. Válidas.","Insc. Vál. / Vagas","Data"]
st.dataframe(df_filter[colunas].sort_values(by='Insc.', ascending=False).reset_index(drop=True), use_container_width=True)

