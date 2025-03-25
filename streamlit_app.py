import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CRM TS - Visão 360º", layout="wide")

# Carrega dados
def load_data():
    df = pd.read_csv("leads_data.csv")
    df["Data de Contato"] = pd.to_datetime(df["Data de Contato"])
    return df

# Título do app
st.title("📊 CRM TS - Visão 360º")

# Carregando dados
data = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Leads Totais", len(data))
with col2:
    ganhos = len(data[data["Status"] == "Fechado (Ganho)"])
    taxa_conv = round((ganhos / len(data)) * 100, 2)
    st.metric("Taxa de Conversão", f"{taxa_conv}%")
with col3:
    tempo_medio = data["Dias até Fechamento"].mean()
    st.metric("Tempo Médio Fechamento", f"{tempo_medio:.1f} dias")

st.markdown("---")

# Gráficos
st.subheader("Distribuição por Etapas do Funil")
fig1 = px.histogram(data, x="Etapa", color="Responsável", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Conversões por Colaborador")
fig2 = data[data["Status"] == "Fechado (Ganho)"].groupby("Responsável").size().sort_values(ascending=False)
st.bar_chart(fig2)

st.subheader("Status dos Leads")
fig3 = px.pie(data, names="Status", title="Status Geral dos Leads")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Tabela
st.subheader("📋 Leads Detalhados")
st.dataframe(data, use_container_width=True)

# Sugestão de Treinamento
st.markdown("---")
st.subheader("📚 Sugestões de Treinamento")
etapa_counts = data["Etapa"].value_counts()
sugestoes = []

for etapa, count in etapa_counts.items():
    etapa_dif = data[data["Etapa"] == etapa]
    if len(etapa_dif[etapa_dif["Status"] != "Fechado (Ganho)"]) >= 5:
        sugestoes.append(f"⚠️ Muita dificuldade na etapa **{etapa}** — considera um treinamento focado!")

if sugestoes:
    for s in sugestoes:
        st.markdown(s)
else:
    st.markdown("✅ Nenhuma etapa crítica por enquanto!")
