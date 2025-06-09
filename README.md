# Relatório Executivo Interativo sobre Riscos Logísticos (Brasil, 2025)

Este projeto consiste em um dashboard interativo desenvolvido com Streamlit para análise e previsão de riscos logísticos no Brasil entre 01 de janeiro e 05 de junho de 2025.

## Conteúdo do Dashboard

O dashboard inclui:
- Visão geral do 1º semestre de 2025 com total de incidentes e custos
- Eventos críticos destacados (enchentes em MG, ciberataque à Tegma)
- Desempenho detalhado das TOP 3 transportadoras (Brado, JSL, Tegma)
- Mapa de calor geográfico com rotas críticas
- Previsões e riscos para Julho/2025
- Insights acionáveis e recomendações estratégicas

## Arquivos do Projeto

- `generate_data.py`: Script para geração dos dados fictícios verossímeis
- `riscos_logisticos_2025.csv`: Dataset gerado com os dados de incidentes
- `dashboard.py`: Código do dashboard interativo em Streamlit

## Como Executar Localmente

1. Instale as dependências:
```
pip install streamlit pandas numpy plotly matplotlib seaborn
```

2. Execute o dashboard:
```
streamlit run dashboard.py
```

## Parâmetros do Projeto

- **Período analisado**: 01/01/2025 a 05/06/2025
- **Transportadoras analisadas**: JSL, Rumo, Tegma, Brado, Mercúrio, LATAM Cargo
- **Variáveis-chave por incidente**:
  - Tipo de risco: Climático, Roubo, Acidente, Greve, Operacional
  - Custo associado: R$ milhões
  - Nível de criticidade: Baixo, Médio, Alto
  - Modal afetado: Rodoviário, Ferroviário, Aéreo

## Insights Principais

1. Os roubos na BR-040 cresceram 23% no 1º semestre de 2025, com pico em fevereiro.
2. O fenômeno El Niño intensificou eventos climáticos no Sul e Sudeste, elevando os custos logísticos em 27% no segundo trimestre.
3. Cargas de alto valor no modal rodoviário têm 3x mais chances de roubo.

## Alerta Prioritário (05/06–12/06/2025)

Greve anunciada por operadores ferroviários da Brado poderá impactar as operações entre Campinas e Santos. Recomenda-se redirecionar até 30% da carga para o modal rodoviário preventivamente.
