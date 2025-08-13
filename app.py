import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Jobs cancelados por mês",
    page_icon="📊",
    layout="wide",
)

# Carrega os dados do arquivo CSV
df = pd.read_csv("https://raw.githubusercontent.com/Where-is-V/Jobs-cancelados-mes/5078220065dc0a3be7555744136bf4316c19701a/dados-mes-final.csv")


# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Mês
meses_disponiveis = sorted(df['Mes'].unique())
meses_selecionados = st.sidebar.multiselect('Mês', meses_disponiveis, default=meses_disponiveis)

# Filtro de Top N jobs mais cancelados
top_n = st.sidebar.slider('Jobs mais cancelados', min_value=1, max_value=20, value=10)
top_jobs = df['nome_job'].value_counts().nlargest(top_n).index
df_filtrado = df[df['nome_job'].isin(top_jobs)]

# ...código existente...

# Aplica o filtro de mês também
df_filtrado = df_filtrado[df_filtrado['Mes'].isin(meses_selecionados)]

# Agrupa os dados para contar o número de cancelamentos por job
cancelamentos_por_job = df_filtrado['nome_job'].value_counts().reset_index()
cancelamentos_por_job.columns = ['nome_job', 'cancelamentos']

# Cria o gráfico de barras
fig = px.bar(
    cancelamentos_por_job,
    x='nome_job',
    y='cancelamentos',
    title=f"Top {top_n} Jobs Mais Cancelados",
    labels={'nome_job': 'Job', 'cancelamentos': 'Cancelamentos'},
    text='cancelamentos',
    color='cancelamentos',
    color_discrete_sequence=px.colors.qualitative.Pastel  # Paleta pastel clara
)

fig.update_layout(xaxis_tickangle=-45, showlegend=False)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)
#



