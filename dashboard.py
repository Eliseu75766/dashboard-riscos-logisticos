import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os

# Configuração da página
st.set_page_config(
    page_title="Relatório Executivo de Riscos Logísticos 2025",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('home/riscos_logisticos_2025.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

# Carregar os dados
df = load_data()

# Estilo personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        flex: 1;
        min-width: 200px;
        margin-right: 1rem;
    }
    .metric-title {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .metric-change {
        font-size: 0.9rem;
        font-weight: 500;
    }
    .metric-change-positive {
        color: #10B981;
    }
    .metric-change-negative {
        color: #EF4444;
    }
    .alert-box {
        background-color: #FECACA;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #DBEAFE;
        border-left: 5px solid #3B82F6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        color: #6B7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar para filtros
st.sidebar.title("Filtros")

# Filtro de data
date_range = st.sidebar.date_input(
    "Período",
    value=(datetime.date(2025, 1, 1), datetime.date(2025, 6, 5)),
    min_value=datetime.date(2025, 1, 1),
    max_value=datetime.date(2025, 6, 5)
)

# Filtro de transportadora
all_carriers = df['Transportadora'].unique().tolist()
selected_carriers = st.sidebar.multiselect(
    "Transportadoras",
    options=all_carriers,
    default=all_carriers
)

# Filtro de tipo de risco
all_risk_types = df['Tipo de Risco'].unique().tolist()
selected_risk_types = st.sidebar.multiselect(
    "Tipos de Risco",
    options=all_risk_types,
    default=all_risk_types
)

# Filtro de modal
all_modals = df['Modal Afetado'].unique().tolist()
selected_modals = st.sidebar.multiselect(
    "Modais",
    options=all_modals,
    default=all_modals
)

# Filtro de região
all_regions = df['Região'].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "Regiões",
    options=all_regions,
    default=all_regions
)

# Aplicar filtros
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Data'].dt.date >= start_date) & 
                             (filtered_df['Data'].dt.date <= end_date)]

if selected_carriers:
    filtered_df = filtered_df[filtered_df['Transportadora'].isin(selected_carriers)]

if selected_risk_types:
    filtered_df = filtered_df[filtered_df['Tipo de Risco'].isin(selected_risk_types)]

if selected_modals:
    filtered_df = filtered_df[filtered_df['Modal Afetado'].isin(selected_modals)]

if selected_regions:
    filtered_df = filtered_df[filtered_df['Região'].isin(selected_regions)]

# Cabeçalho principal
st.markdown('<div class="main-header">Relatório Executivo Interativo sobre Riscos Logísticos</div>', unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; margin-top: -10px;'>Brasil, 01/01/2025 - 05/06/2025</h3>", unsafe_allow_html=True)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Total de Incidentes</div>
        <div class="metric-value">{}</div>
        <div class="metric-change metric-change-negative">↑15% vs 2024</div>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)

with col2:
    total_cost = filtered_df['Custo Associado (R$)'].sum() / 1_000_000
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Custo Acumulado</div>
        <div class="metric-value">R$ {:.1f} milhões</div>
        <div class="metric-change metric-change-negative">↑27% no Q2 (El Niño)</div>
    </div>
    """.format(total_cost), unsafe_allow_html=True)

with col3:
    incidents_by_criticality = filtered_df['Nível de Criticidade'].value_counts()
    high_criticality = incidents_by_criticality.get('Alto', 0)
    high_criticality_pct = high_criticality / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Incidentes Críticos</div>
        <div class="metric-value">{} ({:.1f}%)</div>
        <div class="metric-change">Nível de Criticidade Alto</div>
    </div>
    """.format(high_criticality, high_criticality_pct), unsafe_allow_html=True)

with col4:
    top_route = filtered_df['Rota/Local Crítico'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
    top_route_count = filtered_df['Rota/Local Crítico'].value_counts().iloc[0] if len(filtered_df) > 0 else 0
    top_route_pct = top_route_count / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Rota Mais Crítica</div>
        <div class="metric-value">{}</div>
        <div class="metric-change">{} incidentes ({:.1f}%)</div>
    </div>
    """.format(top_route, top_route_count, top_route_pct), unsafe_allow_html=True)

# Alerta prioritário da semana
st.markdown("""
<div class="alert-box">
    <h3>⚠️ Alerta Prioritário da Semana (05/06–12/06)</h3>
    <p>Greve anunciada por operadores ferroviários da Brado poderá impactar as operações entre Campinas e Santos. 
    Recomenda-se redirecionar até 30% da carga para o modal rodoviário preventivamente.</p>
</div>
""", unsafe_allow_html=True)

# Seção 1: Visão Geral do 1º Semestre de 2025
st.markdown('<div class="sub-header">1. Visão Geral do 1º Semestre de 2025</div>', unsafe_allow_html=True)

# Gráfico de linha temporal dos incidentes por mês, segmentado por tipo de risco
filtered_df['Mês'] = filtered_df['Data'].dt.strftime('%Y-%m')
incidents_by_month_risk = filtered_df.groupby(['Mês', 'Tipo de Risco']).size().reset_index(name='Incidentes')

fig_timeline = px.line(incidents_by_month_risk, x='Mês', y='Incidentes', color='Tipo de Risco',
                      title='Evolução de Incidentes por Tipo de Risco',
                      markers=True, line_shape='linear')
fig_timeline.update_layout(xaxis_title='Mês', yaxis_title='Número de Incidentes',
                         legend_title='Tipo de Risco', height=500)
st.plotly_chart(fig_timeline, use_container_width=True)

# Eventos críticos
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h4>Eventos Críticos</h4>
        <ul>
            <li><strong>Março:</strong> Enchentes em MG → R$ 18,2 milhões</li>
            <li><strong>Abril:</strong> Ciberataque à Tegma → 12h de paralisação operacional</li>
            <li><strong>05/06:</strong> Alerta de greve na Brado (SP)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Gráfico de pizza para distribuição de custos por tipo de risco
    cost_by_risk = filtered_df.groupby('Tipo de Risco')['Custo Associado (R$)'].sum().reset_index()
    cost_by_risk['Custo (R$ milhões)'] = cost_by_risk['Custo Associado (R$)'] / 1_000_000
    
    fig_cost_pie = px.pie(cost_by_risk, values='Custo (R$ milhões)', names='Tipo de Risco',
                         title='Distribuição de Custos por Tipo de Risco')
    fig_cost_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_cost_pie, use_container_width=True)

# Seção 2: Desempenho por Transportadora
st.markdown('<div class="sub-header">2. Desempenho por Transportadora (TOP 3)</div>', unsafe_allow_html=True)

# Tabela de desempenho das transportadoras
top_carriers_df = filtered_df[filtered_df['Transportadora'].isin(['Brado', 'JSL', 'Tegma'])]
carrier_metrics = top_carriers_df.groupby('Transportadora').agg(
    Incidentes=('Transportadora', 'count'),
    Custo_Total=('Custo Associado (R$)', 'sum')
).reset_index()

carrier_metrics['Custo Médio por Incidente'] = carrier_metrics['Custo_Total'] / carrier_metrics['Incidentes']
carrier_metrics['Custo Médio por Incidente'] = carrier_metrics['Custo Médio por Incidente'].map('R$ {:,.0f}'.format)
carrier_metrics['Custo_Total'] = carrier_metrics['Custo_Total'].map('R$ {:,.0f}'.format)

# Identificar riscos predominantes por transportadora
risk_by_carrier = {}
for carrier in ['Brado', 'JSL', 'Tegma']:
    carrier_df = filtered_df[filtered_df['Transportadora'] == carrier]
    if len(carrier_df) > 0:
        top_risk = carrier_df['Tipo de Risco'].value_counts().index[0]
        top_risk_pct = carrier_df['Tipo de Risco'].value_counts().iloc[0] / len(carrier_df) * 100
        risk_by_carrier[carrier] = f"{top_risk} ({top_risk_pct:.0f}%)"
    else:
        risk_by_carrier[carrier] = "N/A"

carrier_metrics['Riscos Predominantes'] = carrier_metrics['Transportadora'].map(risk_by_carrier)
carrier_metrics = carrier_metrics[['Transportadora', 'Incidentes', 'Custo Médio por Incidente', 'Riscos Predominantes']]

# Exibir tabela formatada
st.table(carrier_metrics)

# Gráfico de barras comparativo
carrier_incidents = filtered_df.groupby('Transportadora').size().reset_index(name='Incidentes')
carrier_incidents = carrier_incidents.sort_values('Incidentes', ascending=False)

fig_carriers = px.bar(carrier_incidents, x='Transportadora', y='Incidentes',
                     title='Número de Incidentes por Transportadora',
                     color='Transportadora')
fig_carriers.update_layout(xaxis_title='Transportadora', yaxis_title='Número de Incidentes')
st.plotly_chart(fig_carriers, use_container_width=True)

# Seção 3: Mapa de Calor Geográfico
st.markdown('<div class="sub-header">3. Mapa de Calor Geográfico</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Distribuição de incidentes por região
    region_incidents = filtered_df.groupby('Região').size().reset_index(name='Incidentes')
    region_incidents['Percentual'] = region_incidents['Incidentes'] / region_incidents['Incidentes'].sum() * 100
    
    fig_regions = px.bar(region_incidents, x='Região', y='Percentual',
                        title='Distribuição de Incidentes por Região (%)',
                        color='Região')
    fig_regions.update_layout(xaxis_title='Região', yaxis_title='Percentual de Incidentes (%)')
    st.plotly_chart(fig_regions, use_container_width=True)

with col2:
    # Rotas críticas
    route_incidents = filtered_df.groupby('Rota/Local Crítico').size().reset_index(name='Incidentes')
    route_incidents = route_incidents.sort_values('Incidentes', ascending=False).head(5)
    
    fig_routes = px.bar(route_incidents, x='Rota/Local Crítico', y='Incidentes',
                       title='Top 5 Rotas Críticas',
                       color='Rota/Local Crítico')
    fig_routes.update_layout(xaxis_title='Rota/Local Crítico', yaxis_title='Número de Incidentes')
    st.plotly_chart(fig_routes, use_container_width=True)

# Estatísticas comparativas
st.markdown("""
<div class="insight-box">
    <h3>Estatísticas Comparativas</h3>
    <ul>
        <li>↑23% nos roubos na BR-040 em relação ao mesmo período de 2024.</li>
        <li>↑27% nos custos logísticos no segundo trimestre devido ao El Niño.</li>
        <li>↓12% em acidentes no modal ferroviário comparado ao mesmo período de 2024.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Seção 4: Previsões e Riscos para Julho/2025
st.markdown('<div class="sub-header">4. Previsões e Riscos para Julho/2025</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h4>Previsões para Julho/2025</h4>
        <ul>
            <li><strong>Probabilidade de novos protestos:</strong> 68%</li>
            <li><strong>Rotas sob alerta:</strong> BR-116 (PR-SC)</li>
            <li><strong>Custo estimado:</strong> R$ 12 a 15 milhões</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Gráfico de previsão de incidentes
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
    incidents = [210, 195, 230, 215, 205, 185, 220]  # Julho é previsão
    
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=months[:6], y=incidents[:6],
        mode='lines+markers',
        name='Dados Históricos',
        line=dict(color='blue')
    ))
    fig_forecast.add_trace(go.Scatter(
        x=months[5:], y=incidents[5:],
        mode='lines+markers',
        name='Previsão',
        line=dict(color='red', dash='dash')
    ))
    fig_forecast.update_layout(
        title='Previsão de Incidentes para Julho/2025',
        xaxis_title='Mês',
        yaxis_title='Número de Incidentes'
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

# Insights Acionáveis
st.markdown('<div class="sub-header">Insights Acionáveis</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    <h4>1. Reforçar segurança nas rotas com mais roubos</h4>
    <p>Os roubos na BR-040 cresceram 23% no 1º semestre de 2025, com pico em fevereiro. Recomenda-se: 1) Aumentar patrulhamento, 2) Redirecionar 15% da carga para ferrovias, 3) Reforçar seguros até 15/06.</p>
</div>

<div class="insight-box">
    <h4>2. Redirecionar cargas de alto valor para modais menos vulneráveis</h4>
    <p>Análise mostra que cargas de alto valor no modal rodoviário têm 3x mais chances de roubo. Recomenda-se transferir 40% das cargas premium para o modal ferroviário nas rotas Sul-Sudeste.</p>
</div>

<div class="insight-box">
    <h4>3. Investir em sensores climáticos para prever riscos naturais</h4>
    <p>O fenômeno El Niño intensificou eventos climáticos no Sul e Sudeste, elevando os custos logísticos em 27% no segundo trimestre. Recomenda-se a instalação de sensores em 12 pontos críticos para antecipação de 48h em eventos climáticos severos.</p>
</div>
""", unsafe_allow_html=True)

# Comentário sobre o El Niño
st.markdown("""
<div class="card">
    <h4>Comentário sobre o El Niño (Q2/2025)</h4>
    <p>"O fenômeno El Niño intensificou eventos climáticos no Sul e Sudeste, elevando os custos logísticos em 27% no segundo trimestre. As enchentes em Minas Gerais em março foram o evento mais impactante, gerando custos de R$ 18,2 milhões e afetando principalmente as operações da JSL e Brado na região."</p>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("""
<div class="footer">
    <p>Relatório Executivo Interativo sobre Riscos Logísticos | Brasil, 2025 | Atualizado em: 05/06/2025</p>
</div>
""", unsafe_allow_html=True)
