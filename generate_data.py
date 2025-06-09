import pandas as pd
import numpy as np
import datetime

# Parâmetros
start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 6, 5)
num_incidents = 1240
total_cost_target = 89.7  # R$ milhões
carriers = ["JSL", "Rumo", "Tegma", "Brado", "Mercúrio", "LATAM Cargo"]
risk_types = ["Climático", "Roubo", "Acidente", "Greve", "Operacional"]
criticality_levels = ["Baixo", "Médio", "Alto"]
modals = ["Rodoviário", "Ferroviário", "Aéreo"]
regions = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

# Pesos para simular a distribuição desejada
carrier_weights = [0.20, 0.15, 0.18, 0.22, 0.13, 0.12] # JSL, Rumo, Tegma, Brado, Mercúrio, LATAM
risk_weights = [0.25, 0.30, 0.15, 0.05, 0.25] # Climático, Roubo, Acidente, Greve, Operacional
region_weights = [0.58, 0.15, 0.12, 0.10, 0.05] # Sudeste, Sul, Nordeste, Centro-Oeste, Norte
modal_weights = [0.70, 0.20, 0.10] # Rodoviário, Ferroviário, Aéreo
criticality_weights = [0.4, 0.35, 0.25] # Baixo, Médio, Alto

# Gerar datas aleatórias no período
date_range = pd.date_range(start_date, end_date)
dates = np.random.choice(date_range, num_incidents)

# Gerar dados aleatórios com base nos pesos
data = {
    "Data": dates,
    "Transportadora": np.random.choice(carriers, num_incidents, p=carrier_weights),
    "Tipo de Risco": np.random.choice(risk_types, num_incidents, p=risk_weights),
    "Nível de Criticidade": np.random.choice(criticality_levels, num_incidents, p=criticality_weights),
    "Modal Afetado": np.random.choice(modals, num_incidents, p=modal_weights),
    "Região": np.random.choice(regions, num_incidents, p=region_weights)
}

df = pd.DataFrame(data)

# Ajustar modais por transportadora (simplificado)
df.loc[df["Transportadora"] == "Rumo", "Modal Afetado"] = "Ferroviário"
df.loc[df["Transportadora"] == "Brado", "Modal Afetado"] = np.random.choice(["Ferroviário", "Rodoviário"], size=len(df[df["Transportadora"] == "Brado"]), p=[0.8, 0.2])
df.loc[df["Transportadora"] == "LATAM Cargo", "Modal Afetado"] = "Aéreo"
df.loc[~df["Transportadora"].isin(["Rumo", "Brado", "LATAM Cargo"]), "Modal Afetado"] = "Rodoviário"

# Ajustar tipos de risco predominantes para TOP 3
# Brado: Roubos (62%)
brado_indices = df[df["Transportadora"] == "Brado"].index
num_brado = len(brado_indices)
if num_brado > 0:
    df.loc[np.random.choice(brado_indices, int(num_brado * 0.62), replace=False), "Tipo de Risco"] = "Roubo"

# JSL: Climáticos (57%)
jsl_indices = df[df["Transportadora"] == "JSL"].index
num_jsl = len(jsl_indices)
if num_jsl > 0:
    df.loc[np.random.choice(jsl_indices, int(num_jsl * 0.57), replace=False), "Tipo de Risco"] = "Climático"

# Tegma: Operacionais (48%)
tegma_indices = df[df["Transportadora"] == "Tegma"].index
num_tegma = len(tegma_indices)
if num_tegma > 0:
    df.loc[np.random.choice(tegma_indices, int(num_tegma * 0.48), replace=False), "Tipo de Risco"] = "Operacional"

# Gerar custos associados (distribuição log-normal para simular custos maiores menos frequentes)
# Ajustar a média para chegar perto do total desejado
mean_cost_per_incident = (total_cost_target * 1_000_000) / num_incidents
# Usar uma distribuição gamma ou log-normal para custos
# Log-normal: Média = exp(mu + sigma^2 / 2), Var = (exp(sigma^2) - 1) * exp(2*mu + sigma^2)
# Vamos simplificar com uma exponencial + base, ajustando a escala
base_cost = 10000
scale_cost = mean_cost_per_incident * 0.8 # Ajustar escala para tentar atingir o alvo
costs = np.random.exponential(scale=scale_cost, size=num_incidents) + base_cost

# Aumentar custo para riscos críticos
costs[df["Nível de Criticidade"] == "Alto"] *= np.random.uniform(1.5, 3.0, size=len(costs[df["Nível de Criticidade"] == "Alto"]))
costs[df["Nível de Criticidade"] == "Médio"] *= np.random.uniform(1.1, 1.8, size=len(costs[df["Nível de Criticidade"] == "Médio"]))

# Ajustar custo total para ficar próximo de R$ 89.7M
costs = (costs / costs.sum()) * (total_cost_target * 1_000_000)
df["Custo Associado (R$)"] = costs.astype(int)

# Inserir eventos específicos
# Março: Enchentes em MG -> R$ 18,2 milhões (vamos alocar parte do custo total para isso)
enchentes_cost = 18_200_000
enchentes_indices = df[(df["Data"].dt.month == 3) & (df["Região"] == "Sudeste") & (df["Tipo de Risco"] == "Climático")].index
if len(enchentes_indices) > 0:
    # Selecionar alguns incidentes de enchente em março no Sudeste para ter custo alto
    num_high_cost_floods = min(len(enchentes_indices), 5) # Ex: 5 incidentes somam o custo
    chosen_flood_indices = np.random.choice(enchentes_indices, num_high_cost_floods, replace=False)

    # Reduzir custo de outros incidentes para compensar
    current_total_cost = df["Custo Associado (R$)"].sum()
    if current_total_cost > enchentes_cost:
        reduction_factor = 1 - (enchentes_cost / current_total_cost)
        df["Custo Associado (R$)"] = (df["Custo Associado (R$)"] * reduction_factor).astype(int)
    else:
        # Caso raro onde o custo das enchentes é maior que o total atual (improvável com os ajustes)
        df["Custo Associado (R$)"] = (df["Custo Associado (R$)"] * 0.1).astype(int) # Reduzir drasticamente

    # Atribuir custo aos incidentes de enchente escolhidos
    cost_per_flood = enchentes_cost / num_high_cost_floods
    df.loc[chosen_flood_indices, "Custo Associado (R$)"] = int(cost_per_flood)
    df.loc[chosen_flood_indices, "Nível de Criticidade"] = "Alto"
    # Garantir que o custo total ainda esteja próximo
    df["Custo Associado (R$)"] = (df["Custo Associado (R$)"] / df["Custo Associado (R$)"].sum()) * (total_cost_target * 1_000_000)
    df["Custo Associado (R$)"] = df["Custo Associado (R$)"].astype(int)

# Abril: Ciberataque à Tegma (vamos adicionar um evento específico)
ciberataque_date = datetime.date(2025, 4, 15) # Data exemplo
ciberataque_cost = np.random.randint(500_000, 2_000_000) # Custo exemplo
ciberataque_event = pd.DataFrame([{
    "Data": pd.Timestamp(ciberataque_date),
    "Transportadora": "Tegma",
    "Tipo de Risco": "Operacional",
    "Nível de Criticidade": "Alto",
    "Modal Afetado": "Rodoviário", # Ou relevante para Tegma
    "Região": "Sudeste", # Exemplo
    "Custo Associado (R$)": ciberataque_cost
}])
df = pd.concat([df, ciberataque_event], ignore_index=True)

# 05/06: Alerta de greve na Brado (SP) (Não é um incidente passado, mas um alerta. Será adicionado no texto do dashboard)

# Ajustar contagem total de incidentes para exatamente 1240, se necessário
if len(df) > num_incidents:
    df = df.sample(n=num_incidents, random_state=42).reset_index(drop=True)
elif len(df) < num_incidents:
    # Adicionar mais alguns incidentes genéricos se faltar
    num_missing = num_incidents - len(df)
    missing_dates = np.random.choice(date_range, num_missing)
    missing_data = {
        "Data": missing_dates,
        "Transportadora": np.random.choice(carriers, num_missing, p=carrier_weights),
        "Tipo de Risco": np.random.choice(risk_types, num_missing, p=risk_weights),
        "Nível de Criticidade": np.random.choice(criticality_levels, num_missing, p=criticality_weights),
        "Modal Afetado": np.random.choice(modals, num_missing, p=modal_weights),
        "Região": np.random.choice(regions, num_missing, p=region_weights),
        "Custo Associado (R$)": np.random.exponential(scale=mean_cost_per_incident * 0.5, size=num_missing).astype(int)
    }
    missing_df = pd.DataFrame(missing_data)
    # Ajustar modais para transportadoras específicas nos dados faltantes
    missing_df.loc[missing_df["Transportadora"] == "Rumo", "Modal Afetado"] = "Ferroviário"
    missing_df.loc[missing_df["Transportadora"] == "Brado", "Modal Afetado"] = np.random.choice(["Ferroviário", "Rodoviário"], size=len(missing_df[missing_df["Transportadora"] == "Brado"]), p=[0.8, 0.2])
    missing_df.loc[missing_df["Transportadora"] == "LATAM Cargo", "Modal Afetado"] = "Aéreo"
    missing_df.loc[~missing_df["Transportadora"].isin(["Rumo", "Brado", "LATAM Cargo"]), "Modal Afetado"] = "Rodoviário"
    df = pd.concat([df, missing_df], ignore_index=True)

# Reajustar custo total final
df["Custo Associado (R$)"] = (df["Custo Associado (R$)"] / df["Custo Associado (R$)"].sum()) * (total_cost_target * 1_000_000)
df["Custo Associado (R$)"] = df["Custo Associado (R$)"].astype(int)

# Adicionar coluna de rota crítica (simulada baseada na região)
def assign_route(region):
    if region == "Sudeste":
        return np.random.choice(["BR-040 (RJ-MG)", "Porto de Santos (SP)", "Aeroporto de Guarulhos (GRU)", "Outra Sudeste"], p=[0.3, 0.3, 0.2, 0.2])
    elif region == "Sul":
        return np.random.choice(["BR-116 (PR-SC)", "Outra Sul"], p=[0.4, 0.6])
    else:
        return f"Outra {region}"

df["Rota/Local Crítico"] = df["Região"].apply(assign_route)

# Garantir que as contagens das TOP 3 transportadoras estejam próximas do desejado
# Reajustar levemente se necessário (pode distorcer outras métricas, usar com cuidado)
# Exemplo: forçar contagem da Brado para 142
brado_target = 142
current_brado_count = df[df["Transportadora"] == "Brado"].shape[0]
diff = brado_target - current_brado_count
if diff != 0:
    other_indices = df[df["Transportadora"] != "Brado"].index
    brado_indices = df[df["Transportadora"] == "Brado"].index
    if diff > 0 and len(other_indices) >= diff:
        # Precisa adicionar Brado
        change_indices = np.random.choice(other_indices, diff, replace=False)
        df.loc[change_indices, "Transportadora"] = "Brado"
        # Reajustar modal e risco para Brado
        df.loc[change_indices, "Modal Afetado"] = np.random.choice(["Ferroviário", "Rodoviário"], size=len(change_indices), p=[0.8, 0.2])
        df.loc[np.random.choice(change_indices, int(len(change_indices) * 0.62), replace=False), "Tipo de Risco"] = "Roubo"
    elif diff < 0 and len(brado_indices) >= -diff:
        # Precisa remover Brado
        change_indices = np.random.choice(brado_indices, -diff, replace=False)
        # Trocar para outra transportadora (ex: JSL)
        df.loc[change_indices, "Transportadora"] = "JSL"
        # Reajustar modal e risco para JSL
        df.loc[change_indices, "Modal Afetado"] = "Rodoviário"
        df.loc[np.random.choice(change_indices, int(len(change_indices) * 0.57), replace=False), "Tipo de Risco"] = "Climático"

# Garantir contagem JSL
jsl_target = 128
current_jsl_count = df[df["Transportadora"] == "JSL"].shape[0]
diff_jsl = jsl_target - current_jsl_count
if diff_jsl != 0:
    other_indices_jsl = df[df["Transportadora"] != "JSL"].index
    jsl_indices = df[df["Transportadora"] == "JSL"].index
    if diff_jsl > 0 and len(other_indices_jsl) >= diff_jsl:
        change_indices_jsl = np.random.choice(other_indices_jsl, diff_jsl, replace=False)
        df.loc[change_indices_jsl, "Transportadora"] = "JSL"
        df.loc[change_indices_jsl, "Modal Afetado"] = "Rodoviário"
        df.loc[np.random.choice(change_indices_jsl, int(len(change_indices_jsl) * 0.57), replace=False), "Tipo de Risco"] = "Climático"
    elif diff_jsl < 0 and len(jsl_indices) >= -diff_jsl:
        change_indices_jsl = np.random.choice(jsl_indices, -diff_jsl, replace=False)
        df.loc[change_indices_jsl, "Transportadora"] = "Mercúrio" # Trocar para outra menos proeminente
        df.loc[change_indices_jsl, "Modal Afetado"] = "Rodoviário"

# Garantir contagem Tegma
tegma_target = 119
current_tegma_count = df[df["Transportadora"] == "Tegma"].shape[0]
diff_tegma = tegma_target - current_tegma_count
if diff_tegma != 0:
    other_indices_tegma = df[df["Transportadora"] != "Tegma"].index
    tegma_indices = df[df["Transportadora"] == "Tegma"].index
    if diff_tegma > 0 and len(other_indices_tegma) >= diff_tegma:
        change_indices_tegma = np.random.choice(other_indices_tegma, diff_tegma, replace=False)
        df.loc[change_indices_tegma, "Transportadora"] = "Tegma"
        df.loc[change_indices_tegma, "Modal Afetado"] = "Rodoviário"
        df.loc[np.random.choice(change_indices_tegma, int(len(change_indices_tegma) * 0.48), replace=False), "Tipo de Risco"] = "Operacional"
    elif diff_tegma < 0 and len(tegma_indices) >= -diff_tegma:
        change_indices_tegma = np.random.choice(tegma_indices, -diff_tegma, replace=False)
        df.loc[change_indices_tegma, "Transportadora"] = "Mercúrio"
        df.loc[change_indices_tegma, "Modal Afetado"] = "Rodoviário"

# Ordenar por data
df = df.sort_values(by="Data").reset_index(drop=True)

# Salvar em CSV
output_path = "/home/ubuntu/riscos_logisticos_2025.csv"
df.to_csv(output_path, index=False, date_format='%Y-%m-%d')

print(f"Dados fictícios gerados e salvos em {output_path}")
print(f"Total de incidentes: {len(df)}")
print(f"Custo total: R$ {df['Custo Associado (R$)'].sum() / 1_000_000:.1f} milhões")

# Verificar algumas métricas
print("\nVerificação de Métricas:")
print(f"Incidentes Brado: {df[df['Transportadora'] == 'Brado'].shape[0]}")
print(f"Incidentes JSL: {df[df['Transportadora'] == 'JSL'].shape[0]}")
print(f"Incidentes Tegma: {df[df['Transportadora'] == 'Tegma'].shape[0]}")
print(f"% Roubos Brado: {df[(df['Transportadora'] == 'Brado') & (df['Tipo de Risco'] == 'Roubo')].shape[0] / df[df['Transportadora'] == 'Brado'].shape[0]:.1%}")
print(f"% Climáticos JSL: {df[(df['Transportadora'] == 'JSL') & (df['Tipo de Risco'] == 'Climático')].shape[0] / df[df['Transportadora'] == 'JSL'].shape[0]:.1%}")
print(f"% Operacionais Tegma: {df[(df['Transportadora'] == 'Tegma') & (df['Tipo de Risco'] == 'Operacional')].shape[0] / df[df['Transportadora'] == 'Tegma'].shape[0]:.1%}")
print(f"% Região Sudeste: {df[df['Região'] == 'Sudeste'].shape[0] / len(df):.1%}")
