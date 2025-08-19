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



st.subheader('📈 Gráfico de inscrições acumuladas')
container = st.container()
with container:
    # Colunas que queremos acompanhar
    colunas = ["LB_PPI","LB_Q","LB_PCD","LB_EP",
            "LI_PPI","LI_Q","LI_PCD","LI_EP",
            "AC","Insc."]

    # Agrupar por data e somar
    df_grouped = df_filter_mapa.groupby("Data")[colunas].sum().reset_index()

    # Calcular acumulado
    df_cumsum = df_grouped.copy()
    # df_cumsum[colunas] = df_cumsum[colunas].cumsum()

    # Transformar em formato longo (para Plotly)
    df_melt = df_cumsum.melt(id_vars="Data", value_vars=colunas,
                            var_name="Categoria", value_name="Inscrições")

    # Criar gráfico com Plotly Express
    fig = px.line(df_melt, x="Data", y="Inscrições", color="Categoria",
                markers=True, title="Evolução Acumulada das Inscrições")

    # Mostrar no Streamlit
    st.plotly_chart(fig, use_container_width=True)




st.subheader('📊 Resumo dos dados')
# st.write(f"Total de inscritos: {df_filter.iloc[-1]['Total']}")
# colunas = ["Unidade","Curso","Modalidade","LB_PPI","LB_Q","LB_PCD","LB_EP",
#               "LI_PPI","LI_Q","LI_PCD","LI_EP",
#               "AC","Insc.","Data"]

colunas = ["Unidade","Curso","Modalidade","Vagas","LB_PPI","LB_Q","LB_PCD","LB_EP","LI_PPI","LI_Q","LI_PCD","LI_EP","AC","Insc.","1ª Op.","2ª Op.","3ª Op.","Insc. / Vagas","Insc. Válidas.","Insc. Vál. / Vagas","Data"]
st.dataframe(df_filter[colunas].sort_values(by='Insc.', ascending=False).reset_index(drop=True), use_container_width=True)
