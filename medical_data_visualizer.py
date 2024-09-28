import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("boilerplate-medical-data-visualizer/medical_examination.csv")
print(df.head)


# 2
df['overweight'] = df['weight'] / (df['height'] ** 2).apply(lambda x: 1 if x > 25 else 0)

# 3
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)


# 4 - Função para desenhar o gráfico categórico
def draw_cat_plot():
    # 5 - Convertendo os dados para formato longo
    df_cat = pd.melt(df, id_vars=['cardio'], 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # 6 - Agrupando e contando os dados
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_cat.rename(columns={0: 'total'}, inplace=True)

    # 7 - Criando o gráfico categórico usando seaborn.catplot
    # Ajuste de altura, largura, e aspect para melhorar o layout
    fig = sns.catplot(x="variable", y="total", hue="value", col="cardio", 
                      data=df_cat, kind="bar", height=6, aspect=1.2)

    # 8 - Ajustando o layout para melhor visualização
    fig.fig.subplots_adjust(top=0.9)  # Aumenta o espaço no topo do gráfico
    fig.fig.suptitle('Distribuição dos Fatores Categóricos por Doença Cardiovascular')

    # Salvando o gráfico categórico
    fig.savefig('catploot.png')
    return fig.fig

# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & 
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(12, 12))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", linewidths=1, square=True, cbar_kws={"shrink": 0.5}, ax=ax)

    # 15



    # 16
    fig.savefig('heatmap.png')
    return fig